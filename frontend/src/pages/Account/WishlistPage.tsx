import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Trash2, ShoppingCart } from "lucide-react";

import { useWishlist, useRemoveFromWishlist } from "@/hooks/useWishlist";
import { useAddToCart } from "@/hooks/useCart";

export default function WishlistPage() {
  const { data: items, isLoading } = useWishlist();
  const removeItem = useRemoveFromWishlist();
  const addToCart = useAddToCart();

  const moveToCart = (productId: string) => {
    addToCart.mutate(
      { productId, quantity: 1 },
      { onSuccess: () => removeItem.mutate(productId) }
    );
  };

  return (
    <div>
      <h1 className="mb-6 text-2xl font-semibold">My Wishlist</h1>

      {isLoading ? (
        <p className="text-slate-500">Loading wishlist...</p>
      ) : !items || items.length === 0 ? (
        <div className="rounded-2xl border border-slate-200 bg-white shadow-sm p-8 text-center text-slate-500">
          <p>Your wishlist is empty.</p>
          <Link to="/" className="mt-4 inline-block rounded-full bg-slate-900 px-6 py-2 text-sm text-white">
            Discover products
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3">
          <AnimatePresence>
            {items.map((item) => (
              <motion.div
                key={item.id}
                layout
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.9 }}
                className="rounded-xl border border-slate-200 bg-white shadow-sm p-4"
              >
                <Link to={`/product/${item.product.slug}`}>
                  <p className="truncate font-medium">{item.product.name}</p>
                  <p className="mt-1 text-sm text-slate-500">{item.product.effective_price} {item.product.currency}</p>
                </Link>
                <div className="mt-3 flex gap-2">
                  <button
                    onClick={() => moveToCart(item.product.id)}
                    className="flex flex-1 items-center justify-center gap-1.5 rounded-full bg-slate-100 py-1.5 text-xs hover:bg-slate-200"
                  >
                    <ShoppingCart size={12} /> Move to cart
                  </button>
                  <button
                    onClick={() => removeItem.mutate(item.product.id)}
                    className="rounded-full border border-slate-200 p-1.5 text-slate-500 hover:text-red-500"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}
