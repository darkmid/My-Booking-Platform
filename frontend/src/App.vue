<script setup lang="ts">
import { RouterView } from "vue-router";
import {
  NConfigProvider,
  NGlobalStyle,
  darkTheme,
  lightTheme,
  NMessageProvider,
} from "naive-ui";
import MessageContent from "./components/MessageContent.vue";
</script>

<template>
  <n-config-provider :theme="darkTheme">
    <n-global-style />
    <n-message-provider>
      <message-content />
      <RouterView />
    </n-message-provider>
  </n-config-provider>
</template>

<style scoped></style>
