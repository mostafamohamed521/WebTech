import { useState } from "react";
import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import { Heart, Truck, ShieldCheck } from "lucide-react";

import { productService } from "@/services/productService";
import { useAddToCart } from "@/hooks/useCart";
import { wishlistService } from "@/services/wishlistService";
import { useAuthStore } from "@/store/authStore";
import ProductViewer from "@/three/scenes/ProductViewer";
import StarRating from "@/components/ui/StarRating";
import ReviewsSection from "@/components/product/ReviewsSection";
import { useReviews } from "@/hooks/useReviews";

const COLOR_HEX: Record<string, string> = {
  black: "#111318",
  white: "#e8e8e8",
  blue: "#3B82F6",
  purple: "#8B5CF6",
  silver: "#c8c8c8",
  gold: "#d4af37",
};

export default function ProductDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const { data: product, isLoading } = useQuery({
    queryKey: ["product", slug],
    queryFn: () => productService.detail(slug!),
    enabled: !!slug,
  });
  const { data: reviewData } = useReviews(slug ?? "");
  const addToCart = useAddToCart();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  const [selectedVariantId, setSelectedVariantId] = useState<string | null>(null);
  const [quantity, setQuantity] = useState(1);

  if (isLoading) {
    return <div className="flex h-screen items-center justify-center bg-background text-white/50">Loading product...</div>;
  }

  if (!product) {
    return (
      <div className="flex h-screen flex-col items-center justify-center gap-4 bg-background text-white/50">
        <p>Product not found.</p>
        <Link to="/" className="rounded-full bg-white px-6 py-2 text-background">Back to home</Link>
      </div>
    );
  }

  const selectedVariant = product.variants.find((v) => v.id === selectedVariantId);
  const displayPrice = selectedVariant ? selectedVariant.final_price : product.effective_price;
  const viewerColor = selectedVariant?.color ? COLOR_HEX[selectedVariant.color.toLowerCase()] ?? "#111318" : "#111318";

  return (
    <div className="min-h-screen bg-background px-6 pb-24 pt-32 text-white md:px-16">
      <div className="grid gap-12 lg:grid-cols-2">
        {/* 3D Viewer */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
          <ProductViewer color={viewerColor} />
        </motion.div>

        {/* Info */}
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }}>
          <p className="text-sm text-white/40">{product.brand.name} · {product.category.name}</p>
          <h1 className="mt-1 text-3xl font-semibold md:text-4xl">{product.name}</h1>

          {reviewData && (
            <div className="mt-3 flex items-center gap-2">
              <StarRating value={Math.round(reviewData.summary.average_rating)} />
              <span className="text-sm text-white/50">
                {reviewData.summary.average_rating} ({reviewData.summary.total_reviews} reviews)
              </span>
            </div>
          )}

          <p className="mt-4 text-white/60">{product.short_description}</p>

          <div className="mt-6 flex items-baseline gap-3">
            <span className="text-3xl font-semibold">{displayPrice.toLocaleString()} {product.currency}</span>
            {product.discount_price && (
              <span className="text-lg text-white/40 line-through">{product.price} {product.currency}</span>
            )}
          </div>

          {/* Variants */}
          {product.variants.length > 0 && (
            <div className="mt-6">
              <p className="mb-2 text-sm text-white/60">Choose an option</p>
              <div className="flex flex-wrap gap-2">
                {product.variants.map((variant) => (
                  <button
                    key={variant.id}
                    onClick={() => setSelectedVariantId(variant.id)}
                    className={`rounded-full border px-4 py-1.5 text-sm transition-colors ${
                      selectedVariantId === variant.id
                        ? "border-accent-blue bg-accent-blue/10"
                        : "border-white/15 text-white/60 hover:border-white/30"
                    }`}
                  >
                    {[variant.color, variant.storage, variant.ram, variant.size].filter(Boolean).join(" / ")}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Quantity + actions */}
          <div className="mt-8 flex items-center gap-3">
            <div className="flex items-center rounded-full border border-white/15">
              <button onClick={() => setQuantity((q) => Math.max(1, q - 1))} className="px-4 py-2">−</button>
              <span className="w-8 text-center">{quantity}</span>
              <button onClick={() => setQuantity((q) => q + 1)} className="px-4 py-2">+</button>
            </div>

            <button
              onClick={() => addToCart.mutate({ productId: product.id, quantity, variantId: selectedVariantId ?? undefined })}
              disabled={!product.in_stock || addToCart.isPending}
              className="flex-1 rounded-full bg-white py-3 font-medium text-background transition-transform hover:scale-[1.02] disabled:opacity-40"
            >
              {product.in_stock ? "Add to Cart" : "Out of Stock"}
            </button>

            <button
              onClick={() => isAuthenticated ? wishlistService.add(product.id) : undefined}
              className="rounded-full border border-white/15 p-3 transition-colors hover:border-red-400 hover:text-red-400"
              aria-label="Add to wishlist"
            >
              <Heart size={18} />
            </button>
          </div>

          <div className="mt-6 flex flex-col gap-2 text-sm text-white/50">
            <p className="flex items-center gap-2"><Truck size={16} /> Free shipping over 500 EGP</p>
            {product.warranty && <p className="flex items-center gap-2"><ShieldCheck size={16} /> {product.warranty} warranty</p>}
          </div>

          {/* Specifications */}
          {product.specifications.length > 0 && (
            <div className="mt-10">
              <h2 className="mb-3 text-lg font-medium">Specifications</h2>
              <table className="w-full text-sm">
                <tbody>
                  {product.specifications.map((spec) => (
                    <tr key={spec.key} className="border-b border-white/5">
                      <td className="py-2 text-white/40">{spec.key}</td>
                      <td className="py-2 text-right text-white/80">{spec.value}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </motion.div>
      </div>

      {/* Description */}
      <div className="mt-16 max-w-3xl">
        <h2 className="mb-3 text-lg font-medium">About this product</h2>
        <p className="leading-relaxed text-white/60">{product.description}</p>
      </div>

      {/* Reviews */}
      <ReviewsSection slug={product.slug} />

      {/* Related products */}
      {product.related_products.length > 0 && (
        <div className="mt-20">
          <h2 className="mb-6 text-2xl font-semibold">You might also like</h2>
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            {product.related_products.map((related) => (
              <Link
                key={related.id}
                to={`/product/${related.slug}`}
                className="rounded-xl border border-white/10 bg-surface/30 p-4 transition-transform hover:scale-[1.02]"
              >
                <p className="font-medium">{related.name}</p>
                <p className="mt-1 text-sm text-white/50">{related.effective_price} {related.currency}</p>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
