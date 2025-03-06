<script setup lang="ts">
import { useCourseList } from "@/api/course";
import CourseList from "@/components/CourseList.vue";
import { useAuthStore } from "@/stores/auth";
import CourseControlPanel from '@/components/CourseControlPanel.vue';
import { ref } from 'vue';

const authStore = useAuthStore();
const { data: courseList, isLoading, execute: refreshCourseList } = useCourseList();

const handleRefresh = () => {
  refreshCourseList();
};
</script>
<template>
  <div>
    <CourseControlPanel />
    <course-list
      :user-info="authStore.getUserInfo!"
      :courses="courseList!"
      v-if="!isLoading"
      @refresh="handleRefresh"
    ></course-list>
  </div>
</template>

