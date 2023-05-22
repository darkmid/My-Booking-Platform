import { useAxios } from "@vueuse/integrations/useAxios";
import axios from "@/utils/http";
import type { Campus } from "./course";

export const useCurrentCampus = () => useAxios<Campus[]>(`/campus`, axios);

export const getCurrentCampus = async () => {
  const res = await axios.get<Campus[]>("/campus");
  return res.data;
};
