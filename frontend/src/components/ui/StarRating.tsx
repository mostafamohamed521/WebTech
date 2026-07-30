import { Star } from "lucide-react";

interface StarRatingProps {
  value: number;
  onChange?: (value: number) => void;
  size?: number;
}

export default function StarRating({ value, onChange, size = 16 }: StarRatingProps) {
  const interactive = !!onChange;
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map((star) => (
        <button
          key={star}
          type="button"
          disabled={!interactive}
          onClick={() => onChange?.(star)}
          className={interactive ? "cursor-pointer" : "cursor-default"}
        >
          <Star
            size={size}
            fill={star <= value ? "#3B82F6" : "transparent"}
            stroke={star <= value ? "#3B82F6" : "#666"}
          />
        </button>
      ))}
    </div>
  );
}
