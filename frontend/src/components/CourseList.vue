<script setup lang="ts">
import type { CourseBasicInfo } from "@/api/course";
import { createOrder } from "@/api/order";
import { deleteCourse } from "@/api/course";
import type { User } from "@/interfaces/user.interface";
import { useAuthStore } from "@/stores/auth";
import {
  NGrid,
  NGridItem,
  NCard,
  NA,
  NP,
  NSpace,
  NButton,
  NModal,
  NPopconfirm,
  useMessage,
} from "naive-ui";
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import UpdateCourseButton from "@/components/course/UpdateCourseButton.vue";

const props = defineProps<{
  userInfo: User;
  courses: CourseBasicInfo[];
}>();

const emit = defineEmits(['refresh']);

const router = useRouter();
const authStore = useAuthStore();
const message = useMessage();

const showPurchaseModal = ref(false);
const clickedCourse = ref<string>("");
const deletingCourses = ref<Map<string, boolean>>(new Map());

// Use require to import the image (or define the path)
const defaultCourseImage = '/src/assets/course_wrap.png';

// Responsive columns based on screen width
const gridCols = computed(() => {
  // Using a single number for responsive breakpoints
  return "1 s:2 m:3 l:3 xl:4 xxl:4";
});

const isEnrolledCourse = (course_id: string) => {
  if (props.userInfo?.permissions?.includes("course_admin") || authStore.isTeacher) {
    return true;
  } else {
    return props.userInfo?.enrolled_courses
      ?.map((c) => c.id)
      .includes(course_id);
  }
};

const isAdmin = computed(() => {
  return props.userInfo?.permissions?.includes("course_admin");
});

const handleCourseClick = (course_id: string) => {
  if (isEnrolledCourse(course_id)) {
    router.replace(`/courses/${course_id}`);
  } else {
    clickPurchase(course_id);
  }
};

const clickPurchase = (course_id: string) => {
  clickedCourse.value = course_id;
  showPurchaseModal.value = true;
};

const purchase = async () => {
  const orderId = await createOrder(
    clickedCourse.value,
    authStore.getUserInfo?.id!
  );
  message.success(`Course ordered. Order ID: ${orderId}`);
};

const handleDeleteCourse = async (courseId: string) => {
  try {
    deletingCourses.value.set(courseId, true);
    await deleteCourse(courseId);
    message.success('Course has been completely deleted');
    emit('refresh');
    if (router.currentRoute.value.params.id === courseId) {
      router.replace('/courses');
    }
  } catch (error) {
    console.error('Error deleting course:', error);
    message.error('Failed to delete the course');
  } finally {
    deletingCourses.value.delete(courseId);
  }
};

const handleCourseUpdated = () => {
  emit('refresh');
};
</script>
<template>
  <div class="course-list-container">
    <n-grid :cols="gridCols" :x-gap="16" :y-gap="24" responsive="screen">
      <n-grid-item v-for="course in courses" :key="course.id">
        <n-card :title="course.name" class="course-card">
          <template #cover>
            <div class="course-image-container">
              <n-a @click="handleCourseClick(course.id)" class="course-link">
                <img 
                  :src="course.cover_image || defaultCourseImage" 
                  :alt="course.name" 
                  class="course-image" 
                />
              </n-a>
            </div>
          </template>
          <div class="course-content">
            <n-p class="course-teacher"> 
              <strong>Teacher:</strong> {{ course.teacher.display_name }} 
            </n-p>
            <n-p class="course-description"> 
              <strong>Description:</strong> {{ course.description }} 
            </n-p>
          </div>
          <template #footer>
            <!-- Purchase button for non-enrolled users -->
            <n-space
              justify="space-between"
              align="center"
              class="course-footer"
              v-if="!isEnrolledCourse(course.id)"
            >
              <span class="course-price">
                ${{ course.original_price }}
              </span>
              <n-button
                size="small"
                type="success"
                class="purchase-button"
                @click="() => clickPurchase(course.id)"
                >Purchase now</n-button
              >
            </n-space>
            
            <!-- Enrolled status for regular users -->
            <n-space 
              v-else-if="isEnrolledCourse(course.id) && !isAdmin"
              class="course-footer" 
              align="center"
            >
              <span class="enrolled-status">
                Enrolled
              </span>
            </n-space>
            
            <!-- Admin actions -->
            <n-space 
              v-else-if="isAdmin"
              justify="space-between" 
              align="center"
              class="course-footer"
            >
              <!-- Left side shows enrollment count -->
              <span class="enrolled-status">
                Admin
              </span>
              
              <!-- Right side shows admin actions -->
              <n-space>
                <update-course-button
                  :course="course"
                  :onUpdated="handleCourseUpdated"
                />
                
                <n-popconfirm
                  positive-text="Yes"
                  negative-text="No"
                  @positive-click="() => handleDeleteCourse(course.id)"
                >
                  <template #trigger>
                    <n-button 
                      size="small" 
                      type="error" 
                      :loading="deletingCourses.get(course.id)"
                      class="delete-button"
                    >
                      Delete Course
                    </n-button>
                  </template>
                  <template #default>
                    <div style="max-width: 280px">
                      <p>Are you sure you want to delete this course?</p>
                      <p style="margin-top: 8px; font-weight: bold">This will permanently delete:</p>
                      <ul style="padding-left: 16px; margin-top: 8px">
                        <li>The course information</li>
                        <li>All associated lectures</li>
                        <li>All uploaded files</li>
                        <li>All student enrollments</li>
                      </ul>
                      <p style="margin-top: 8px"><strong>This action cannot be undone!</strong></p>
                    </div>
                  </template>
                </n-popconfirm>
              </n-space>
            </n-space>
          </template>
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
  <n-modal
    v-model:show="showPurchaseModal"
    preset="dialog"
    title="Purchase Course"
    content="Do you want to purchase this course?"
    positive-text="Place Order"
    negative-text="Cancel"
    @positive-click="purchase"
  ></n-modal>
</template>

<style scoped>
.course-list-container {
  padding: 16px;
  max-width: 1400px;
  margin: 0 auto;
}

.course-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s, box-shadow 0.2s;
}

.course-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.course-image-container {
  position: relative;
  overflow: hidden;
  border-radius: 3px;
  height: 200px;
}

.course-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.course-link {
  display: block;
  height: 100%;
  cursor: pointer;
}

.course-link:hover .course-image {
  transform: scale(1.05);
}

.course-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 8px 0;
}

.course-teacher {
  margin-bottom: 8px;
  font-size: 0.95rem;
}

.course-description {
  margin-top: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.9rem;
  color: rgba(255, 252, 252, 0.7);
}

.course-footer {
  min-height: 40px;
  padding-top: 8px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.course-price {
  font-weight: bold;
  color: #ff7a45;
  font-size: 1.15rem;
}

.purchase-button {
  font-weight: 500;
}

.enrolled-status {
  font-weight: 500;
  color: #52c41a;
}

.delete-button {
  font-weight: 500;
}

/* Ensure text doesn't overflow on small screens */
@media (max-width: 768px) {
  .course-image-container {
    height: 180px;
  }
  
  .course-description {
    -webkit-line-clamp: 2;
  }
}
</style>
