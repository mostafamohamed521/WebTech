import { apiClient } from "./apiClient";
import type { OrderDetail, OrderListItem } from "@/types/order";

export const orderService = {
  async checkout(payload: { address_id: string; coupon_code?: string; payment_method: "cod" | "stripe" | "paypal" }) {
    const { data } = await apiClient.post<{ data: OrderDetail }>("/orders/checkout/", payload);
    return data.data;
  },
  async list() {
    const { data } = await apiClient.get<{ data: OrderListItem[] }>("/orders/");
    return data.data;
  },
  async detail(orderNumber: string) {
    const { data } = await apiClient.get<{ data: OrderDetail }>(`/orders/${orderNumber}/`);
    return data.data;
  },
};
