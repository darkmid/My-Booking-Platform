<script lang="ts" setup>
import { deleteLecture, uploadAttachment, type Lecture } from "@/api/course";
import { computed, defineProps, ref } from "vue";
import axios from "@/utils/http";
import {
  NCard,
  NThing,
  NAvatar,
  NIcon,
  NDescriptions,
  NDescriptionsItem,
  NA,
  NDivider,
  NButton,
  NPopconfirm,
  NSpace,
  NTag,
  NModal,
  NUpload,
  NUploadDragger,
  NInput,
  NForm,
  NFormItem,
  type UploadCustomRequestOptions,
  useMessage,
} from "naive-ui";
import {
  Archive,
  CloudUpload,
  DocumentAttach,
  Videocam,
  Create,
} from "@vicons/ionicons5";
import { Delete } from "@vicons/carbon";

const props = defineProps<{
  lecture: Lecture;
  course_id: string;
  isAdmin: Boolean;
  onUpdate: () => void;
}>();

const message = useMessage();
const showUpload = ref(false);
const showEditRecordingModal = ref(false);
const recordingUrl = ref('');
const isUpdatingRecording = ref(false);

// Initialize recording URL from props
const initEditRecording = () => {
  recordingUrl.value = props.lecture.recording_url;
  showEditRecordingModal.value = true;
};

// Update recording URL
const updateRecordingUrl = async () => {
  if (!recordingUrl.value) {
    message.warning('Please enter a valid recording URL');
    return;
  }

  try {
    isUpdatingRecording.value = true;
    
    // Make API call to update lecture recording URL
    await axios.put(`/courses/${props.course_id}/lectures/${props.lecture.id}`, {
      recording_url: recordingUrl.value
    });
    
    message.success('Recording URL updated successfully');
    showEditRecordingModal.value = false;
    
    // Refresh lecture data
    props.onUpdate();
  } catch (error) {
    console.error('Failed to update recording URL:', error);
    message.error('Failed to update recording URL');
  } finally {
    isUpdatingRecording.value = false;
  }
};

const handleAddNewAttachment = () => {
  showUpload.value = true;
};

const uploadRequest = async ({
  file,
  onFinish,
  onError,
  onProgress,
}: UploadCustomRequestOptions) => {
  try {
    console.log("upload");
    await uploadAttachment(
      props.course_id,
      props.lecture.id,
      file.file!,
      file.name,
      "attachment",
      ({ progress }) => {
        onProgress({ percent: Math.ceil(progress || 0) });
      }
    );
    onFinish();
    message.success("File Uploaded.");
    setTimeout(() => window.location.reload(), 1500);
  } catch (e) {
    onError();
  }
};

const scheduled_at = computed(() => new Date(props.lecture.scheduled_at + "Z"));

