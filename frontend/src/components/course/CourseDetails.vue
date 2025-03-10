<script lang="ts" setup>
import type { Course } from "@/api/course";
import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { computed } from "vue";
import {
  NCard,
  NSpace,
  NH3,
  NP,
  NImage,
  NTag,
  NIcon,
  NDivider,
} from "naive-ui";
import { People } from "@vicons/ionicons5";

// Define the default course image path
const defaultCourseImage = '/course_wrap.png';

// Standard dimensions for course images (matching the ImageUploader)
const STANDARD_WIDTH = 800;
const STANDARD_HEIGHT = 450; // 16:9 aspect ratio

const props = defineProps<{
  course: Course;
}>();
const authStore = useAuthStore();
const auth = storeToRefs(authStore);
</script>
<template>
  <n-card>
    <div class="course-detail-container">
      <div class="course-image-wrapper">
        <n-image
          class="course-cover-image"
          :src="props.course.cover_image || defaultCourseImage"
          :width="400"
          :height="225"
          object-fit="cover"
          preview-disabled
        />
      </div>
      <n-space vertical class="course-info">
        <n-h3>{{ props.course.name }}</n-h3>
        <n-space>
          <n-p>
            Price: <span> ${{ props.course.original_price }}</span>
          </n-p>
          <n-p>
            Teacher: <span> {{ props.course.teacher.display_name }}</span>
          </n-p>
          <n-p>
            Campus: <span> {{ props.course.campus.name }}</span>
          </n-p>
        </n-space>
        <n-tag type="success" round :bordered="false" class="mt-2">
          Enrolled: {{ props.course.enrolled_students.length }}
          <template #icon>
            <n-icon :component="People" class="mr-1"></n-icon>
          </template>
        </n-tag>
        <n-divider></n-divider>
        <n-p class="course-description"> {{ props.course.description }}</n-p>
      </n-space>
    </div>
  </n-card>
</template>

<style lang="less" scoped>
.course-detail-container {
  display: flex;
  flex-direction: row;
  gap: 24px;
  
  @media (max-width: 768px) {
    flex-direction: column;
  }
}

.course-image-wrapper {
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
}

.course-cover-image {
  display: block;
  transition: transform 0.3s ease;
  
  &:hover {
    transform: scale(1.03);
  }
}

.course-info {
  flex: 1;
  
  span {
    font-size: 16px;
    font-weight: 400;
    margin-left: 10px;
    margin-right: 16px;
  }
}

.course-description {
  font-size: 16px;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.8);
}

.mr-1 {
  margin-right: 4px;
}

.mt-2 {
  margin-top: 8px;
}
</style>
