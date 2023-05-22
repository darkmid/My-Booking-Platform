<script setup lang="ts">
import { useCurrentCampus } from "@/api/campus";
import {
  type CreateStudentData,
  registerNewStudent,
  changePassword,
  type UpdatePasswordData,
} from "@/api/user";
import { useCampusStore } from "@/stores/auth";
import { FlowModelerReference } from "@vicons/carbon";
import {
  NForm,
  NFormItem,
  NInput,
  NButton,
  NSpace,
  NSelect,
  NTag,
  type FormRules,
  type FormItemRule,
  type FormInst,
  useMessage,
} from "naive-ui";
import { ref } from "vue";
import { useRouter } from "vue-router";

const username = ref<string>("");
const updatePasswordForm = ref<UpdatePasswordData>({
  password: "",
});

const router = useRouter();
const message = useMessage();
const campusStore = useCampusStore();
const campusList = campusStore.getCampusList;

const formRef = ref<FormInst | null>(null);
const handleUpdatePassword = async (
  username: string,
  data: UpdatePasswordData
) => {
  await changePassword(username, data);
};

const handleUpdateButtonClick = () => {
  formRef.value?.validate((errors) => {
    if (!errors) {
      handleUpdatePassword(username.value, updatePasswordForm.value);
    } else {
      console.log(errors);
      message.error("Invalid");
    }
  });
};

const handleBackButtonClick = () => {
  router.replace("/login");
};

const rules: FormRules = {
  password: [
    {
      required: true,
      validator(rule: FormItemRule, value: string) {
        if (!value) {
          return new Error("Password is required");
        }
        return true;
      },
      trigger: ["input", "blur"],
    },
  ],
};
</script>

<template>
  <div class="forget">
    <n-space vertical space-between class="w-1/2 bg-gray-800 rounded">
      <n-form
        :model="updatePasswordForm"
        class="m-20"
        :rules="rules"
        ref="formRef"
      >
        <n-form-item label="Username" path="username">
          <n-input v-model:value="username" clearable />
        </n-form-item>
        <n-form-item label="Password" path="password">
          <n-input
            v-model:value="updatePasswordForm.password"
            clearable
            type="password"
          />
        </n-form-item>

        <n-space align="center" justify="space-between">
          <n-button
            type="primary"
            size="large"
            class="text-white"
            @click="handleUpdateButtonClick"
            >Update</n-button
          >
          <n-button
            type="error"
            class="text-white"
            @click="handleBackButtonClick"
            >Back</n-button
          >
        </n-space>
      </n-form>
    </n-space>
  </div>
</template>

<style lang="less">
.forget {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
