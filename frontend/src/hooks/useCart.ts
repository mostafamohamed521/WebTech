import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import { cartService } from "@/services/cartService";

export function useCart() {
  return useQuery({
    queryKey: ["cart"],
    queryFn: cartService.getCart,
  });
}

export function useAddToCart() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ productId, quantity, variantId }: { productId: string; quantity?: number; variantId?: string }) =>
      cartService.addItem(productId, quantity, variantId),
    onSuccess: (cart) => {
      qc.setQueryData(["cart"], cart);
      toast.success("Added to cart");
    },
    onError: () => toast.error("Could not add item to cart"),
  });
}

export function useUpdateCartItem() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ itemId, quantity }: { itemId: string; quantity: number }) => cartService.updateItem(itemId, quantity),
    onSuccess: (cart) => qc.setQueryData(["cart"], cart),
  });
}

export function useRemoveCartItem() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (itemId: string) => cartService.removeItem(itemId),
    onSuccess: (cart) => qc.setQueryData(["cart"], cart),
  });
}
