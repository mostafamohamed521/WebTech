import { apiClient } from "./apiClient";

export const wishlistService = {
  async list() {
    const { data } = await apiClient.get("/wishlist/");
    return data.data;
  },
  async add(productId: string) {
    const { data } = await apiClient.post("/wishlist/", { product_id: productId });
    return data.data;
  },
  async remove(productId: string) {
    await apiClient.delete(`/wishlist/${productId}/`);
  },
};
