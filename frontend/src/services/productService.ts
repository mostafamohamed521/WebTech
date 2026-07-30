import { apiClient } from "./apiClient";
import type { ProductDetail, ProductListItem } from "@/types/product";

export const productService = {
  async detail(slug: string) {
    const { data } = await apiClient.get<{ data: ProductDetail }>(`/products/${slug}/`);
    return data.data;
  },
  async list(params?: Record<string, string | number | boolean>) {
    const { data } = await apiClient.get<{ data: { results: ProductListItem[]; count: number } }>("/products/", { params });
    return data.data;
  },
};
