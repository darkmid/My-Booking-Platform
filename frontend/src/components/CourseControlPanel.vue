<template>
  <div class="course-control-panel p-4 mb-4 rounded-lg bg-gray-800">
    <!-- Admin Controls -->
    <div v-if="isAdmin" class="admin-controls mb-4">
      <h2 class="text-xl font-bold mb-2">Course Administration</h2>
      <p class="text-sm text-gray-400 mb-4">Create and manage courses for your platform.</p>
      <div class="flex flex-wrap gap-2">
        <NewCourseButton :on-created="handleRefresh" />
      </div>
    </div>
    
    <!-- Search and Filters -->
    <div class="filters">
      <n-space vertical>
        <n-input 
          v-model:value="searchValue" 
          placeholder="Search courses..." 
          clearable
          @update:value="emitSearchUpdate"
        >
          <template #prefix>
            <n-icon><SearchOutline /></n-icon>
          </template>
        </n-input>
        
        <n-space justify="space-between">
          <n-select
            v-model:value="sortValue"
            placeholder="Sort by"
            :options="sortOptions"
            @update:value="emitSortUpdate"
          />
          
          <n-button @click="handleRefresh" type="primary">
            <template #icon>
              <n-icon><RefreshOutline /></n-icon>
            </template>
            Refresh
          </n-button>
        </n-space>
      </n-space>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/stores/auth";
import { useTeacherStore } from "@/stores/teacher";
import { ref, watch } from "vue";
import NewCourseButton from "@/components/course/NewCourseButton.vue";
import { NSpace, NInput, NSelect, NButton, NIcon } from "naive-ui";
import { RefreshOutline, SearchOutline } from "@vicons/ionicons5";

const props = defineProps<{
  search?: string;
  sort?: string;
}>();

const emit = defineEmits([
  'update:search', 
  'update:sort', 
  'refresh'
]);

const authStore = useAuthStore();
const teacherStore = useTeacherStore();
const isAdmin = authStore.hasPermission('course_admin');

// Local state synced with parent component
const searchValue = ref(props.search || '');
const sortValue = ref(props.sort || 'newest');

// Watch prop changes to update local state
watch(() => props.search, (newVal) => {
  if (newVal !== undefined) searchValue.value = newVal;
});

watch(() => props.sort, (newVal) => {
  if (newVal !== undefined) sortValue.value = newVal;
});

// Emit updates to parent component
const emitSearchUpdate = (value: string) => {
  emit('update:search', value);
};

const emitSortUpdate = (value: string) => {
  emit('update:sort', value);
};

// Handle refresh button click
const handleRefresh = () => {
  emit('refresh');
};

// Sort options
const sortOptions = [
  { label: 'Newest', value: 'newest' },
  { label: 'Oldest', value: 'oldest' },
  { label: 'Alphabetical', value: 'alphabetical' }
];

// Pre-fetch teacher data for the dropdown
if (isAdmin) {
  teacherStore.fetchTeachers();
}
</script>

<style scoped>
.course-control-panel {
  border: 1px solid #333;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
