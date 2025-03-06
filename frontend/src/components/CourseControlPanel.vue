<template>
  <div v-if="isAdmin" class="course-control-panel p-4 mb-4 rounded-lg bg-gray-800">
    <h2 class="text-xl font-bold mb-4">Course Administration</h2>
    <p class="text-sm text-gray-400 mb-4">Create and manage courses for your platform.</p>
    <div class="flex flex-wrap gap-2">
      <NewCourseButton :on-created="refreshCourseList" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { useTeacherStore } from "@/stores/teacher";
import { onMounted } from "vue";
import NewCourseButton from "@/components/course/NewCourseButton.vue";

const authStore = useAuthStore();
const teacherStore = useTeacherStore();
const isAdmin = authStore.hasPermission('course_admin');

// Pre-fetch teacher data for the dropdown
onMounted(() => {
  if (isAdmin) {
    teacherStore.fetchTeachers();
  }
});

const refreshCourseList = () => {
  // This function will be called after a new course is created
  // It should trigger a refresh of the course list in the parent component
  window.location.reload(); // Simplest approach for now
};
</script>

<style scoped>
.course-control-panel {
  border: 1px solid #333;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
