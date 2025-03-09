<script lang="ts" setup>
import { ref, onMounted } from "vue";
import {
  NUpload,
  NUploadDragger,
  NImage,
  NText,
  NIcon,
  NButton,
  NSpace,
  NTag,
  useMessage,
  type UploadCustomRequestOptions,
} from "naive-ui";
import { CloudUpload, Resize } from "@vicons/ionicons5";

// Define standard dimensions for cover images
const STANDARD_WIDTH = 800;
const STANDARD_HEIGHT = 450; // 16:9 aspect ratio
const STANDARD_FORMAT = 'image/jpeg';
const STANDARD_QUALITY = 0.85;

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
const isResizing = ref(false);
const originalImageSize = ref('');
const standardizedImageSize = ref('');

// Reset the component
const resetUpload = () => {
  previewUrl.value = "";
  originalImageSize.value = "";
  standardizedImageSize.value = "";
  emits("reset");
};

// Handle upload error
const handleUploadError = () => {
  message.error("Upload failed. Please try again.");
};

// Convert file size to human-readable format
const formatFileSize = (size: number): string => {
  if (size < 1024) return size + ' B';
  if (size < 1024 * 1024) return (size / 1024).toFixed(1) + ' KB';
  return (size / (1024 * 1024)).toFixed(2) + ' MB';
};

// Resize image to standard dimensions
const resizeImage = (dataUrl: string): Promise<string> => {
  return new Promise((resolve, reject) => {
    isResizing.value = true;
    const img = new Image();
    img.onload = () => {
      // Create canvas with standard dimensions
      const canvas = document.createElement('canvas');
      canvas.width = STANDARD_WIDTH;
      canvas.height = STANDARD_HEIGHT;
      const ctx = canvas.getContext('2d');
      
      if (!ctx) {
        isResizing.value = false;
        return reject('Canvas context not available');
      }
      
      // Fill canvas with white background (for transparent PNGs)
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, STANDARD_WIDTH, STANDARD_HEIGHT);
      
      // Calculate aspect ratio
      const sourceWidth = img.width;
      const sourceHeight = img.height;
      const sourceRatio = sourceWidth / sourceHeight;
      const targetRatio = STANDARD_WIDTH / STANDARD_HEIGHT;
      
      let drawWidth, drawHeight, offsetX = 0, offsetY = 0;
      
      // Determine dimensions to maintain aspect ratio with center crop
      if (sourceRatio > targetRatio) {
        // Source is wider than target, crop sides
        drawHeight = STANDARD_HEIGHT;
        drawWidth = sourceWidth * (STANDARD_HEIGHT / sourceHeight);
        offsetX = (STANDARD_WIDTH - drawWidth) / 2;
      } else {
        // Source is taller than target, crop top/bottom
        drawWidth = STANDARD_WIDTH;
        drawHeight = sourceHeight * (STANDARD_WIDTH / sourceWidth);
        offsetY = (STANDARD_HEIGHT - drawHeight) / 2;
      }
      
      // Draw image on canvas with calculated dimensions
      ctx.drawImage(img, offsetX, offsetY, drawWidth, drawHeight);
      
      // Convert canvas to data URL
      const resizedDataUrl = canvas.toDataURL(STANDARD_FORMAT, STANDARD_QUALITY);
      
      // Calculate and store sizes for display
      const originalSize = dataUrl.length * 0.75; // Rough approximation for base64
      originalImageSize.value = formatFileSize(originalSize);
      
      const standardizedSize = resizedDataUrl.length * 0.75;
      standardizedImageSize.value = formatFileSize(standardizedSize);
      
      isResizing.value = false;
      resolve(resizedDataUrl);
    };
    
    img.onerror = () => {
      isResizing.value = false;
      reject('Error loading image for resizing');
    };
    
    img.src = dataUrl;
  });
};

