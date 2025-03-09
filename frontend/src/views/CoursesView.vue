<script setup lang="ts">
import CourseList from "@/components/CourseList.vue";
import { useCourseStore } from "@/stores/course";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

import { NSpin, NSpace, NTabs, NTabPane } from "naive-ui";
import { onMounted, computed } from "vue";
import type { User } from "@/interfaces/user.interface";

const courseStore = useCourseStore();
const authStore = useAuthStore();
const router = useRouter();
const isAdmin = computed(() => authStore.hasPermission("course_admin"));

const { allCourses, isLoading } = storeToRefs(courseStore);
const { userInfo } = storeToRefs(authStore);

// Redirect admin users to browse page since it's the same content
onMounted(() => {
  if (!authStore.isStudent) {
    router.replace("/browse");
  }
});

// Ensure we have user info before rendering
const isUserReady = computed(() => !!userInfo.value);

// Access user info with type assertion
const userInfoTyped = computed(() => userInfo.value as User);

// Get courses based on user type
const teacherCourses = computed(() => {
  if (!allCourses.value || !userInfo.value) return [];

  return allCourses.value.filter(
    (course) => course.teacher.id === userInfo.value?.id
  );
});

const studentCourses = computed(() => {
  if (!allCourses.value || !userInfo.value) return [];

  return allCourses.value.filter((course) =>
    userInfo.value?.enrolled_courses?.some(
      (enrolledCourse) => enrolledCourse.id === course.id
    )
  );
});

// Handle refreshing the course list
const handleRefresh = () => {
  courseStore.refreshCourses();
};

onMounted(async () => {
  await courseStore.fetchCourses();
});
</script>

<template>
  <div class="courses-view">
    <div v-if="isUserReady">
      <n-space vertical size="large">
        <CourseList
          v-if="authStore.isStudent"
          :userInfo="userInfoTyped"
          :courses="studentCourses"
          :loading="isLoading"
          @refresh="handleRefresh"
        />

        <CourseList
          v-if="authStore.isTeacher"
          :userInfo="userInfoTyped"
          :courses="teacherCourses"
          :loading="isLoading"
          @refresh="handleRefresh"
        />
      </n-space>
    </div>
    <NSpin v-else size="large" />
  </div>
</template>

<style scoped>
.courses-view {
  padding: 1rem 0;
}

.section-title {
  margin: 1.5rem 0;
  font-size: 1.25rem;
  color: var(--text-color-base);
}
</style>
