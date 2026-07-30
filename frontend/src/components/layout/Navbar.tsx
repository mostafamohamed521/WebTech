import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { ShoppingCart, Heart, User, Search } from "lucide-react";

import { useAuthStore } from "@/store/authStore";
import { useCart } from "@/hooks/useCart";
import { useLogout } from "@/hooks/useAuth";

/**
 * Navbar — transparent at top, blurs + shrinks on scroll (per WEBTECH
 * animation spec).
 */
export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const { isAuthenticated, user } = useAuthStore();
  const { data: cart } = useCart();
  const cartCount = cart?.items.length ?? 0;
  const logout = useLogout();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <motion.header
      animate={{
        backgroundColor: scrolled ? "rgba(5,5,5,0.7)" : "rgba(5,5,5,0)",
        backdropFilter: scrolled ? "blur(16px)" : "blur(0px)",
        height: scrolled ? 64 : 84,
      }}
      transition={{ duration: 0.3 }}
      className="fixed top-0 z-50 flex w-full items-center justify-between border-b border-white/0 px-6 md:px-12"
      style={{ borderBottomColor: scrolled ? "rgba(255,255,255,0.08)" : "transparent" }}
    >
      <Link to="/" className="text-xl font-bold tracking-widest text-white">
        WEBTECH
      </Link>

      <nav className="hidden gap-8 text-sm text-white/70 md:flex">
        <Link to="/category/smartphones" className="transition-colors hover:text-white">Smartphones</Link>
        <Link to="/category/laptops" className="transition-colors hover:text-white">Laptops</Link>
        <Link to="/category/gaming" className="transition-colors hover:text-white">Gaming</Link>
        <Link to="/deals" className="transition-colors hover:text-white">Deals</Link>
      </nav>

      <div className="flex items-center gap-5 text-white/80">
        <button aria-label="Search" className="transition-transform hover:scale-110">
          <Search size={19} />
        </button>
        <Link to="/wishlist" aria-label="Wishlist" className="transition-transform hover:scale-110">
          <Heart size={19} />
        </Link>
        <Link to="/cart" aria-label="Cart" className="relative transition-transform hover:scale-110">
          <ShoppingCart size={19} />
          {cartCount > 0 && (
            <span className="absolute -right-2 -top-2 flex h-4 w-4 items-center justify-center rounded-full bg-accent-blue text-[10px]">
              {cartCount}
            </span>
          )}
        </Link>

        {isAuthenticated ? (
          <button onClick={() => logout.mutate()} className="flex items-center gap-1.5 text-sm transition-transform hover:scale-105">
            <User size={19} />
            <span className="hidden md:inline">{user?.first_name || user?.username}</span>
          </button>
        ) : (
          <Link to="/login" className="flex items-center gap-1.5 text-sm transition-transform hover:scale-105">
            <User size={19} />
            <span className="hidden md:inline">Sign In</span>
          </Link>
        )}
      </div>
    </motion.header>
  );
}
