import type { User } from "@/interfaces/user.interface";
import axios from "../utils/http";
import type { Campus } from "./course";

export interface CreateStudentData {
  username: string;
  password: string;
  display_name: string;
  telephone: string;
  campus: string;
}

export interface UpdatePasswordData {
  password: string;
}

export const getCurrentUser = async () => {
  const res = await axios.get<User>("/auth");
  return res.data;
};

export const changePassword = async (
  username: string,
  data: UpdatePasswordData
) => {
  (await axios.put<User>(`/users/${username}`, data)).data;
};

export const registerNewStudent = async (data: CreateStudentData) => {
  (await axios.post(`/students`, data)).data;
};
