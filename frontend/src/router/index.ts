import { createRouter, createWebHistory } from "vue-router";
//import HomeView from "@/views/HomeView.vue";
import Layout from "@/layout/index.vue";
import { useAuthStore } from "@/stores/auth";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "layout",
      redirect: "/home",
      component: Layout,
      children: [
        {
          name: "home",
          path: "/home",
          component: () => import("../views/HomeView.vue"),
          meta: {
            requiresAuth: true,
            title: "Home",
          },
        },
        {
          name: "orders",
          path: "/orders",
          component: () => import("../views/OrdersView.vue"),
          meta: {
            requiresAuth: true,
            title: "Orders",
          },
        },
        {
          name: "browse",
          path: "/browse",
          component: () => import("../views/BrowseView.vue"),
          meta: {
            title: "All Courses",
            requiresAuth: true,
          },
        },
        {
          name: "courses",
          path: "/courses",
          component: () => import("../views/CoursesView.vue"),
          meta: {
            requiresAuth: true,
            title: "Course",
          },
        },
        {
          name: "course",
          path: "/courses/:id",
          component: () => import("../views/CourseView.vue"),
          meta: {
            requiresAuth: true,
            title: "Course Page",
          },
        },
      ],
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue"),
      meta: {
        requiresAuth: false,
        title: "Login",
      },
    },
    {
      path: "/register",
      name: "register",
      component: () => import("../views/RegisterView.vue"),
      meta: {
        requiresAuth: false,
        title: "Register",
      },
    },
    {
      path: "/forget",
      name: "forget",
      component: () => import("../views/ForgetView.vue"),
      meta: {
        requiresAuth: false,
        title: "Forget",
      },
    },
  ],
});

router.beforeEach((to) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return {
      name: "login",
      query: { redirect: to.fullPath },
    };
  }
});

router.afterEach((to) => {
  document.title =
    to.meta.title || to.name?.toString() || "E-Learning Hub";
});

export default router;
