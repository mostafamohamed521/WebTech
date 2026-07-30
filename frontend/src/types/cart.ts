export interface CartItem {
  id: string;
  product: string;
  product_name: string;
  product_slug: string;
  variant: string | null;
  quantity: number;
  price: string;
  subtotal: string;
}

export interface Cart {
  id: string;
  items: CartItem[];
  currency: string;
  coupon_code: string | null;
  subtotal: number;
}
