import { useState } from "react";
import { useAdminOrders, useUpdateOrderStatus } from "@/hooks/useAdmin";

const STATUSES = ["pending", "confirmed", "processing", "shipped", "delivered", "cancelled", "refunded"];

export default function AdminOrdersPage() {
  const [statusFilter, setStatusFilter] = useState("");
  const [page, setPage] = useState(1);
  const { data, isLoading } = useAdminOrders({ status: statusFilter || undefined, page });
  const updateStatus = useUpdateOrderStatus();

  const orders = data?.results ?? [];

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Orders</h1>
        <select
          value={statusFilter}
          onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
          className="rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm"
        >
          <option value="">All statuses</option>
          {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-slate-200">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-left text-slate-500">
              <th className="p-3">Order</th>
              <th className="p-3">Customer</th>
              <th className="p-3">Total</th>
              <th className="p-3">Payment</th>
              <th className="p-3">Status</th>
            </tr>
          </thead>
          <tbody>
            {isLoading ? (
              <tr><td colSpan={5} className="p-4 text-center text-slate-500">Loading...</td></tr>
            ) : orders.length === 0 ? (
              <tr><td colSpan={5} className="p-4 text-center text-slate-500">No orders found.</td></tr>
            ) : (
              orders.map((order) => (
                <tr key={order.id} className="border-b border-slate-200 hover:bg-slate-100">
                  <td className="p-3 font-medium">{order.order_number}</td>
                  <td className="p-3 text-slate-500">{order.customer_email}</td>
                  <td className="p-3">{order.grand_total} EGP</td>
                  <td className="p-3">
                    <span className={`rounded-full px-2 py-0.5 text-xs ${order.payment_status === "paid" ? "bg-green-50 text-green-600" : "bg-slate-100 text-slate-500"}`}>
                      {order.payment_status}
                    </span>
                  </td>
                  <td className="p-3">
                    <select
                      value={order.status}
                      onChange={(e) => updateStatus.mutate({ id: order.id, status: e.target.value })}
                      className="rounded-lg border border-slate-200 bg-slate-50 px-2 py-1 text-xs capitalize"
                    >
                      {STATUSES.map((s) => <option key={s} value={s}>{s}</option>)}
                    </select>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {data && data.count > 20 && (
        <div className="mt-4 flex justify-center gap-2">
          <button disabled={page === 1} onClick={() => setPage((p) => p - 1)} className="rounded-full border border-slate-200 px-4 py-1.5 text-sm disabled:opacity-30">Previous</button>
          <button disabled={orders.length < 20} onClick={() => setPage((p) => p + 1)} className="rounded-full border border-slate-200 px-4 py-1.5 text-sm disabled:opacity-30">Next</button>
        </div>
      )}
    </div>
  );
}
