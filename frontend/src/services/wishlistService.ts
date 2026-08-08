import { apiClient } from "./apiClient";
import type { WishlistItem } from "@/types/wishlist";

export const wishlistService = {
  async list() {
    const { data } = await apiClient.get<{ data: WishlistItem[] }>("/wishlist/");
    return data.data;
  },
  async add(productId: string) {
    const { data } = await apiClient.post<{ data: WishlistItem[] }>("/wishlist/", { product_id: productId });
    return data.data;
  },
  async remove(productId: string) {
    await apiClient.delete(`/wishlist/${productId}/`);
  },
};
