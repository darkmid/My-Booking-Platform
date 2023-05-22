import type { CourseBasicInfo } from "@/interfaces/course.interface";

export interface User {
  id: string;
  username: string;
  password: string | null;
  display_name: string;
  telephone: string;
  campus: string;
  created_at: string;
  wx?: string;
  uni?: string;
  permissions?: [string];
  user_type: string;
  abn?: string;
  enrolled_courses?: CourseBasicInfo[];
}
