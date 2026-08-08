import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  BarChart, Bar, PieChart, Pie, Cell, LineChart, Line,
  XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend,
} from "recharts";
import { Users, UserPlus, UserCheck } from "lucide-react";

import { analyticsService } from "@/services/analyticsService";

const COLORS = ["#3B82F6", "#8B5CF6", "#06B6D4", "#F59E0B", "#EF4444", "#10B981"];
const RANGES = [7, 30, 90];

export default function AdminAnalyticsPage() {
  const [days, setDays] = useState(30);
  const { data, isLoading } = useQuery({
    queryKey: ["admin", "analytics", days],
    queryFn: () => analyticsService.overview(days),
  });

  if (isLoading || !data) {
    return <p className="text-slate-500">Loading analytics...</p>;
  }

  const segments = data.customer_segments;

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Analytics</h1>
        <div className="flex gap-2">
          {RANGES.map((r) => (
            <button
              key={r}
              onClick={() => setDays(r)}
              className={`rounded-full border px-4 py-1.5 text-sm ${
                days === r ? "border-accent-blue bg-accent-blue/10 text-accent-blue" : "border-slate-200 text-slate-500"
              }`}
            >
              {r}d
            </button>
          ))}
        </div>
      </div>

      {/* Customer segments */}
      <div className="grid grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-200 bg-white shadow-sm p-5">
          <Users size={18} className="text-accent-blue" />
          <p className="mt-3 text-xl font-semibold">{segments.no_orders_yet}</p>
          <p className="text-sm text-slate-500">No orders yet</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white shadow-sm p-5">
          <UserPlus size={18} className="text-accent-cyan" />
          <p className="mt-3 text-xl font-semibold">{segments.new_customers}</p>
          <p className="text-sm text-slate-500">New customers (1 order)</p>
        </div>
        <div className="rounded-2xl border border-slate-200 bg-white shadow-sm p-5">
          <UserCheck size={18} className="text-accent-purple" />
          <p className="mt-3 text-xl font-semibold">{segments.returning_customers}</p>
          <p className="text-sm text-slate-500">Returning customers</p>
        </div>
      </div>

      {/* Revenue trend */}
      <div className="mt-6 rounded-2xl border border-slate-200 bg-white shadow-sm p-6">
        <h2 className="mb-4 text-lg font-medium">Revenue trend — last {days} days</h2>
        <ResponsiveContainer width="100%" height={260}>
          <LineChart data={data.revenue_trend}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
            <XAxis dataKey="date" tick={{ fill: "rgba(255,255,255,0.4)", fontSize: 11 }} tickFormatter={(d: string) => d.slice(5)} />
            <YAxis tick={{ fill: "rgba(255,255,255,0.4)", fontSize: 11 }} />
            <Tooltip contentStyle={{ background: "#181C25", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8 }} />
            <Line type="monotone" dataKey="revenue" stroke="#3B82F6" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        {/* Top products */}
        <div className="rounded-2xl border border-slate-200 bg-white shadow-sm p-6">
          <h2 className="mb-4 text-lg font-medium">Top selling products</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={data.top_products} layout="vertical" margin={{ left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis type="number" tick={{ fill: "rgba(255,255,255,0.4)", fontSize: 11 }} />
              <YAxis dataKey="name" type="category" width={120} tick={{ fill: "rgba(255,255,255,0.5)", fontSize: 11 }} />
              <Tooltip contentStyle={{ background: "#181C25", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8 }} />
              <Bar dataKey="units_sold" fill="#3B82F6" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Sales by category */}
        <div className="rounded-2xl border border-slate-200 bg-white shadow-sm p-6">
          <h2 className="mb-4 text-lg font-medium">Sales by category</h2>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={data.sales_by_category} dataKey="revenue" nameKey="category" cx="50%" cy="50%" outerRadius={90} label>
                {data.sales_by_category.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ background: "#181C25", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8 }} />
              <Legend wrapperStyle={{ fontSize: 12, color: "rgba(255,255,255,0.6)" }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
