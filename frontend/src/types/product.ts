export interface Product {
  id: string;
  name: string;
  slug: string;
  price: number;
  discountPrice?: number;
  image: string;
  rating: number;
  stock: number;
}
