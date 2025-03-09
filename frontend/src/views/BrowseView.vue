<script setup lang="ts">
import CourseList from "@/components/CourseList.vue";
import CourseControlPanel from "@/components/CourseControlPanel.vue";
import { useCourseStore } from "@/stores/course";
import { storeToRefs } from "pinia";
import { useAuthStore } from "@/stores/auth";
import { ref, computed } from "vue";
import type { CourseBasicInfo } from "@/api/course";
import { NSpin } from "naive-ui";
import type { User } from "@/interfaces/user.interface";

const courseStore = useCourseStore();
const authStore = useAuthStore();
const { allCourses, isLoading } = storeToRefs(courseStore);
const { userInfo } = storeToRefs(authStore);

// Ensure we have user info before rendering
const isUserReady = computed(() => !!userInfo.value);

// Access user info with type assertion
const userInfoTyped = computed(() => userInfo.value as User);

// Filter state
const searchQuery = ref("");
const sortBy = ref("newest");

// Handle refreshing the course list
const handleRefresh = () => {
  courseStore.refreshCourses();
};

// Filter and sort courses based on user selections
const filteredCourses = computed(() => {
  if (!allCourses.value) return [];

  if (authStore.isTeacher) {
    allCourses.value = allCourses.value.filter(course => course.teacher.id === userInfo.value?.id);
  }
  let filtered = [...allCourses.value];
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      course => 
        course.name.toLowerCase().includes(query) || 
        (course.description && course.description.toLowerCase().includes(query))
    );
  }
  
  // Apply sorting
  if (sortBy.value === "newest") {
    filtered.sort((a, b) => new Date(b.created_time).getTime() - new Date(a.created_time).getTime());
  } else if (sortBy.value === "oldest") {
    filtered.sort((a, b) => new Date(a.created_time).getTime() - new Date(b.created_time).getTime());
  } else if (sortBy.value === "alphabetical") {
    filtered.sort((a, b) => a.name.localeCompare(b.name));
  }
  
  return filtered;
});
</script>

<template>
  <div class="browse-view">    
    <CourseControlPanel 
      v-model:search="searchQuery"
      v-model:sort="sortBy"
      @refresh="handleRefresh"
    />
    
    <CourseList
      v-if="isUserReady"
      :userInfo="userInfoTyped"
      :courses="filteredCourses"
      :loading="isLoading"
      @refresh="handleRefresh"
    />
    <NSpin v-else size="large" />
  </div>
</template>
