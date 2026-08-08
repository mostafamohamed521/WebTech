import { motion } from "framer-motion";
import { useProducts } from "@/hooks/useProducts";
import ProductCard from "@/components/product/ProductCard";

export default function FeaturedProducts() {
  const { data, isLoading } = useProducts({ featured: true, page_size: 8 });
  const products = data?.results ?? [];

  if (!isLoading && products.length === 0) return null;

  return (
    <section id="featured-products" className="bg-background px-6 py-24 md:px-16" style={{ scrollMarginTop: "5rem" }}>
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="mb-10 flex items-end justify-between"
      >
        <div>
          <p className="text-sm uppercase tracking-widest text-accent-blue/70">Curated for you</p>
          <h2 className="mt-1 text-3xl font-semibold text-slate-900 md:text-4xl">Featured Products</h2>
        </div>
      </motion.div>

      {isLoading ? (
        <p className="text-slate-500">Loading featured products...</p>
      ) : (
        <div className="grid grid-cols-2 gap-5 sm:grid-cols-3 lg:grid-cols-4">
          {products.map((product, i) => (
            <ProductCard key={product.id} product={product} index={i} />
          ))}
        </div>
      )}
    </section>
  );
}
