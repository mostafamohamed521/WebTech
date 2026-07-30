export interface OrderListItem {
  id: string;
  order_number: string;
  status: string;
  payment_status: string;
  grand_total: string;
  created_at: string;
}

export interface OrderItem {
  id: string;
  product: string;
  variant: string | null;
  product_name_snapshot: string;
  quantity: number;
  unit_price: string;
  discount: string;
  subtotal: string;
}

export interface OrderDetail extends OrderListItem {
  shipping_status: string;
  subtotal: string;
  tax: string;
  discount: string;
  shipping_cost: string;
  items: OrderItem[];
  status_history: { status: string; note: string; created_at: string }[];
}
