import { defineStore } from 'pinia';
import axios from '@/utils/http';
import type { CourseBasicInfo } from '@/api/course';
import { useLocalStorage } from '@vueuse/core';

// Define course store interface
interface CourseState {
  allCourses: CourseBasicInfo[];
  coursesById: Record<string, CourseBasicInfo>;
  lastFetchTime: number | null;
  isLoading: boolean;
}

// Cache expiry time in milliseconds (24 hours)
const CACHE_EXPIRY_TIME = 24 * 60 * 60 * 1000;

export const useCourseStore = defineStore('course', {
  state: (): CourseState => ({
    allCourses: [],
    coursesById: {},
    lastFetchTime: null,
    isLoading: false
  }),

  getters: {
    // Get a course by its ID
    getCourseById: (state) => (id: string): CourseBasicInfo | undefined => {
      return state.coursesById[id];
    },
    
    // Get all courses
    getAllCourses: (state): CourseBasicInfo[] => {
      return state.allCourses;
    },
    
    // Check if courses need to be refreshed
    needsRefresh: (state): boolean => {
      if (!state.lastFetchTime) return true;
      return Date.now() - state.lastFetchTime > CACHE_EXPIRY_TIME;
    }
  },

  actions: {
    // Fetch all courses from the API
    async fetchCourses() {
      // Don't fetch if we already have fresh data
      if (this.allCourses.length > 0 && !this.needsRefresh) {
        return this.allCourses;
      }
      
      this.isLoading = true;
      
      try {
        const response = await axios.get<CourseBasicInfo[]>('/courses');
        const courses = response.data;
        
        // Update the course list
        this.allCourses = courses;
        
        // Build lookup object for faster access by ID
        this.coursesById = courses.reduce((acc, course) => {
          acc[course.id] = course;
          return acc;
        }, {} as Record<string, CourseBasicInfo>);
        
        // Update fetch timestamp
        this.lastFetchTime = Date.now();
        
        return courses;
      } catch (error) {
        console.error('Failed to fetch courses:', error);
        return [];
      } finally {
        this.isLoading = false;
      }
    },
    
    // Get course name by ID (with fallback)
    getCourseNameById(id: string): string {
      return this.coursesById[id]?.name || 'Course';
    },
    
    // Force refresh courses from the API
    async refreshCourses() {
      // Clear the cache first
      this.allCourses = [];
      this.coursesById = {};
      this.lastFetchTime = null;
      
      // Fetch fresh data
      return await this.fetchCourses();
    }
  }
});
