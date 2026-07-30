import { apiClient } from "./apiClient";

export interface Address {
  id: string;
  label: string;
  full_name: string;
  phone: string;
  country: string;
  city: string;
  street: string;
  building: string;
  apartment: string;
  is_default: boolean;
}

export const addressService = {
  async list() {
    const { data } = await apiClient.get<{ data: Address[] }>("/addresses/");
    return data.data;
  },
  async create(payload: Omit<Address, "id">) {
    const { data } = await apiClient.post<{ data: Address }>("/addresses/", payload);
    return data.data;
  },
};
