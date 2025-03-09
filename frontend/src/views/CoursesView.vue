<script setup lang="ts">
import { useCourseList } from "@/api/course";
import CourseList from "@/components/CourseList.vue";
import { useAuthStore } from "@/stores/auth";
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { NCard, NTabs, NTabPane } from 'naive-ui';
const authStore = useAuthStore();
const router = useRouter();
const isAdmin = computed(() => authStore.hasPermission('course_admin'));
const isTeacher = computed(() => authStore.isTeacher);

// Redirect admin users to browse page since it's the same content
onMounted(() => {
  if (isAdmin.value || isTeacher.value) {
    router.replace('/browse');
  }
});

const { data: courseList, isLoading, execute: refreshCourseList } = useCourseList();

const handleRefresh = () => {
  refreshCourseList();
};
</script>
<template>
  <div v-if="!isTeacher">
    <course-list
      :user-info="authStore.getUserInfo!"
      :courses="courseList!.filter(course => authStore.getUserInfo!.enrolled_courses!.map(c => c.id).includes(course.id))"
      v-if="!isLoading"
      @refresh="handleRefresh"
    ></course-list>
  </div>
  
</template>