const handleDelete = async () => {
  await deleteLecture(props.course_id, props.lecture.id);
  props.onUpdate();
};
</script>
<template>
  <n-card class="lecture-card">
    <n-thing>
      <template #avatar>
        <n-avatar>
          <n-icon :component="Videocam"></n-icon>
        </n-avatar>
      </template>
      <template #header>
        {{ props.lecture.title }}
      </template>
      <template #header-extra>
        {{ scheduled_at.toLocaleDateString() }}
      </template>
      <template #description>
        <div class="text-xs text-slate-300 lecture-id">{{ props.lecture.id }}</div>
      </template>
      <n-descriptions :column="1" label-placement="left" class="lecture-details">
        <n-descriptions-item label="Time">
          {{ scheduled_at.toLocaleTimeString() }}
        </n-descriptions-item>
        <n-descriptions-item label="Streaming">
          <n-a :href="props.lecture.streaming_url" target="_blank" class="lecture-link">Jump to Zoom</n-a>
        </n-descriptions-item>
        <n-descriptions-item label="Recording">
          <div class="recording-row">
            <template v-if="props.lecture.recording_url">
              <n-a :href="props.lecture.recording_url" target="_blank" class="lecture-link">
                Jump to Recording
              </n-a>
            </template>
            <template v-else>
              <span class="no-recording">No recording available</span>
            </template>
            <n-button v-if="isAdmin" size="tiny" text type="primary" @click="initEditRecording" class="edit-btn">
              <n-icon size="small" :component="Create"></n-icon>
              {{ props.lecture.recording_url ? 'Edit' : 'Add' }}
            </n-button>
          </div>
        </n-descriptions-item>
      </n-descriptions>
      <template #footer>
        <n-divider class="text-xs text-gray-400"> Attachments </n-divider>
        <div class="attachments-container">
          <n-space wrap>
            <n-tag
              v-for="attachment in props.lecture.attachments"
              :key="attachment.name"
              size="medium"
              round
              :bordered="false"
              type="success"
              class="attachment-tag"
            >
              <template #icon>
                <n-icon :component="DocumentAttach"></n-icon>
              </template>
              <n-a :href="attachment.signed_url" target="_blank" class="attachment-link">
                {{ attachment.name }}
              </n-a>
            </n-tag>
            <n-tag
              v-if="isAdmin"
              round
              :bordered="false"
              size="medium"
              type="info"
              class="upload-tag"
            >
              <template #icon>
                <n-icon :component="CloudUpload"></n-icon>
              </template>
              <n-a @click="handleAddNewAttachment" class="upload-link">Upload +</n-a>
            </n-tag>
          </n-space>
        </div>
        <n-space justify="end" v-if="isAdmin" class="lecture-actions">
          <n-popconfirm @positive-click="handleDelete">
            <template #trigger>
              <n-button quaternary type="error" class="delete-button">
                <template #icon>
                  <n-icon><delete /></n-icon>
                </template>
                Delete
              </n-button>
            </template>
            Are you sure you want to delete this lecture?
          </n-popconfirm>
        </n-space>
      </template>
    </n-thing>
  </n-card>

  <!-- Upload Attachment Modal -->
  <n-modal v-model:show="showUpload">
    <n-card
      style="width: 450px"
      title="Upload Attachment"
      :bordered="false"
      size="huge"
      class="upload-modal"
    >
      <p class="upload-description">
        Upload files for students to access. Maximum file size: 50MB.
      </p>
      <n-upload 
        :directory-dnd="false" 
        :custom-request="uploadRequest"
        :max-size="50 * 1024 * 1024"
      >
        <n-upload-dragger class="upload-dragger">
          <div class="upload-icon">
            <n-icon size="48" :depth="3" :component="Archive"></n-icon>
          </div>
          <div class="upload-text">
            <p>Click or drag files here to upload</p>
            <p class="upload-hint">PDF, Word, Excel, PowerPoint, Images, etc.</p>
          </div>
        </n-upload-dragger>
      </n-upload>
    </n-card>
  </n-modal>

  <!-- Edit Recording URL Modal -->
  <n-modal v-model:show="showEditRecordingModal">
    <n-card
      style="width: 450px"
      title="Update Recording URL"
      :bordered="false"
      size="huge"
      class="upload-modal"
    >
      <p class="upload-description">
        Update the URL for this lecture's recording.
      </p>
      <n-form>
        <n-form-item label="Recording URL">
          <n-input 
            v-model:value="recordingUrl" 
            placeholder="https://zoom.us/rec/share/..." 
            :disabled="isUpdatingRecording"
          />
        </n-form-item>
        <p class="form-hint">Recording URLs are typically provided by Zoom after the meeting is recorded.</p>
      </n-form>
      <n-space justify="end" class="mt-4">
        <n-button @click="showEditRecordingModal = false" :disabled="isUpdatingRecording">
          Cancel
        </n-button>
        <n-button type="primary" @click="updateRecordingUrl" :loading="isUpdatingRecording">
          Update
        </n-button>
      </n-space>
    </n-card>
  </n-modal>
</template>

<style scoped>
.lecture-card {
  transition: transform 0.2s, box-shadow 0.2s;
  height: 100%;
}

.lecture-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.lecture-id {
  opacity: 0.6;
}

.lecture-details {
  margin: 16px 0;
}

.recording-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.edit-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 0 6px;
  height: 22px;
  font-size: 12px;
}

.attachments-container {
  margin: 12px 0;
}

.attachment-tag {
  margin-right: 8px;
  margin-bottom: 8px;
  transition: transform 0.2s;
}

.attachment-tag:hover {
  transform: translateY(-2px);
}

.attachment-link {
  display: inline-block;
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.upload-tag {
  background-color: rgba(24, 144, 255, 0.1) !important;
  cursor: pointer;
}

.lecture-link:hover,
.attachment-link:hover,
.upload-link:hover {
  text-decoration: underline;
}

.lecture-actions {
  margin-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding-top: 12px;
}

.delete-button {
  display: flex;
  align-items: center;
}

.upload-modal {
  border-radius: 8px;
}

.upload-description {
  margin-bottom: 16px;
  color: rgba(255, 255, 255, 0.7);
}

.form-hint {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 4px;
}

.upload-dragger {
  padding: 24px;
  border-radius: 8px;
}

.upload-icon {
  margin-bottom: 16px;
}

.upload-text {
  font-size: 14px;
}

.upload-hint {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 4px;
}

.mt-4 {
  margin-top: 16px;
}

.no-recording {
  color: rgba(255, 255, 255, 0.45);
  font-style: italic;
  cursor: not-allowed;
}
</style>
