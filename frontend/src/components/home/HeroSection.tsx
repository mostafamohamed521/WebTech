import { Suspense, lazy } from "react";
import { motion } from "framer-motion";

import SplitText from "@/components/ui/SplitText";

const HeroCanvas = lazy(() => import("@/three/scenes/HeroCanvas"));

/**
 * HeroSection — full-screen cinematic hero.
 * Dark gradient background + animated grid + 3D floating products
 * (laptop/phone/watch/earbuds) + split-text headline + glass CTAs.
 */
export default function HeroSection() {
  return (
    <section className="relative h-screen w-full overflow-hidden bg-background">
      {/* Background: gradient + animated grid */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_#0D1117_0%,_#050505_70%)]" />
      <div
        className="absolute inset-0 opacity-[0.08]"
        style={{
          backgroundImage:
            "linear-gradient(#3B82F6 1px, transparent 1px), linear-gradient(90deg, #3B82F6 1px, transparent 1px)",
          backgroundSize: "48px 48px",
        }}
      />

      {/* 3D scene */}
      <div className="absolute inset-0">
        <Suspense fallback={null}>
          <HeroCanvas />
        </Suspense>
      </div>

      {/* Foreground content */}
      <div className="relative z-10 flex h-full w-full flex-col items-center justify-center px-6 text-center pointer-events-none">
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mb-4 text-sm uppercase tracking-[0.35em] text-accent-cyan/80"
        >
          Premium Electronics Experience
        </motion.p>

        <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-white">
          <SplitText text="THE FUTURE OF" delay={0.3} />
          <br />
          <SplitText text="TECHNOLOGY" delay={0.3 + "THE FUTURE OF".length * 0.03} className="bg-gradient-to-r from-accent-blue via-accent-purple to-accent-cyan bg-clip-text text-transparent" />
        </h1>

        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.4 }}
          className="mt-10 flex gap-4 pointer-events-auto"
        >
          <button className="rounded-full bg-white px-8 py-3 font-medium text-background transition-transform hover:scale-[1.03] active:scale-[0.97]">
            Explore Products
          </button>
          <button className="rounded-full border border-white/20 bg-white/5 px-8 py-3 font-medium text-white backdrop-blur-md transition-transform hover:scale-[1.03] active:scale-[0.97]">
            Watch Experience
          </button>
        </motion.div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2 text-white/40"
      >
        <motion.div
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 1.6, repeat: Infinity, ease: "easeInOut" }}
          className="h-9 w-5 rounded-full border border-white/30 flex justify-center pt-2"
        >
          <div className="h-1.5 w-1 rounded-full bg-white/60" />
        </motion.div>
      </motion.div>
    </section>
  );
}
