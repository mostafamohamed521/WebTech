import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";

import { orderService } from "@/services/orderService";

const STATUS_LABEL: Record<string, string> = {
  pending: "Pending",
  confirmed: "Confirmed",
  processing: "Processing",
  shipped: "Shipped",
  delivered: "Delivered",
  cancelled: "Cancelled",
  refunded: "Refunded",
};

export default function OrderDetailPage() {
  const { orderNumber } = useParams<{ orderNumber: string }>();
  const { data: order, isLoading } = useQuery({
    queryKey: ["order", orderNumber],
    queryFn: () => orderService.detail(orderNumber!),
    enabled: !!orderNumber,
  });

  if (isLoading) {
    return <div className="flex h-screen items-center justify-center bg-background text-white/50">Loading order...</div>;
  }

  if (!order) {
    return (
      <div className="flex h-screen flex-col items-center justify-center gap-4 bg-background text-white/50">
        <p>Order not found.</p>
        <Link to="/" className="rounded-full bg-white px-6 py-2 text-background">Back to home</Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background px-6 pb-24 pt-32 text-white md:px-16">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <p className="text-sm text-white/40">Order</p>
        <h1 className="mb-2 text-3xl font-semibold">{order.order_number}</h1>
        <span className="inline-block rounded-full bg-accent-blue/15 px-3 py-1 text-sm text-accent-blue">
          {STATUS_LABEL[order.status] ?? order.status}
        </span>
      </motion.div>

      <div className="mt-10 grid gap-10 lg:grid-cols-[1fr_360px]">
        <div className="flex flex-col gap-3">
          {order.items.map((item) => (
            <div key={item.id} className="flex items-center justify-between rounded-xl border border-white/10 bg-surface/50 p-4">
              <div>
                <p className="font-medium">{item.product_name_snapshot}</p>
                <p className="text-sm text-white/40">Qty {item.quantity} × {item.unit_price} EGP</p>
              </div>
              <p className="font-medium">{item.subtotal} EGP</p>
            </div>
          ))}

          <div className="mt-6">
            <h2 className="mb-3 text-lg font-medium">Order Timeline</h2>
            <div className="flex flex-col gap-2 border-l border-white/10 pl-4">
              {order.status_history.map((h, i) => (
                <div key={i} className="relative">
                  <span className="absolute -left-[21px] top-1.5 h-2 w-2 rounded-full bg-accent-blue" />
                  <p className="text-sm font-medium">{STATUS_LABEL[h.status] ?? h.status}</p>
                  {h.note && <p className="text-xs text-white/40">{h.note}</p>}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="h-fit rounded-2xl border border-white/10 bg-surface/50 p-6">
          <h2 className="mb-4 text-lg font-medium">Summary</h2>
          {[
            ["Subtotal", order.subtotal],
            ["Tax", order.tax],
            ["Shipping", order.shipping_cost],
            ["Discount", `-${order.discount}`],
          ].map(([label, value]) => (
            <div key={label} className="flex justify-between text-sm text-white/60">
              <span>{label}</span>
              <span>{value} EGP</span>
            </div>
          ))}
          <div className="mt-3 flex justify-between border-t border-white/10 pt-3 font-medium">
            <span>Total</span>
            <span>{order.grand_total} EGP</span>
          </div>
        </div>
      </div>
    </div>
  );
}