// Create custom request function
const handleUpload = ({ file }: UploadCustomRequestOptions) => {
  // This is where you would normally send the file to your server
  // For now, we'll use FileReader to display a local preview
  console.log("handleUpload", file.file);
  
  // Create a FileReader to read the image as a data URL (base64)
  const reader = new FileReader();
  reader.readAsDataURL(file.file!);
  
  // When the file is loaded, resize and emit
  reader.onload = async (e) => {
    if (e.target?.result) {
      const originalBase64 = e.target.result as string;
      
      try {
        // Resize the image to standard dimensions
        const resizedBase64 = await resizeImage(originalBase64);
        
        // Set the preview with resized image
        previewUrl.value = resizedBase64;
        
        // Emit the uploaded event with the resized base64 data
        emits("uploaded", resizedBase64.split(",")[1]);
        
        message.success(`Image standardized to ${STANDARD_WIDTH}x${STANDARD_HEIGHT}`);
      } catch (error) {
        console.error("Error resizing image:", error);
        message.error("Failed to standardize image. Using original instead.");
        
        // Use original as fallback
        previewUrl.value = originalBase64;
        emits("uploaded", originalBase64.split(",")[1]);
      }
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
      <n-space vertical align="center">
        <n-image
          :src="previewUrl"
          object-fit="cover"
          width="300"
          height="169"
          :preview-disabled="true"
          class="preview-image"
        />
        
        <n-space vertical size="small" align="center">
          <!-- Display image dimensions info -->
          <n-tag v-if="standardizedImageSize" type="success" size="small">
            <n-icon :component="Resize" class="mr-1" />
            Standardized to {{ STANDARD_WIDTH }}x{{ STANDARD_HEIGHT }}
          </n-tag>
          
          <n-space v-if="originalImageSize && standardizedImageSize" size="small">
            <n-tag type="info" size="small">
              Original: {{ originalImageSize }}
            </n-tag>
            <n-tag type="info" size="small">
              Optimized: {{ standardizedImageSize }}
            </n-tag>
          </n-space>
          
          <n-button size="small" type="error" class="mt-2" @click="resetUpload">
            Remove
          </n-button>
        </n-space>
      </n-space>
    </div>
    
    <!-- Upload area -->
    <n-upload
      v-if="!previewUrl"
      accept="image/*"
      :max-size="(props.maxSize || 5) * 1024 * 1024"
      :custom-request="handleUpload"
      @error="handleUploadError"
    >
      <n-upload-dragger :disabled="isResizing" class="upload-area">
        <div class="flex flex-col items-center justify-center p-4">
          <n-icon size="40" :depth="3">
            <cloud-upload />
          </n-icon>
          <n-text style="margin-top: 8px; font-size: 14px;">
            Click to select a cover image
          </n-text>
          <n-text depth="3" style="margin-top: 4px; font-size: 12px;">
            Will be standardized to {{ STANDARD_WIDTH }}x{{ STANDARD_HEIGHT }}
          </n-text>
          <n-text depth="3" style="font-size: 12px;">
            JPG, PNG, GIF under {{ props.maxSize || 5 }}MB
          </n-text>
        </div>
      </n-upload-dragger>
    </n-upload>
    
    <!-- Loading indicator while resizing -->
    <div v-if="isResizing" class="resize-loading">
      <n-text>Standardizing image size...</n-text>
    </div>
  </div>
</template>

<style scoped>
.image-uploader {
  width: 100%;
  max-width: 320px;
  margin: 0 auto;
  position: relative;
}

.preview-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #444;
  padding: 12px;
  border-radius: 8px;
}

.preview-image {
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.upload-area {
  cursor: pointer;
  position: relative;
  overflow: hidden;
  height: 180px;
  border: 1px dashed #444;
  border-radius: 8px;
}

.resize-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  z-index: 10;
}

.mr-1 {
  margin-right: 4px;
}

.mt-2 {
  margin-top: 8px;
}
</style> 