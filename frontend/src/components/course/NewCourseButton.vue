<script lang="ts" setup>
import axios from "@/utils/http";
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
  type FormRules
} from "naive-ui";
import { ref, onMounted } from "vue";
import { useCampusStore } from "@/stores/auth";
import { useTeacherStore } from "@/stores/teacher";
import type { Campus, Teacher } from "@/api/course";
import ImageUploader from "@/components/common/ImageUploader.vue";
interface CourseForm {
  name: string;
  uni_course_code: string;
  description: string;
  teacher: string;
  campus: string;
  original_price: number | null;
  cover_image?: string;
}

const newCourseFormRef = ref(null);
const newCourseForm = ref<CourseForm>({
  name: "course1",
  uni_course_code: "course1",
  description: "course1",
  teacher: "",
  campus: "",
  original_price: 0,
});

const isCreatingCourse = ref(false);
// Whether to show the image uploader step
const courseBaseInfoFilled = ref(false);

// Get campus and teacher stores
const campusStore = useCampusStore();
const teacherStore = useTeacherStore();

// Options for select dropdowns
const campusOptions = ref<{ label: string; value: string }[]>([]);
const teacherOptions = ref<{ label: string; value: string }[]>([]);

// Fetch campus and teacher data
onMounted(async () => {
  // Fetch campus data if not already loaded
  await campusStore.fetchCampus();
  if (campusStore.getCampusList) {
    campusOptions.value = campusStore.getCampusList.map((campus: Campus) => ({
      label: campus.name,
      value: campus.id,
    }));
  }

  // Fetch teacher data
  await teacherStore.fetchTeachers();
  if (teacherStore.getTeacherList) {
    teacherOptions.value = teacherStore.getTeacherList.map((teacher: Teacher) => ({
      label: teacher.display_name,
      value: teacher.id,
    }));
  }
});

const props = defineProps<{
  onCreated: () => void;
}>();

// Handler for when the cover image is uploaded
const handleCoverImageUploaded = (base64: string) => {
  newCourseForm.value.cover_image = base64;
};

// Create a new course
const createNewCourse = async () => {
  try {
    isCreatingCourse.value = true;
    
    // Ensure original_price is a number and not null when submitting
    const formData = {
      ...newCourseForm.value,
      original_price: newCourseForm.value.original_price || 0
    };
    
    // Send the course data to the API
    const response = await axios.post('/courses', formData);    
    // Close the modal
    showNewCourseModal.value = false;
    
    // Reset form
    resetForm();
    
    // Notify parent component
    props.onCreated();
  } catch (error) {
    console.error('Error creating course:', error);
  } finally {
    isCreatingCourse.value = false;
  }
};

// Move to the image upload step
const switchToNextStep = async () => {
  const isValid = await newCourseFormRef.value?.validate();
  if (isValid) {
    courseBaseInfoFilled.value = true;
  }
};

// Go back to the course info step
const switchToPrevStep = () => {
  courseBaseInfoFilled.value = false;
};

// Reset the form to its initial state
const resetForm = () => {
  newCourseForm.value = {
    name: "",
    uni_course_code: "",
    description: "",
    teacher: "",
    campus: "",
    original_price: 0,
  };
  courseBaseInfoFilled.value = false;
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
  uni_course_code: [
    {
      required: true,
      message: "Course code is required",
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
    },
    {
      validator: (_rule: FormItemRule, value: string) => {
        return !!value && value.length > 0;
      },
      message: "A valid teacher must be selected",
      trigger: ["blur", "change"]
    }
  ],
  campus: [
    {
      required: true,
      message: "Please select a campus for this course",
      trigger: ["blur", "change"]
    },
    {
      validator: (_rule: FormItemRule, value: string) => {
        return !!value && value.length > 0;
      },
      message: "A valid campus must be selected",
      trigger: ["blur", "change"]
    }
  ],
  original_price: [
    {
      validator: (_rule: FormItemRule, value: number | null) => {
        return value !== null && value >= 0;
      },
      message: "Price must be a non-negative number",
      trigger: ["blur", "change"]
    }
  ]
};

const showNewCourseModal = ref(false);
</script>

<template>
  <n-button type="primary" @click="showNewCourseModal = true"
    >Add New Course</n-button
  >
  <n-modal v-model:show="showNewCourseModal" style="width: 500px">
    <n-card
      style="width: 500px; margin: 0 auto"
      title="Add New Course"
      :bordered="false"
      size="huge"
    >
      <!-- Step 1: Basic Course Info -->
      <div v-show="!courseBaseInfoFilled">
        <n-form
          ref="newCourseFormRef"
          :model="newCourseForm"
          :rules="rules"
          label-placement="left"
          label-width="auto"
        >
          <n-form-item label="Course Name" path="name">
            <n-input v-model:value="newCourseForm.name"></n-input>
          </n-form-item>
          <n-form-item label="Course Code" path="uni_course_code">
            <n-input v-model:value="newCourseForm.uni_course_code"></n-input>
          </n-form-item>
          <n-form-item label="Description" path="description">
            <n-input 
              v-model:value="newCourseForm.description"
              type="textarea"
            ></n-input>
          </n-form-item>
          <n-form-item label="Teacher" path="teacher">
            <n-select
              v-model:value="newCourseForm.teacher"
              :options="teacherOptions"
              placeholder="Select a teacher"
              filterable
            />
          </n-form-item>
          <n-form-item label="Campus" path="campus">
            <n-select
              v-model:value="newCourseForm.campus"
              :options="campusOptions"
              placeholder="Select a campus"
              filterable
            />
          </n-form-item>
          <n-form-item label="Original Price" path="original_price">
            <n-input-number 
              v-model:value="newCourseForm.original_price"
              :min="0"
            ></n-input-number>
          </n-form-item>
        </n-form>
        <n-space justify="end" class="mt-4">
          <n-button type="primary" @click="switchToNextStep">Next</n-button>
          <n-button @click="showNewCourseModal = false">Cancel</n-button>
        </n-space>
      </div>
      
      <!-- Step 2: Upload Cover Image -->
      <div v-show="courseBaseInfoFilled">
        <h3 class="text-lg font-bold mb-4">Upload Course Cover Image</h3>
        <p class="mb-4">Please upload a cover image for your course (optional).</p>
        
        <image-uploader @uploaded="handleCoverImageUploaded" />
        
        <n-space justify="end" class="mt-4">
          <n-button @click="switchToPrevStep">Previous</n-button>
          <n-button 
            type="primary" 
            @click="createNewCourse" 
            :loading="isCreatingCourse"
          >
            {{ newCourseForm.cover_image ? 'Create Course' : 'Create Without Image' }}
          </n-button>
        </n-space>
      </div>
    </n-card>
  </n-modal>
</template> 