import { defineStore } from "pinia";
import { StorageSerializers, useLocalStorage } from "@vueuse/core";
import { type Teacher } from "@/api/course";
import axios from "@/utils/http";
import { getTeacherList } from "@/api/user";

const PREFIX = import.meta.env.VITE_STORAGE_PREFIX;

// Function to fetch teachers from the API
export const getTeachers = async () => {
  try {
    const response = await axios.get<Teacher[]>("/users?type=teacher");
    return response.data;
  } catch (error) {
    console.error("Error fetching teachers:", error);
    return [];
  }
};

export const useTeacherStore = defineStore({
  id: "teacherStore",
  state: () => ({
    list: useLocalStorage<Teacher[] | null>(`${PREFIX}teacherList`, null, {
      serializer: StorageSerializers.object,
    }),
  }),
  getters: {
    getTeacherList: (state) => state.list,
    getTeacherListLen: (state) => state.list?.length,
    getTeacherName: (state) => (id: string) =>
      state.list?.find((teacher) => teacher.id === id)?.display_name,
  },
  actions: {
    async fetchTeachers() {
      if (this.list == null) {
        this.list = await getTeacherList();
        console.log("fetching teachers", this.list);
      }
    },

    async reload() {
      this.list = await getTeacherList();
      console.log("re-fetching teachers", this.list);
    },
  },
}); 