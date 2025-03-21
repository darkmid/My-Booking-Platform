import uuid
from typing import List

from flask_jwt_extended import get_current_user
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import NotFound

from app.campus.model import Campus
from app.core.service import BaseService
from app.core.storage import upload_file_to_s3, base64_to_filestorage
from app.course.model import Course, Lecture, LectureAttachment
from app.course.schema import (
    CourseCreateSchema,
    CoursePutSchema,
    LectureAttachmentSchema,
    LectureCreateSchema,
    LecturePutSchema,
)
from app.user.model import Teacher, User, Student
from app.core.convertor import prepare_reference_fields
from app.core.storage import base64_to_s3_storage

class CourseService(BaseService):
    def __init__(self, user: User) -> None:
        super().__init__(CourseService.__name__, user)

    def get_course_query(self, **kwargs):
        if self.user._cls == "User.Admin" and "course_admin" in self.user.permissions:
            return Course.objects(**kwargs)
        if self.user._cls == "User.Teacher":
            return Course.objects(teacher=self.user, **kwargs)
        else:
            return Course.objects(enrolled_students=self.user, **kwargs)

    def create_course(self, course: CourseCreateSchema) -> Course:
        self.logger.info("Creating courses")
        print(course.teacher, type(course.teacher))
        Campus.objects(id=course.campus).first_or_404("Campus not exists")
        Teacher.objects(id=course.teacher).first_or_404("Teacher not exists")
        print(course.teacher, type(course.teacher))
        # Store the cover image temporarily
        temp_cover_image = course.cover_image
        
        # Create course without cover image first
        course_data = course.dict(exclude={"cover_image"})
        new_course = Course(**course_data)
        new_course.save()
        
        # Now upload the cover image with course ID in the path
        if temp_cover_image:
            # Use the course ID in the S3 path
            s3_path = f"courses/{new_course.id}"
            
            # Update the course with the cover image URL
            new_course.cover_image = base64_to_s3_storage(temp_cover_image, s3_path)
            new_course.save()
        
        return new_course

    def list_courses(self, campus: str = None, teacher: str = None) -> List[Course]:
        self.logger.info("Fetching courses")
        querys = {}
        if campus is not None:
            querys["campus"] = campus
        if teacher is not None:
            querys["teacher"] = teacher
        return list(Course.objects(**querys))

    def get_course(self, course_id: str) -> Course:
        return self.get_course_query(id=course_id).first_or_404("Course not exists")

    def delete_course(self, course_id: str) -> int:
        course = self.get_course_query(id=course_id).first_or_404("Course not exists")
        if course.enrolled_students:
            self.logger.info(f"Removing course from {len(course.enrolled_students)} student enrollments")
            for student in course.enrolled_students:
                # Update student's enrolled_courses list
                Student.objects(id=student.id).update_one(pull__enrolled_courses=course.id)
    
        # Clean up S3 resources if needed
        if course.cover_image:
            # Here you might want to add S3 deletion logic
            # For example: s3.delete_object(Bucket=current_app.config["AWS_BUCKET_NAME"], Key=course.cover_image)
            self.logger.info(f"Deleting course cover image: {course.cover_image}")
        
        # For each lecture, clean up attachments if needed
        for lecture in course.lectures:
            for attachment in lecture.attachments:
                if attachment.bucket_url:
                    # Here you might want to add S3 deletion logic for attachments
                    self.logger.info(f"Deleting lecture attachment: {attachment.bucket_url}")
        
        # Perform the actual deletion
        course.delete()
        return 1  # Indicating successful deletion

    def update_course(self, course_id: str, course: CoursePutSchema):
        update_dict = course.dict(exclude_none=True)
        if "cover_image" in update_dict and update_dict.get("cover_image"):
            temp_cover_image = update_dict["cover_image"]
            s3_path = f"courses/{course_id}"
            update_dict["cover_image"] = base64_to_s3_storage(temp_cover_image, s3_path)

        update_dict = prepare_reference_fields(update_dict, {"teacher": (Teacher, "Teacher not exists")})   
        if len(update_dict) == 0:
            return
        
        Course.objects(id=course_id).first_or_404("Course not exists").update(
            **update_dict
        )

    def add_lecture(self, course_id: str, lecture: LectureCreateSchema) -> int:
        lecture.id = uuid.uuid4()
        course: Course = Course.objects(id=course_id).first_or_404("Course not exists")
        course.update(push__lectures=lecture.dict(exclude_none=True))
        return str(lecture.id)

    def list_lectures(self, course_id: str) -> List[Lecture]:
        return Course.objects(id=course_id).first_or_404("Course not exists").lectures

    def delete_lecture(self, course_id: str, lecture_id: str) -> int:
        return (
            Course.objects(id=course_id)
            .filter(lectures__id=lecture_id)
            .update_one(pull__lectures__id=lecture_id)
        )

    def update_lecture(
        self, course_id: str, lecture_id: str, lecture: LecturePutSchema
    ) -> int:
        update_action = {
            f"set__lectures__S__{key}": value
            for key, value in lecture.dict(exclude_defaults=True).items()
        }
        return (
            Course.objects(id=course_id)
            .filter(lectures__id=lecture_id)
            .update_one(**update_action)
        )

    def upload_lecture_attachment(
        self, course_id: str, lecture_id: str, file: FileStorage, file_type: str, name
    ):
        course: Course = Course.objects(id=course_id).first_or_404("Course not exists")
        lecture: Lecture = course.lectures.filter(id=lecture_id).first()
        if lecture is None:
            raise NotFound("Lecture not exists")

        url = upload_file_to_s3(
            file, f"courses/{course_id}/lectures/{lecture_id}/attachments"
        )
        attachment = LectureAttachment(
            name=name is not None and name or file.filename,
            filename=file.filename,
            type=file_type,
            bucket_url=url,
        )
        Course.objects(id=course_id).filter(lectures__id=lecture_id).update_one(
            push__lectures__S__attachments=attachment
        )

    def delete_attachment(self, course_id: str, lecture_id: str, filename: str):
        course: Course = Course.objects(id=course_id).first_or_404("Course not exists")
        lecture: Lecture = course.lectures.filter(id=lecture_id).first()

        if lecture is None:
            raise NotFound("Lecture not exists")

        del_num = lecture.attachments.filter(filename=filename).delete()
        course.save()
        return del_num, 200


def course_service():
    return CourseService(get_current_user())
