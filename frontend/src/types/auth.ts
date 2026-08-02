export interface AuthUser {
  id: string;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  phone: string;
  avatar: string;
  role: "super_admin" | "admin" | "manager" | "support" | "customer";
  is_email_verified: boolean;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface RegisterPayload {
  email: string;
  username: string;
  password: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}
