import HeroSection from "@/components/home/HeroSection";
import FeaturedProducts from "@/components/home/FeaturedProducts";

/**
 * HomePage
 * Structure per WEBTECH spec: Hero, Featured Categories, Featured
 * Products, Premium Brands, Trending, Gaming Zone, Deals, Reviews...
 */
export default function HomePage() {
  return (
    <main>
      <HeroSection />
      <FeaturedProducts />
      {/* TODO: FeaturedCategories, PremiumBrands, Trending... */}
    </main>
  );
}
