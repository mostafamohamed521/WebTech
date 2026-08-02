import { motion } from "framer-motion";

interface SplitTextProps {
  text: string;
  className?: string;
  delay?: number;
}

/**
 * SplitText — characters fade + rise + sharpen in sequence.
 * Matches the WEBTECH animation-system spec: "Split-text reveal.
 * Characters appear sequentially. Small upward motion. Blur to sharp."
 */
export default function SplitText({ text, className = "", delay = 0 }: SplitTextProps) {
  const letters = Array.from(text);

  return (
    <span className={className} aria-label={text}>
      {letters.map((char, i) => (
        <motion.span
          key={`${char}-${i}`}
          aria-hidden="true"
          initial={{ opacity: 0, y: 24, filter: "blur(8px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          transition={{
            duration: 0.6,
            delay: delay + i * 0.03,
            ease: [0.16, 1, 0.3, 1],
          }}
          style={{ display: "inline-block", whiteSpace: "pre" }}
        >
          {char}
        </motion.span>
      ))}
    </span>
  );
}
