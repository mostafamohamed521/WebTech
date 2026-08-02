import { useQuery } from "@tanstack/react-query";
import { productService } from "@/services/productService";

export interface ProductQueryParams {
  category?: string;
  brand?: string;
  search?: string;
  min_price?: number;
  max_price?: number;
  featured?: boolean;
  trending?: boolean;
  ordering?: string;
  page?: number;
  page_size?: number;
}

export function useProducts(params?: ProductQueryParams) {
  return useQuery({
    queryKey: ["products", params],
    queryFn: () => productService.list(params as Record<string, string | number | boolean>),
  });
}
