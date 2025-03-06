<script lang="ts" setup>
import { ref } from "vue";
import {
  NUpload,
  NUploadDragger,
  NImage,
  NText,
  NIcon,
  NButton,
  useMessage,
  type UploadCustomRequestOptions,
} from "naive-ui";
import { CloudUpload } from "@vicons/ionicons5";

const props = defineProps<{
  initialImageUrl?: string; // Initial image URL if editing
  maxSize?: number; // Max file size in MB, default 5MB
}>();

const emits = defineEmits<{
  (e: "uploaded", url: string): void;
  (e: "reset"): void;
}>();

const message = useMessage();
const previewUrl = ref(props.initialImageUrl || "");

// Reset the component
const resetUpload = () => {
  previewUrl.value = "";
  emits("reset");
};

// Handle upload error
const handleUploadError = () => {
  message.error("Upload failed. Please try again.");
};

// Create custom request function
const handleUpload = ({ file }: UploadCustomRequestOptions) => {
  // This is where you would normally send the file to your server
  // For now, we'll use FileReader to display a local preview
  console.log("handleUpload", file.file);
  
  // Create a FileReader to read the image as a data URL (base64)
  const reader = new FileReader();
  reader.readAsDataURL(file.file!);
  
  // When the file is loaded, set the preview and emit the event
  reader.onload = (e) => {
    if (e.target?.result) {
      const base64 = e.target.result as string;
      console.log("Image converted to base64", base64);
      
      // Set the preview
      previewUrl.value = base64;
      // Emit the uploaded event with the base64 URL
      // In a real app, you would upload to a server and get a real URL back
      emits("uploaded", base64.split(",")[1]);
    } else {
      message.error("Failed to read the image file");
    }
  };
  
  reader.onerror = () => {
    message.error("Error reading the image file");
  };
  
  // Return a function to abort the upload (if needed)
  return () => {
    reader.abort();
  };
};
</script>

<template>
  <div class="image-uploader">
    <!-- Image preview area -->
    <div v-if="previewUrl" class="preview-container">
      <n-image
        :src="previewUrl"
        object-fit="cover"
        width="150"
        height="150"
        :preview-disabled="true"
      />
      <n-button size="small" type="error" class="mt-2" @click="resetUpload">
        Remove
      </n-button>
    </div>
    
    <!-- Upload area -->
    <n-upload
      v-if="!previewUrl"
      accept="image/*"
      :max-size="(props.maxSize || 5) * 1024 * 1024"
      :custom-request="handleUpload"
      @error="handleUploadError"
    >
      <n-upload-dragger class="upload-area">
        <div class="flex flex-col items-center justify-center p-4">
          <n-icon size="40" :depth="3">
            <cloud-upload />
          </n-icon>
          <n-text style="margin-top: 8px; font-size: 14px;">
            Click to select image
          </n-text>
          <n-text depth="3" style="margin-top: 4px; font-size: 12px;">
            JPG, PNG, GIF under {{ props.maxSize || 5 }}MB
          </n-text>
        </div>
      </n-upload-dragger>
    </n-upload>
  </div>
</template>

<style scoped>
.image-uploader {
  width: 100%;
  max-width: 200px;
  margin: 0 auto;
}

.preview-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #444;
  padding: 8px;
  border-radius: 4px;
}

.upload-area {
  cursor: pointer;
  position: relative;
  overflow: hidden;
  height: 150px;
  border: 1px dashed #444;
}
</style> 