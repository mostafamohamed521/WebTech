import { useState } from "react";
import { useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { SlidersHorizontal, X } from "lucide-react";

import { useProducts } from "@/hooks/useProducts";
import ProductCard from "@/components/product/ProductCard";

const SORT_OPTIONS = [
  { value: "newest", label: "Newest" },
  { value: "price_low", label: "Price: Low to High" },
  { value: "price_high", label: "Price: High to Low" },
  { value: "name", label: "Name (A–Z)" },
];

export default function CategoryPage() {
  const { slug } = useParams<{ slug: string }>();
  const [ordering, setOrdering] = useState("newest");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [page, setPage] = useState(1);
  const [filtersOpen, setFiltersOpen] = useState(false);

  const { data, isLoading } = useProducts({
    category: slug,
    ordering,
    min_price: minPrice ? Number(minPrice) : undefined,
    max_price: maxPrice ? Number(maxPrice) : undefined,
    page,
    page_size: 12,
  });

  const products = data?.results ?? [];
  const count = data?.count ?? 0;

  const FilterPanel = (
    <div className="flex flex-col gap-6">
      <div>
        <p className="mb-2 text-sm font-medium text-slate-500">Price range (EGP)</p>
        <div className="flex items-center gap-2">
          <input
            type="number"
            value={minPrice}
            onChange={(e) => setMinPrice(e.target.value)}
            placeholder="Min"
            className="w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm outline-none focus:border-accent-blue"
          />
          <span className="text-slate-500">—</span>
          <input
            type="number"
            value={maxPrice}
            onChange={(e) => setMaxPrice(e.target.value)}
            placeholder="Max"
            className="w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm outline-none focus:border-accent-blue"
          />
        </div>
      </div>

      <button
        onClick={() => { setMinPrice(""); setMaxPrice(""); setPage(1); }}
        className="self-start text-sm text-slate-500 underline-offset-2 hover:text-slate-900 hover:underline"
      >
        Clear filters
      </button>
    </div>
  );

  return (
    <div className="min-h-screen bg-background px-6 pb-24 pt-32 text-slate-900 md:px-16">
      <div className="mb-8 flex items-end justify-between">
        <div>
          <p className="text-sm text-slate-500">Category</p>
          <h1 className="text-3xl font-semibold capitalize md:text-4xl">{slug?.replace(/-/g, " ")}</h1>
          <p className="mt-2 text-sm text-slate-500">{count} products</p>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={ordering}
            onChange={(e) => setOrdering(e.target.value)}
            className="rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm outline-none"
          >
            {SORT_OPTIONS.map((opt) => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>
          <button
            onClick={() => setFiltersOpen(true)}
            className="flex items-center gap-2 rounded-full border border-slate-200 px-4 py-2 text-sm md:hidden"
          >
            <SlidersHorizontal size={14} /> Filters
          </button>
        </div>
      </div>

      <div className="grid gap-10 md:grid-cols-[220px_1fr]">
        <aside className="hidden md:block">{FilterPanel}</aside>

        {filtersOpen && (
          <div className="fixed inset-0 z-50 flex bg-black/70 md:hidden" onClick={() => setFiltersOpen(false)}>
            <motion.div
              initial={{ x: -300 }}
              animate={{ x: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="h-full w-72 bg-surface p-6"
            >
              <div className="mb-6 flex items-center justify-between">
                <p className="font-medium">Filters</p>
                <button onClick={() => setFiltersOpen(false)}><X size={18} /></button>
              </div>
              {FilterPanel}
            </motion.div>
          </div>
        )}

        <div>
          {isLoading ? (
            <p className="text-slate-500">Loading products...</p>
          ) : products.length === 0 ? (
            <p className="text-slate-500">No products found in this category yet.</p>
          ) : (
            <div className="grid grid-cols-2 gap-5 sm:grid-cols-3 lg:grid-cols-4">
              {products.map((product, i) => (
                <ProductCard key={product.id} product={product} index={i} />
              ))}
            </div>
          )}

          {data && data.count > 12 && (
            <div className="mt-10 flex justify-center gap-2">
              <button
                disabled={page === 1}
                onClick={() => setPage((p) => p - 1)}
                className="rounded-full border border-slate-200 px-4 py-2 text-sm disabled:opacity-30"
              >
                Previous
              </button>
              <button
                disabled={products.length < 12}
                onClick={() => setPage((p) => p + 1)}
                className="rounded-full border border-slate-200 px-4 py-2 text-sm disabled:opacity-30"
              >
                Next
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
