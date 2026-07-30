import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { reviewService } from "@/services/reviewService";

export function useReviews(slug: string) {
  return useQuery({
    queryKey: ["reviews", slug],
    queryFn: () => reviewService.list(slug),
    enabled: !!slug,
  });
}

export function useCreateReview(slug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (payload: { rating: number; comment: string }) => reviewService.create(slug, payload),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["reviews", slug] });
      toast.success("Review posted — thank you!");
    },
    onError: () => toast.error("Could not post review (maybe you already reviewed this product?)"),
  });
}

export function useToggleHelpful(slug: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (reviewId: string) => reviewService.toggleHelpful(reviewId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["reviews", slug] }),
  });
}
