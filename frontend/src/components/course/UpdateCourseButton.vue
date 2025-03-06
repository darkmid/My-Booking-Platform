<script lang="ts" setup>
import axios from "@/utils/http";
import { updateCourse, type CourseUpdateData, type CourseBasicInfo } from "@/api/course";
import {
  NButton,
  NModal,
  NCard,
  NForm,
  NFormItem,
  NInput,
  NSpace,
  NInputNumber,
  NSelect,
  NDivider,
  type FormItemRule,
  type FormRules,
  type FormInst,
  useMessage
} from "naive-ui";
import { ref, onMounted, computed } from "vue";
import { useCampusStore } from "@/stores/auth";
import { useTeacherStore } from "@/stores/teacher";
import type { Campus, Teacher } from "@/api/course";
import ImageUploader from "@/components/common/ImageUploader.vue";

const props = defineProps<{
  course: CourseBasicInfo;
  onUpdated: () => void;
}>();

const updateCourseFormRef = ref<FormInst | null>(null);
const updateCourseForm = ref<CourseUpdateData>({
  name: "",
  description: "",
  teacher: "",
  original_price: 0,
});

// Loading states for individual actions
const isUpdatingCourse = ref(false);
const showFormStep = ref(true);
const showImageStep = ref(false);

// Get campus and teacher stores
const teacherStore = useTeacherStore();
const message = useMessage();

// Options for select dropdowns
const teacherOptions = ref<{ label: string; value: string }[]>([]);

// Fetch teacher data
onMounted(async () => {
  // Load course data into form
  updateCourseForm.value = {
    name: props.course.name,
    description: props.course.description,
    teacher: props.course.teacher.id,
    original_price: props.course.original_price,
  };

  // Fetch teacher data if not already loaded
  await teacherStore.fetchTeachers();
  if (teacherStore.getTeacherList) {
    teacherOptions.value = teacherStore.getTeacherList.map((teacher: Teacher) => ({
      label: teacher.display_name,
      value: teacher.id,
    }));
  }
});

// Original image URL for preview
const originalImageUrl = computed(() => {
  return props.course.cover_image;
});

// Handler for when the cover image is uploaded
const handleCoverImageUploaded = (base64: string) => {
  updateCourseForm.value.cover_image = base64;
};

const handleCoverImageReset = () => {
  updateCourseForm.value.cover_image = "";
};

// Update the course
const submitCourseUpdate = async () => {
  try {
    isUpdatingCourse.value = true;
    await updateCourse(props.course.id, updateCourseForm.value);
    
    // Close the modal
    showUpdateCourseModal.value = false;
    
    // Notify parent component
    message.success("Course updated successfully");
    props.onUpdated();
  } catch (error) {
    console.error('Error updating course:', error);
    message.error("Failed to update course");
  } finally {
    isUpdatingCourse.value = false;
  }
};

// Move to the image upload step
const switchToImageStep = async () => {
  try {
    if (updateCourseFormRef.value) {
      const isValid = await updateCourseFormRef.value.validate();
      if (isValid) {
        showFormStep.value = false;
        showImageStep.value = true;
      }
    } else {
      console.error("Form reference is not available");
    }
  } catch (error) {
    console.error("Validation error:", error);
  }
};

// Go back to the course info step
const switchToFormStep = () => {
  showFormStep.value = true;
  showImageStep.value = false;
};

// Form validation rules
const rules: FormRules = {
  name: [
    {
      required: true,
      message: "Course name is required",
      trigger: ["blur", "change"]
    },
    {
      min: 3,
      message: "Course name must be at least 3 characters",
      trigger: ["blur", "change"]
    }
  ],
  description: [
    {
      required: true,
      message: "Description is required",
      trigger: ["blur", "change"]
    }
  ],
  teacher: [
    {
      required: true,
      message: "Please select a teacher for this course",
      trigger: ["blur", "change"]
    }
  ],
  original_price: [
    {
      validator: (_rule: FormItemRule, value: number) => {
        return value >= 0;
      },
      message: "Price must be a non-negative number",
      trigger: ["blur", "change"]
    }
  ]
};

const showUpdateCourseModal = ref(false);
</script>

<template>
  <n-button size="small" type="info" @click="showUpdateCourseModal = true">
    Edit Course
  </n-button>
  
  <n-modal v-model:show="showUpdateCourseModal" style="width: 500px">
    <n-card
      style="width: 500px; margin: 0 auto"
      title="Update Course"
      :bordered="false"
      size="huge"
    >
      <!-- Step 1: Basic Course Info -->
      <div v-show="showFormStep">
        <n-form
          ref="updateCourseFormRef"
          :model="updateCourseForm"
          :rules="rules"
          label-placement="left"
          label-width="auto"
        >
          <n-form-item label="Course Name" path="name">
            <n-input v-model:value="updateCourseForm.name"></n-input>
          </n-form-item>
          <n-form-item label="Description" path="description">
            <n-input 
              v-model:value="updateCourseForm.description"
              type="textarea"
            ></n-input>
          </n-form-item>
          <n-form-item label="Teacher" path="teacher">
            <n-select
              v-model:value="updateCourseForm.teacher"
              :options="teacherOptions"
              placeholder="Select a teacher"
              filterable
            />
          </n-form-item>
          <n-form-item label="Original Price" path="original_price">
            <n-input-number 
              v-model:value="updateCourseForm.original_price"
              :min="0"
              :default-value="0"
            ></n-input-number>
          </n-form-item>
        </n-form>
        <n-space justify="end" class="mt-4">
          <n-button type="primary" @click="switchToImageStep">Next</n-button>
          <n-button @click="showUpdateCourseModal = false">Cancel</n-button>
        </n-space>
      </div>
      
      <!-- Step 2: Upload Cover Image -->
      <div v-show="showImageStep">
        <h3 class="text-lg font-bold mb-4">Update Course Cover Image</h3>
        <p class="mb-4">Update the cover image for your course (optional).</p>
        
        <image-uploader 
          :initialImageUrl="originalImageUrl" 
          @uploaded="handleCoverImageUploaded" 
          @reset="handleCoverImageReset"
        />
        
        <n-space justify="end" class="mt-4">
          <n-button @click="switchToFormStep">Previous</n-button>
          <n-button 
            type="primary" 
            @click="submitCourseUpdate" 
            :loading="isUpdatingCourse"
          >
            Update Course
          </n-button>
        </n-space>
      </div>
    </n-card>
  </n-modal>
</template>

<style scoped>
.mt-4 {
  margin-top: 16px;
}
.text-lg {
  font-size: 1.125rem;
}
.font-bold {
  font-weight: 700;
}
.mb-4 {
  margin-bottom: 16px;
}
</style> 