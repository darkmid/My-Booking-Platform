<script setup lang="ts">
import router from "@/router";
import { useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useCourseStore } from "@/stores/course";
import {
  NLayoutHeader,
  NBreadcrumb,
  NBreadcrumbItem,
  NSpace,
  NDropdown,
  NAvatar,
  NIcon,
  NA,
} from "naive-ui";
import { storeToRefs } from "pinia";
import { computed, ref, watch, markRaw, onMounted } from "vue";
import { Home, Book, BookOutline, School, Grid } from "@vicons/ionicons5";

// Mark icon components as raw (non-reactive) to prevent the Vue warning
const HomeIcon = markRaw(Home);
const BookIcon = markRaw(Book);
const BookOutlineIcon = markRaw(BookOutline);
const GridIcon = markRaw(Grid);

const route = useRoute();
const authStore = useAuthStore();
const courseStore = useCourseStore();
const auth = storeToRefs(authStore);
const displayName = computed(() => {
  return auth.userInfo.value?.display_name || auth.userInfo.value?.username;
});

// Breadcrumb logic
const breadcrumbs = ref<{ name: string; path: string; icon?: any }[]>([]);

// Update breadcrumbs based on current route
const updateBreadcrumbs = () => {
  // Always start with Home
  breadcrumbs.value = [
    { name: 'Home', path: '/home', icon: HomeIcon }
  ];
  
  // Build breadcrumbs based on current route
  if (route.path.includes('/browse')) {
    breadcrumbs.value.push({ name: 'All Courses', path: '/browse', icon: GridIcon });
  } else if (route.path.includes('/courses')) {
    breadcrumbs.value.push({ name: 'My Courses', path: '/courses', icon: BookOutlineIcon });
    
    // If viewing a specific course, add it to breadcrumbs
    if (route.params.id) {
      const courseId = route.params.id.toString();
      const courseName = courseStore.getCourseNameById(courseId);
      
      breadcrumbs.value.push({ 
        name: courseName, 
        path: `/courses/${courseId}`,
        icon: BookIcon
      });
    }
  } else if (route.path.includes('/orders')) {
    breadcrumbs.value.push({ name: 'Orders', path: '/orders' });
  }
};

// Load courses data on component mount
onMounted(async () => {
  // Only fetch courses if we need to
  await courseStore.fetchCourses();
  updateBreadcrumbs();
});

// Watch only for changes to the route path and params
watch(
  () => [route.path, route.params.id],
  () => {
    updateBreadcrumbs();
  }
);

const options = [{ label: "Sign out", key: "logout" }];
const handleOptionSelect = async (key: string) => {
  if (key === "logout") {
    await authStore.logout();
    await router.push("/login");
  }
};
</script>
<template>
  <n-layout-header bordered>
    <n-breadcrumb class="my-1">
      <n-breadcrumb-item v-for="(crumb, index) in breadcrumbs" :key="crumb.path">
        <n-a v-if="index < breadcrumbs.length - 1" :href="crumb.path" @click.prevent="router.push(crumb.path)">
          <n-icon v-if="crumb.icon" :component="crumb.icon" class="breadcrumb-icon" />
          {{ crumb.name }}
        </n-a>
        <span v-else class="current-breadcrumb">
          <n-icon v-if="crumb.icon" :component="crumb.icon" class="breadcrumb-icon" />
          {{ crumb.name }}
        </span>
      </n-breadcrumb-item>
    </n-breadcrumb>

    <n-space class="navs my-1" :size="20" align="center">
      <span>Hello {{ displayName }}</span>
      <n-dropdown
        :options="options"
        placement="bottom-end"
        @select="handleOptionSelect"
      >
        <n-avatar size="small" round>
          <img src="~@/assets/logo.png" alt="" />
        </n-avatar>
      </n-dropdown>
    </n-space>
  </n-layout-header>
</template>

<style scoped>
.n-layout-header {
  display: flex;
  font-size: 1.1em;
  padding: 8px 18px;
}
.navs {
  margin-left: auto;
  line-height: 1px;
}
.breadcrumb-icon {
  margin-right: 4px;
  font-size: 1em;
  vertical-align: middle;
}
.current-breadcrumb {
  color: var(--primary-color, #18a058);
  font-weight: 500;
}
.my-1 {
  margin-top: 4px;
  margin-bottom: 4px;
}
</style>

