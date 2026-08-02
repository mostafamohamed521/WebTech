import { apiClient } from "./apiClient";
import { sessionKeyHeader, clearSessionKey } from "@/utils/session";
import type { AuthUser, AuthTokens, RegisterPayload, LoginPayload } from "@/types/auth";

interface AuthResponse {
  user: AuthUser;
  tokens: AuthTokens;
}

export const authService = {
  async register(payload: RegisterPayload) {
    // Send the guest session key so any items added to the cart before
    // registering get merged into the new account's cart server-side.
    const { data } = await apiClient.post<{ data: AuthResponse }>(
      "/authentication/register/", payload, { headers: sessionKeyHeader() }
    );
    clearSessionKey();
    return data.data;
  },

  async login(payload: LoginPayload) {
    // Same merge behavior on login — the backend folds the guest cart
    // (identified by this session key) into the user's cart.
    const { data } = await apiClient.post<{ data: AuthResponse }>(
      "/authentication/login/", payload, { headers: sessionKeyHeader() }
    );
    clearSessionKey();
    return data.data;
  },

  async logout(refresh: string) {
    await apiClient.post("/authentication/logout/", { refresh });
  },

  async me() {
    const { data } = await apiClient.get<{ data: AuthUser }>("/users/me/");
    return data.data;
  },
};
