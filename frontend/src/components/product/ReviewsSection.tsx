import { useState } from "react";
import { motion } from "framer-motion";
import { ThumbsUp, BadgeCheck } from "lucide-react";

import StarRating from "@/components/ui/StarRating";
import { useAuthStore } from "@/store/authStore";
import { useReviews, useCreateReview, useToggleHelpful } from "@/hooks/useReviews";

export default function ReviewsSection({ slug }: { slug: string }) {
  const { data, isLoading } = useReviews(slug);
  const createReview = useCreateReview(slug);
  const toggleHelpful = useToggleHelpful(slug);
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");

  if (isLoading) return null;

  const summary = data?.summary;
  const reviews = data?.reviews ?? [];

  return (
    <section className="mt-20">
      <h2 className="mb-6 text-2xl font-semibold text-slate-900">Customer Reviews</h2>

      {summary && (
        <div className="mb-8 flex items-center gap-6 rounded-2xl border border-slate-200 bg-white shadow-sm p-6">
          <div className="text-center">
            <p className="text-4xl font-bold text-slate-900">{summary.average_rating}</p>
            <StarRating value={Math.round(summary.average_rating)} />
            <p className="mt-1 text-xs text-slate-500">{summary.total_reviews} reviews</p>
          </div>
          <div className="flex-1 space-y-1">
            {[5, 4, 3, 2, 1].map((star) => {
              const count = summary.breakdown[String(star)] ?? 0;
              const pct = summary.total_reviews ? (count / summary.total_reviews) * 100 : 0;
              return (
                <div key={star} className="flex items-center gap-2 text-xs text-slate-500">
                  <span className="w-3">{star}</span>
                  <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-slate-100">
                    <div className="h-full bg-accent-blue" style={{ width: `${pct}%` }} />
                  </div>
                  <span className="w-6 text-right">{count}</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {isAuthenticated && (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            createReview.mutate({ rating, comment });
            setComment("");
          }}
          className="mb-10 rounded-2xl border border-slate-200 bg-white shadow-sm p-5"
        >
          <p className="mb-2 text-sm text-slate-500">Your rating</p>
          <StarRating value={rating} onChange={setRating} size={22} />
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Share your experience with this product..."
            className="mt-3 w-full rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm text-slate-900 outline-none focus:border-accent-blue"
            rows={3}
          />
          <button
            type="submit"
            disabled={createReview.isPending}
            className="mt-3 rounded-full bg-slate-900 px-6 py-2 text-sm font-medium text-white disabled:opacity-50"
          >
            {createReview.isPending ? "Posting..." : "Post Review"}
          </button>
        </form>
      )}

      <div className="flex flex-col gap-4">
        {reviews.map((review) => (
          <motion.div
            key={review.id}
            initial={{ opacity: 0, y: 8 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="rounded-xl border border-slate-200 bg-white shadow-sm p-4"
          >
            <div className="mb-1 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="font-medium text-slate-900">{review.user_name}</span>
                {review.verified_purchase && (
                  <span className="flex items-center gap-1 text-xs text-green-600">
                    <BadgeCheck size={14} /> Verified purchase
                  </span>
                )}
              </div>
              <StarRating value={review.rating} />
            </div>
            <p className="text-sm text-slate-500">{review.comment}</p>
            <button
              onClick={() => toggleHelpful.mutate(review.id)}
              className={`mt-2 flex items-center gap-1.5 text-xs transition-colors ${
                review.liked_by_me ? "text-accent-blue" : "text-slate-500 hover:text-accent-blue"
              }`}
            >
              <ThumbsUp size={13} /> Helpful ({review.helpful_count})
            </button>
          </motion.div>
        ))}
        {reviews.length === 0 && <p className="text-sm text-slate-500">No reviews yet — be the first to review this product.</p>}
      </div>
    </section>
  );
}
