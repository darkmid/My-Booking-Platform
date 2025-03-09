<script setup lang="ts">
import CourseList from "../components/CourseList.vue";
import { useCourseList } from "../api/course";
import { useAuthStore } from "@/stores/auth";
import CourseControlPanel from "@/components/CourseControlPanel.vue";
import { NCard, NTabs, NTabPane } from 'naive-ui';

const { data: courseList, isLoading, execute: refreshCourseList } = useCourseList();
const authStore = useAuthStore();

const handleRefresh = () => {
  refreshCourseList();
};
</script>
<template>
  <CourseControlPanel />
  <div v-if="!authStore.isTeacher">
    <course-list
      :user-info="authStore.getUserInfo!"
      :courses="isLoading ? [] : courseList!"
      @refresh="handleRefresh"
    ></course-list>
  </div>
  <div v-else>
    <course-list
      :user-info="authStore.getUserInfo!"
      :courses="isLoading ? [] : courseList!.filter(course => course.teacher.id === authStore.getUserInfo!.id)"
    ></course-list>
  </div>

</template>
