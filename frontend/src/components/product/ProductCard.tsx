import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Heart, Eye } from "lucide-react";
import toast from "react-hot-toast";

import type { ProductListItem } from "@/types/product";
import { useAddToCart } from "@/hooks/useCart";
import { useAddToWishlist } from "@/hooks/useWishlist";
import { useAuthStore } from "@/store/authStore";
import CompareButton from "@/components/compare/CompareButton";

interface ProductCardProps {
  product: ProductListItem;
  index?: number;
}

/**
 * ProductCard — premium glass card with tilt-on-hover, glow border,
 * quick actions (wishlist / quick add). Per WEBTECH product-card spec.
 */
export default function ProductCard({ product, index = 0 }: ProductCardProps) {
  const addToCart = useAddToCart();
  const addToWishlist = useAddToWishlist();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  const handleWishlist = (e: React.MouseEvent) => {
    e.preventDefault();
    if (!isAuthenticated) {
      toast.error("Sign in to save items to your wishlist");
      return;
    }
    addToWishlist.mutate(product.id);
  };

  const handleQuickAdd = (e: React.MouseEvent) => {
    e.preventDefault();
    addToCart.mutate({ productId: product.id, quantity: 1 });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.4, delay: (index % 8) * 0.05 }}
      whileHover={{ y: -4, rotate: 0.4 }}
      className="group relative"
    >
      <Link
        to={`/product/${product.slug}`}
        className="block overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition-colors group-hover:border-accent-blue/40"
      >
        <div className="relative aspect-square overflow-hidden bg-slate-50">
          {product.main_image ? (
            <img
              src={product.main_image}
              alt={product.name}
              className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
            />
          ) : (
            <div className="flex h-full w-full items-center justify-center text-slate-400">No image</div>
          )}

          {product.discount_price && (
            <span className="absolute left-3 top-3 rounded-full bg-accent-blue px-2.5 py-1 text-xs font-medium text-white">
              Sale
            </span>
          )}
          {!product.in_stock && (
            <span className="absolute inset-0 flex items-center justify-center bg-black/60 text-sm text-white/80">
              Out of Stock
            </span>
          )}

          <div className="absolute right-3 top-3 flex flex-col gap-2 opacity-0 transition-opacity group-hover:opacity-100">
            <button
              onClick={handleWishlist}
              className="rounded-full bg-black/50 p-2 text-white backdrop-blur-md hover:bg-black/70"
              aria-label="Add to wishlist"
            >
              <Heart size={15} />
            </button>
            <Link
              to={`/product/${product.slug}`}
              className="rounded-full bg-black/50 p-2 text-white backdrop-blur-md hover:bg-black/70"
              aria-label="Quick view"
            >
              <Eye size={15} />
            </Link>
            <CompareButton slug={product.slug} />
          </div>
        </div>

        <div className="p-4">
          <p className="text-xs text-slate-500">{product.brand}</p>
          <h3 className="mt-0.5 truncate font-medium text-slate-900">{product.name}</h3>
          <div className="mt-2 flex items-center justify-between">
            <div className="flex items-baseline gap-2">
              <span className="font-semibold">{product.effective_price.toLocaleString()} {product.currency}</span>
              {product.discount_price && (
                <span className="text-xs text-slate-500 line-through">{product.price}</span>
              )}
            </div>
            <button
              onClick={handleQuickAdd}
              disabled={!product.in_stock}
              className="rounded-full bg-slate-100 px-3 py-1.5 text-xs font-medium text-slate-900 opacity-0 transition-opacity hover:bg-slate-200 group-hover:opacity-100 disabled:opacity-0"
            >
              + Add
            </button>
          </div>
        </div>
      </Link>
    </motion.div>
  );
}
