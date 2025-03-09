<script setup lang="ts">
import { useCourseList } from "@/api/course";
import CourseList from "@/components/CourseList.vue";
import { useAuthStore } from "@/stores/auth";
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();
const isAdmin = computed(() => authStore.hasPermission('course_admin'));

// Redirect admin users to browse page since it's the same content
onMounted(() => {
  if (isAdmin.value) {
    router.replace('/browse');
  }
});

const { data: courseList, isLoading, execute: refreshCourseList } = useCourseList();

const handleRefresh = () => {
  refreshCourseList();
};
</script>
<template>
  <div>
    <course-list
      :user-info="authStore.getUserInfo!"
      :courses="courseList!"
      v-if="!isLoading"
      @refresh="handleRefresh"
    ></course-list>
  </div>
</template>

