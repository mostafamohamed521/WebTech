export interface ProductVariant {
  id: string;
  color: string;
  storage: string;
  ram: string;
  size: string;
  material: string;
  edition: string;
  price_difference: string;
  stock: number;
  image: string;
  final_price: number;
}

export interface ProductSpecification {
  key: string;
  value: string;
}

export interface ProductImage {
  id: string;
  url: string;
  is_main: boolean;
  sort_order: number;
}

export interface ProductListItem {
  id: string;
  name: string;
  slug: string;
  price: string;
  discount_price: string | null;
  effective_price: number;
  currency: string;
  brand: string;
  category: string;
  featured: boolean;
  trending: boolean;
  in_stock: boolean;
  main_image: string | null;
}

export interface ProductDetail {
  id: string;
  name: string;
  slug: string;
  description: string;
  short_description: string;
  brand: { id: string; name: string; slug: string; logo: string; description: string };
  category: { id: string; name: string; slug: string; image: string; sort_order: number };
  price: string;
  discount_price: string | null;
  effective_price: number;
  currency: string;
  stock: number;
  in_stock: boolean;
  sku: string;
  warranty: string;
  featured: boolean;
  trending: boolean;
  images: ProductImage[];
  variants: ProductVariant[];
  specifications: ProductSpecification[];
  seo_title: string;
  seo_description: string;
  created_at: string;
  related_products: ProductListItem[];
}
