export interface Review {
  id: string;
  user_name: string;
  user_avatar: string;
  rating: number;
  comment: string;
  verified_purchase: boolean;
  helpful_count: number;
  images: { id: string; url: string }[];
  liked_by_me: boolean;
  created_at: string;
}

export interface RatingSummary {
  average_rating: number;
  total_reviews: number;
  breakdown: Record<string, number>;
}
