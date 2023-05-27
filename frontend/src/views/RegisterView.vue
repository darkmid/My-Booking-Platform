<script setup lang="ts">
import { useCurrentCampus } from "@/api/campus";
import { type CreateStudentData, registerNewStudent } from "@/api/user";
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

const newStudentForm = ref<CreateStudentData>({
  username: "",
  password: "",
  display_name: "",
  telephone: "",
  campus: "",
});

const router = useRouter();
const message = useMessage();
const campusStore = useCampusStore();
const campusList = campusStore.getCampusList;

const formRef = ref<FormInst | null>(null);
const handleRegisterNewStudent = async (data: CreateStudentData) => {
  await registerNewStudent(data);
};

const handleRegisterButtonClick = () => {
  formRef.value?.validate((errors) => {
    if (!errors) {
      handleRegisterNewStudent(newStudentForm.value);
      router.replace("/");
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
  username: [
    {
      required: true,
      validator(rule: FormItemRule, value: string) {
        if (!value) {
          return new Error("Username is required");
        }
        return true;
      },
      trigger: ["input", "blur"],
    },
  ],
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
  display_name: [
    {
      required: true,
      validator(rule: FormItemRule, value: string) {
        if (!value) {
          return new Error("Display Name is required");
        }
        return true;
      },
      trigger: ["input", "blur"],
    },
  ],
  telephone: [
    {
      required: true,
      validator(rule: FormItemRule, value: string) {
        if (!value) {
          return new Error("Phone Number is required");
        }
        if (!/^\d*$/.test(value)) {
          return new Error("Phone Number should be an integer");
        }
        return true;
      },
      trigger: ["input", "blur"],
    },
  ],
  campus: [
    {
      required: true,
      validator(rule: FormItemRule, value: string) {
        if (!value) {
          return new Error("Campus is required");
        }
        return true;
      },
      trigger: ["input", "blur"],
    },
  ],
};
</script>

<template>
  <div class="register gradientBg">
    <n-space
      vertical
      space-between
      class="w-1/2 bg-gray-50 bg-opacity-30 rounded-lg shadow-xl p-10"
    >
      <n-form :model="newStudentForm" class="m-20" :rules="rules" ref="formRef">
        <n-form-item label="Username" path="username">
          <n-input v-model:value="newStudentForm.username" clearable />
        </n-form-item>
        <n-form-item label="Password" path="password">
          <n-input
            v-model:value="newStudentForm.password"
            clearable
            type="password"
          />
        </n-form-item>
        <n-form-item label="Display Name" path="display_name">
          <n-input v-model:value="newStudentForm.display_name" clearable />
        </n-form-item>
        <n-form-item label="Phone Number" path="telephone">
          <n-input v-model:value="newStudentForm.telephone" clearable />
        </n-form-item>
        <n-form-item label="Campus" path="campus">
          <n-select
            :options="campusList?.map((a) => ({ label: a.name, value: a.id }))"
            v-model:value="newStudentForm.campus"
          />
        </n-form-item>
        <n-space align="center" justify="space-between">
          <n-button
            type="primary"
            size="large"
            class="text-white"
            @click="handleRegisterButtonClick"
            >Register</n-button
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
@import "../assets/page_background.css";
.register {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
