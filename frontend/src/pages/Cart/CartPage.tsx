import { motion, AnimatePresence } from "framer-motion";
import { Link, useNavigate } from "react-router-dom";
import { Trash2, Minus, Plus } from "lucide-react";

import { useCart, useUpdateCartItem, useRemoveCartItem } from "@/hooks/useCart";
import { useAuthStore } from "@/store/authStore";

export default function CartPage() {
  const { data: cart, isLoading } = useCart();
  const updateItem = useUpdateCartItem();
  const removeItem = useRemoveCartItem();
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const navigate = useNavigate();

  if (isLoading) {
    return <div className="flex h-screen items-center justify-center bg-background text-white/50">Loading cart...</div>;
  }

  const items = cart?.items ?? [];
  const subtotal = cart?.subtotal ?? 0;

  return (
    <div className="min-h-screen bg-background px-6 pb-24 pt-32 text-white md:px-16">
      <h1 className="mb-10 text-3xl font-semibold">Shopping Cart</h1>

      {items.length === 0 ? (
        <div className="flex flex-col items-center gap-4 py-20 text-white/50">
          <p>Your cart is empty.</p>
          <Link to="/" className="rounded-full bg-white px-6 py-2 text-background">
            Continue shopping
          </Link>
        </div>
      ) : (
        <div className="grid gap-10 lg:grid-cols-[1fr_360px]">
          <div className="flex flex-col gap-4">
            <AnimatePresence>
              {items.map((item) => (
                <motion.div
                  key={item.id}
                  layout
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="flex items-center justify-between rounded-xl border border-white/10 bg-surface/50 p-4"
                >
                  <div>
                    <p className="font-medium">{item.product_name}</p>
                    <p className="text-sm text-white/40">{item.price} EGP</p>
                  </div>

                  <div className="flex items-center gap-3">
                    <button
                      onClick={() => updateItem.mutate({ itemId: item.id, quantity: Math.max(1, item.quantity - 1) })}
                      className="rounded-full border border-white/15 p-1.5 hover:bg-white/10"
                    >
                      <Minus size={14} />
                    </button>
                    <span className="w-6 text-center">{item.quantity}</span>
                    <button
                      onClick={() => updateItem.mutate({ itemId: item.id, quantity: item.quantity + 1 })}
                      className="rounded-full border border-white/15 p-1.5 hover:bg-white/10"
                    >
                      <Plus size={14} />
                    </button>
                  </div>

                  <p className="w-24 text-right font-medium">{item.subtotal} EGP</p>

                  <button
                    onClick={() => removeItem.mutate(item.id)}
                    className="ml-4 text-white/40 transition-colors hover:text-red-400"
                    aria-label="Remove item"
                  >
                    <Trash2 size={18} />
                  </button>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            className="h-fit rounded-2xl border border-white/10 bg-surface/50 p-6"
          >
            <h2 className="mb-4 text-lg font-medium">Order Summary</h2>
            <div className="flex justify-between text-sm text-white/60">
              <span>Subtotal</span>
              <span>{subtotal} EGP</span>
            </div>
            <p className="mt-1 text-xs text-white/30">Tax and shipping calculated at checkout</p>

            <button
              onClick={() => navigate(isAuthenticated ? "/checkout" : "/login")}
              className="mt-6 w-full rounded-full bg-white py-3 font-medium text-background transition-transform hover:scale-[1.02]"
            >
              {isAuthenticated ? "Proceed to Checkout" : "Sign in to Checkout"}
            </button>
          </motion.div>
        </div>
      )}
    </div>
  );
}
