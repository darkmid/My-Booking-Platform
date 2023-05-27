<script setup lang="ts">
import {
  NSpace,
  NH1,
  NH5,
  NButton,
  NForm,
  NInput,
  NFormItem,
  NA,
  loadingBarDark,
  NTable,
  NGradientText,
} from "naive-ui";
import { VueElement, computed, ref } from "vue";
import { useAuthStore, useCampusStore } from "@/stores/auth";
import { useRouter } from "vue-router";

interface LoginForm {
  username: string;
  password: string;
}

const formRef = ref<LoginForm | null>(null);
const formValue = ref<LoginForm>({
  username: "",
  password: "",
});

const router = useRouter();
const authStore = useAuthStore();
const campusStore = useCampusStore();
const disabled = computed(
  () => formValue.value.username === "" || formValue.value.password === ""
);
const loading = ref(false);
const handleLogin = async () => {
  try {
    loading.value = true;
    await authStore.login(formValue.value.username, formValue.value.password);
    router.replace("/");
  } finally {
    loading.value = false;
  }
};

campusStore.fetchCampus();
</script>

<template>
  <div class="login gradientBg">
    <n-space class="m-20 bg-white flex" vertical>
      <n-gradient-text type="error" size="20" class="">
        Belows are demo accounts.<br />
        Please dont change the password from forgot page!
      </n-gradient-text>
      <n-table :bordered="false" :single-line="false">
        <thead>
          <tr>
            <th>Acc. Type</th>
            <th>Username</th>
            <th>Password</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Admin</td>
            <td>admin</td>
            <td>password</td>
          </tr>
          <tr>
            <td>Student</td>
            <td>student</td>
            <td>password</td>
          </tr>
          <tr>
            <td>Teacher</td>
            <td>teacher1</td>
            <td>password</td>
          </tr>
        </tbody>
      </n-table>
    </n-space>

    <n-space
      vertical
      class="mr-20 min-h-fit min-w-fit bg-gray-50 bg-opacity-30 rounded-lg shadow-xl p-10"
    >
      <n-h1>Welcome to My Booking Platform Online</n-h1>
      <n-h5>Please login to continue</n-h5>
      <n-form ref="formRef" :model="formValue">
        <n-form-item path="username" label="Username">
          <n-input
            type="text"
            placeholder="Please Input"
            v-model:value="formValue.username"
          />
        </n-form-item>
        <n-form-item path="password" label="Password">
          <n-input
            type="password"
            placeholder="Please Input"
            v-model:value="formValue.password"
          />
        </n-form-item>
      </n-form>

      <n-space align="center" justify="space-between">
        <n-a href="/forget">Forget Your Password?</n-a>
        <n-space>
          <n-button tag="a" size="large" href="/register">Register</n-button>
          <n-button
            type="primary"
            tag="a"
            size="large"
            :disabled="disabled"
            :loading="loading"
            class="text-white"
            @click="handleLogin"
            >Login</n-button
          >
        </n-space>
      </n-space>
    </n-space>
  </div>
</template>

<style lang="less">
.login {
  width: 100vw;
  height: 100vh;
  display: inline-flex;
  justify-content: flex-end;
  align-items: center;
}

@import "../assets/page_background.css";
</style>
