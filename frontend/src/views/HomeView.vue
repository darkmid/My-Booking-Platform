<script setup lang="ts">
import UserInfoCard from "@/components/UserInfoCard.vue";
import CoursesStatus from "@/components/CourseStatus.vue";
import CourseList from "@/components/CourseList.vue";
import { NGrid, NGridItem, NDivider } from "naive-ui";
import { useAuthStore, useCampusStore } from "@/stores/auth";

const authStore = useAuthStore();
const campusStore = useCampusStore();

const refreshUserInfo = async () => {
  await authStore.reload();
};
</script>

<template>
  <n-grid cols="1 m:2" :x-gap="12" :y-gap="8" responsive="screen">
    <n-grid-item v-if="authStore.userInfo">
      <user-info-card
        :user-info="authStore.getUserInfo!"
        :campus-name="campusStore.getCampusName(authStore.getUserInfo!.campus)!"
      ></user-info-card>
    </n-grid-item>
    <n-grid-item>
      <courses-status
        :user-info="authStore.getUserInfo!"
        :campus-name="campusStore.getCampusName(authStore.getUserInfo!.campus)!"
      ></courses-status>
    </n-grid-item>
  </n-grid>
  <n-divider />
  <course-list
    :user-info="authStore.getUserInfo!"
    :courses="authStore.getUserInfo?.enrolled_courses || []"
    @refresh="refreshUserInfo"
  ></course-list>
</template>
