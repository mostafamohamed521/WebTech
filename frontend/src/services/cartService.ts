import { apiClient } from "./apiClient";
import type { Cart } from "@/types/cart";

function sessionKeyHeader() {
  let key = localStorage.getItem("webtech_session_key");
  if (!key) {
    key = crypto.randomUUID();
    localStorage.setItem("webtech_session_key", key);
  }
  return { "X-Session-Key": key };
}

export const cartService = {
  async getCart() {
    const { data } = await apiClient.get<{ data: Cart }>("/cart/", { headers: sessionKeyHeader() });
    return data.data;
  },

  async addItem(productId: string, quantity = 1, variantId?: string) {
    const { data } = await apiClient.post<{ data: Cart }>(
      "/cart/items/",
      { product_id: productId, variant_id: variantId, quantity },
      { headers: sessionKeyHeader() }
    );
    return data.data;
  },

  async updateItem(itemId: string, quantity: number) {
    const { data } = await apiClient.patch<{ data: Cart }>(
      `/cart/items/${itemId}/`,
      { quantity },
      { headers: sessionKeyHeader() }
    );
    return data.data;
  },

  async removeItem(itemId: string) {
    const { data } = await apiClient.delete<{ data: Cart }>(`/cart/items/${itemId}/`, {
      headers: sessionKeyHeader(),
    });
    return data.data;
  },
};

export { sessionKeyHeader };
