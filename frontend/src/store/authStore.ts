import { create } from "zustand";
import type { AuthUser } from "@/types/auth";

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  user: AuthUser | null;
  isAuthenticated: boolean;
  setAuth: (tokens: { access: string; refresh: string }, user: AuthUser) => void;
  setAccessToken: (access: string) => void;
  logout: () => void;
}

const STORAGE_KEY = "webtech_refresh_token";

export const useAuthStore = create<AuthState>((set) => ({
  accessToken: null,
  refreshToken: typeof window !== "undefined" ? localStorage.getItem(STORAGE_KEY) : null,
  user: null,
  isAuthenticated: false,
  setAuth: (tokens, user) => {
    if (typeof window !== "undefined") localStorage.setItem(STORAGE_KEY, tokens.refresh);
    set({ accessToken: tokens.access, refreshToken: tokens.refresh, user, isAuthenticated: true });
  },
  setAccessToken: (access) => set({ accessToken: access }),
  logout: () => {
    if (typeof window !== "undefined") localStorage.removeItem(STORAGE_KEY);
    set({ accessToken: null, refreshToken: null, user: null, isAuthenticated: false });
  },
}));
