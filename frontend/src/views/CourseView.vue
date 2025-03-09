<script setup lang="ts">
import { useRoute } from "vue-router";
import { useCourse } from "@/api/course";
import { NSpin, NSpace, NH1, NDivider, NGrid, NGridItem } from "naive-ui";
import CourseDetails from "@/components/course/CourseDetails.vue";
import CourseLecture from "@/components/course/CourseLecture.vue";
import NewLectureButton from "@/components/course/NewLectureButton.vue";
import { useAuthStore } from "@/stores/auth";
import { useCourseStore } from "@/stores/course";
const route = useRoute();
const courseId = route.params.id.toString();
const { data: course, isFinished, execute: reloadCourse } = useCourse(courseId);

const authStore = useAuthStore();
const { hasPermission } = useAuthStore();
const courseStore = useCourseStore();
</script>

<template>
  <n-spin :show="!isFinished">
    <n-space vertical v-if="course">
      <n-h1>
        {{ course.name }}
        <span class="text-slate-400 text-xl">
          ({{ course.uni_course_code }})</span
        >
      </n-h1>
      <course-details :course="course" />
      <n-divider>Lectures</n-divider>
      <n-grid :cols="3" x-gap="24" y-gap="12">
        <n-grid-item v-for="lecture in course.lectures" :key="lecture.id">
          <course-lecture
            :lecture="lecture"
            :course_id="course.id"
            :is-admin="hasPermission('course_admin') || authStore.isTeacher"
            :on-update="reloadCourse"
          ></course-lecture>
        </n-grid-item>
      </n-grid>
      <n-divider v-if="hasPermission('course_admin') || authStore.isTeacher">
        <new-lecture-button
          :course-id="course.id"
          :on-created="reloadCourse"
        ></new-lecture-button>
      </n-divider>
    </n-space>
  </n-spin>
</template>
