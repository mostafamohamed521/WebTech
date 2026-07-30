import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { useCart } from "@/hooks/useCart";
import { addressService } from "@/services/addressService";
import { orderService } from "@/services/orderService";

const addressSchema = z.object({
  full_name: z.string().min(2),
  phone: z.string().min(8),
  city: z.string().min(2),
  street: z.string().min(3),
  building: z.string().optional(),
  apartment: z.string().optional(),
});

type AddressForm = z.infer<typeof addressSchema>;

export default function CheckoutPage() {
  const navigate = useNavigate();
  const qc = useQueryClient();
  const { data: cart } = useCart();
  const { data: addresses, isLoading: loadingAddresses } = useQuery({
    queryKey: ["addresses"],
    queryFn: addressService.list,
  });

  const [selectedAddressId, setSelectedAddressId] = useState<string | null>(null);
  const [paymentMethod, setPaymentMethod] = useState<"cod" | "stripe" | "paypal">("cod");

  const { register, handleSubmit, formState: { errors } } = useForm<AddressForm>({
    resolver: zodResolver(addressSchema),
  });

  const createAddress = useMutation({
    mutationFn: (data: AddressForm) =>
      addressService.create({ ...data, label: "", country: "Egypt", building: data.building ?? "", apartment: data.apartment ?? "", is_default: true }),
    onSuccess: (address) => {
      qc.invalidateQueries({ queryKey: ["addresses"] });
      setSelectedAddressId(address.id);
      toast.success("Address saved");
    },
  });

  const checkout = useMutation({
    mutationFn: () => {
      if (!selectedAddressId) throw new Error("no-address");
      return orderService.checkout({ address_id: selectedAddressId, payment_method: paymentMethod });
    },
    onSuccess: (order) => {
      qc.invalidateQueries({ queryKey: ["cart"] });
      toast.success(`Order ${order.order_number} placed!`);
      navigate(`/account/orders/${order.order_number}`);
    },
    onError: () => toast.error("Could not place order — check your address and cart."),
  });

  const subtotal = cart?.subtotal ?? 0;

  return (
    <div className="min-h-screen bg-background px-6 pb-24 pt-32 text-white md:px-16">
      <h1 className="mb-10 text-3xl font-semibold">Checkout</h1>

      <div className="grid gap-10 lg:grid-cols-[1fr_360px]">
        <div className="flex flex-col gap-8">
          {/* Address selection */}
          <section>
            <h2 className="mb-4 text-lg font-medium">Shipping Address</h2>

            {!loadingAddresses && addresses && addresses.length > 0 && (
              <div className="mb-4 flex flex-col gap-2">
                {addresses.map((addr) => (
                  <label
                    key={addr.id}
                    className={`flex cursor-pointer items-start gap-3 rounded-xl border p-4 transition-colors ${
                      selectedAddressId === addr.id ? "border-accent-blue bg-accent-blue/10" : "border-white/10 bg-surface/40"
                    }`}
                  >
                    <input
                      type="radio"
                      name="address"
                      className="mt-1"
                      checked={selectedAddressId === addr.id}
                      onChange={() => setSelectedAddressId(addr.id)}
                    />
                    <div>
                      <p className="font-medium">{addr.full_name}</p>
                      <p className="text-sm text-white/50">{addr.street}, {addr.city}, {addr.country}</p>
                      <p className="text-sm text-white/50">{addr.phone}</p>
                    </div>
                  </label>
                ))}
              </div>
            )}

            <details className="rounded-xl border border-white/10 bg-surface/30 p-4">
              <summary className="cursor-pointer text-sm text-white/60">+ Add a new address</summary>
              <form
                onSubmit={handleSubmit((data) => createAddress.mutate(data))}
                className="mt-4 grid grid-cols-2 gap-3"
              >
                <input {...register("full_name")} placeholder="Full name" className="col-span-2 rounded-lg border border-white/10 bg-black/30 px-3 py-2" />
                <input {...register("phone")} placeholder="Phone" className="rounded-lg border border-white/10 bg-black/30 px-3 py-2" />
                <input {...register("city")} placeholder="City" className="rounded-lg border border-white/10 bg-black/30 px-3 py-2" />
                <input {...register("street")} placeholder="Street" className="col-span-2 rounded-lg border border-white/10 bg-black/30 px-3 py-2" />
                <input {...register("building")} placeholder="Building (optional)" className="rounded-lg border border-white/10 bg-black/30 px-3 py-2" />
                <input {...register("apartment")} placeholder="Apartment (optional)" className="rounded-lg border border-white/10 bg-black/30 px-3 py-2" />
                {(errors.full_name || errors.phone || errors.city || errors.street) && (
                  <p className="col-span-2 text-xs text-red-400">Please fill all required fields correctly.</p>
                )}
                <button type="submit" className="col-span-2 mt-1 rounded-full bg-white/10 py-2 text-sm hover:bg-white/20">
                  Save address
                </button>
              </form>
            </details>
          </section>

          {/* Payment method */}
          <section>
            <h2 className="mb-4 text-lg font-medium">Payment Method</h2>
            <div className="flex gap-3">
              {(["cod", "stripe", "paypal"] as const).map((method) => (
                <button
                  key={method}
                  onClick={() => setPaymentMethod(method)}
                  className={`rounded-full border px-5 py-2 text-sm transition-colors ${
                    paymentMethod === method ? "border-accent-blue bg-accent-blue/10" : "border-white/10 text-white/60"
                  }`}
                >
                  {method === "cod" ? "Cash on Delivery" : method === "stripe" ? "Stripe" : "PayPal"}
                </button>
              ))}
            </div>
            {paymentMethod !== "cod" && (
              <p className="mt-2 text-xs text-white/40">Online gateway integration is a pluggable TODO in PaymentService — COD is fully functional today.</p>
            )}
          </section>
        </div>

        {/* Summary */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="h-fit rounded-2xl border border-white/10 bg-surface/50 p-6"
        >
          <h2 className="mb-4 text-lg font-medium">Order Summary</h2>
          <div className="flex justify-between text-sm text-white/60">
            <span>Subtotal</span>
            <span>{subtotal} EGP</span>
          </div>
          <p className="mt-1 text-xs text-white/30">Tax (14%) and shipping (50 EGP) added at checkout</p>

          <button
            onClick={() => checkout.mutate()}
            disabled={!selectedAddressId || checkout.isPending}
            className="mt-6 w-full rounded-full bg-white py-3 font-medium text-background transition-transform hover:scale-[1.02] disabled:opacity-40"
          >
            {checkout.isPending ? "Placing order..." : "Place Order"}
          </button>
        </motion.div>
      </div>
    </div>
  );
}
