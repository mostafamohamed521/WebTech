import { apiClient } from "./apiClient";
import type { Review, RatingSummary } from "@/types/review";

export const reviewService = {
  async list(slug: string) {
    const { data } = await apiClient.get<{ data: { summary: RatingSummary; reviews: Review[] } }>(`/reviews/product/${slug}/`);
    return data.data;
  },
  async create(slug: string, payload: { rating: number; comment: string }) {
    const { data } = await apiClient.post<{ data: Review }>(`/reviews/product/${slug}/`, payload);
    return data.data;
  },
  async toggleHelpful(reviewId: string) {
    const { data } = await apiClient.post<{ data: { liked: boolean; helpful_count: number } }>(`/reviews/${reviewId}/helpful/`);
    return data.data;
  },
};
