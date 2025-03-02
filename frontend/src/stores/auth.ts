import { defineStore } from "pinia";
import axios from "@/utils/http";
import { getCurrentUser } from "@/api/user";
import { StorageSerializers, useLocalStorage, useStorage } from "@vueuse/core";
import { type User } from "@/interfaces/user.interface";
import { type Campus } from "@/api/course";
import { getCurrentCampus, useCurrentCampus } from "@/api/campus";

const PREFIX = import.meta.env.VITE_STORAGE_PREFIX;
const USER_INFO_PREFIX = PREFIX + "user_info";

export const useCampusStore = defineStore({
  id: "campusStore",
  state: () => ({
    list: useLocalStorage<Campus[] | null>("campusList", null, {
      serializer: StorageSerializers.object,
    }),
  }),
  getters: {
    getCampusList: (state) => state.list,
    getCampusListLen: (state) => state.list?.length,
    getCampusName: (state) => (id: string) =>
      state.list?.find((campus) => campus.id == id)?.name,
  },
  actions: {
    async fetchCampus() {
      if (this.list == null) {
        this.list = await getCurrentCampus();
        console.log("fetching", this.list);
      }
    },

    async reload() {
      this.list = await getCurrentCampus();
      console.log("re-fetching", this.list);
    },
  },
});

export const useAuthStore = defineStore({
  id: "auth",
  state: () => ({
    userInfo: useLocalStorage<User | null>(USER_INFO_PREFIX, null, {
      serializer: StorageSerializers.object,
    }),
    // userInfo: JSON.parse(localStorage.getItem(USER_INFO_PREFIX) ?? "null"),
  }),
  getters: {
    getUserInfo: (state) => state.userInfo,
    isAdmin: (state) => state.userInfo?.user_type === "admin",
    isLoggedIn: (state) => state.userInfo !== null,
    hasPermission: (state) => (permission: string) => {
      return state.userInfo?.permissions?.includes(permission) || false;
    },
  },
  actions: {
    async login(username: string, password: string) {
      await axios.post("auth/login", {
        username,
        password,
      });
      const user = await getCurrentUser();
      this.userInfo = user;
      console.log(this.userInfo);
    },

    async reload() {
      const user = await getCurrentUser();
      this.userInfo = user;
    },
    async logout() {
      this.userInfo = null;
    },
  },
});
