<script setup lang="ts">
import router from "@/router";
import { useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useCourse } from "@/api/course";
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
import { computed, ref, watchEffect } from "vue";
import { Home, Book, BookOutline, School, Grid } from "@vicons/ionicons5";

const route = useRoute();
const authStore = useAuthStore();
const auth = storeToRefs(authStore);
const displayName = computed(() => {
  return auth.userInfo.value?.display_name || auth.userInfo.value?.username;
});

// Breadcrumb logic
const breadcrumbs = ref<{ name: string; path: string; icon?: any }[]>([]);
const currentCourse = ref<any>(null);
const currentLectureTitle = ref<string>('');

// Watch for route changes to update breadcrumbs
watchEffect(async () => {
  // Always start with Home
  breadcrumbs.value = [
    { name: 'Home', path: '/home', icon: Home }
  ];
  
  // Reset course and lecture info
  currentCourse.value = null;
  currentLectureTitle.value = '';
  
  // Build breadcrumbs based on current route
  if (route.path.includes('/browse')) {
    breadcrumbs.value.push({ name: 'All Courses', path: '/browse', icon: Grid });
  } else if (route.path.includes('/courses')) {
    breadcrumbs.value.push({ name: 'My Courses', path: '/courses', icon: BookOutline });
    
    // If viewing a specific course, add it to breadcrumbs
    if (route.params.id) {
      try {
        // Fetch course details
        const courseId = route.params.id.toString();
        const { data: course } = useCourse(courseId);
        
        // Wait for the course data to be loaded
        if (course.value) {
          currentCourse.value = course.value;
          breadcrumbs.value.push({ 
            name: course.value.name, 
            path: `/courses/${courseId}`,
            icon: Book
          });
          
          // If there's a lecture hash in the URL, add it as well
          const hash = route.hash;
          if (hash && hash.startsWith('#lecture-')) {
            const lectureId = hash.replace('#lecture-', '');
            const lecture = course.value.lectures.find(l => l.id === lectureId);
            if (lecture) {
              currentLectureTitle.value = lecture.title;
              breadcrumbs.value.push({ 
                name: lecture.title, 
                path: `${route.path}${hash}`,
                icon: School
              });
            }
          }
        }
      } catch (error) {
        console.error('Error fetching course for breadcrumbs:', error);
      }
    }
  } else if (route.path.includes('/orders')) {
    breadcrumbs.value.push({ name: 'Orders', path: '/orders' });
  }
});

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
