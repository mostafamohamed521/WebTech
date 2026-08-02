import { useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { authService } from "@/services/authService";
import { useAuthStore } from "@/store/authStore";
import type { LoginPayload, RegisterPayload } from "@/types/auth";

export function useLogin() {
  const setAuth = useAuthStore((s) => s.setAuth);
  const qc = useQueryClient();

  return useMutation({
    mutationFn: (payload: LoginPayload) => authService.login(payload),
    onSuccess: (data) => {
      setAuth(data.tokens, data.user);
      // Wipe any cached cart/wishlist/orders/etc — could belong to a
      // previous guest session or a different user on this same tab.
      qc.clear();
      toast.success(`Welcome back, ${data.user.first_name || data.user.username}`);
    },
    onError: () => {
      toast.error("Invalid email or password");
    },
  });
}

export function useRegister() {
  const setAuth = useAuthStore((s) => s.setAuth);
  const qc = useQueryClient();

  return useMutation({
    mutationFn: (payload: RegisterPayload) => authService.register(payload),
    onSuccess: (data) => {
      setAuth(data.tokens, data.user);
      qc.clear();
      toast.success("Account created — welcome to WEBTECH");
    },
    onError: () => {
      toast.error("Could not create account. Check your details and try again.");
    },
  });
}

export function useLogout() {
  const { refreshToken, logout } = useAuthStore();
  const qc = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      if (refreshToken) await authService.logout(refreshToken);
    },
    onSuccess: () => {
      logout();
      // Same reasoning as login: don't let this user's data survive
      // into the next guest session or next account on this tab.
      qc.clear();
      toast.success("Logged out");
    },
  });
}
