import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { motion, AnimatePresence } from "framer-motion";
import { Trash2, Plus } from "lucide-react";

import { useAddresses, useCreateAddress, useDeleteAddress } from "@/hooks/useAddresses";
import Button from "@/components/ui/Button";

const schema = z.object({
  full_name: z.string().min(2),
  phone: z.string().min(8),
  city: z.string().min(2),
  street: z.string().min(3),
  building: z.string().optional(),
  apartment: z.string().optional(),
});
type FormData = z.infer<typeof schema>;

export default function AddressesPage() {
  const { data: addresses, isLoading } = useAddresses();
  const createAddress = useCreateAddress();
  const deleteAddress = useDeleteAddress();
  const [showForm, setShowForm] = useState(false);

  const { register, handleSubmit, reset, formState: { errors } } = useForm<FormData>({ resolver: zodResolver(schema) });

  const onSubmit = (data: FormData) => {
    createAddress.mutate(
      { ...data, label: "", country: "Egypt", building: data.building ?? "", apartment: data.apartment ?? "", is_default: !addresses?.length },
      { onSuccess: () => { reset(); setShowForm(false); } }
    );
  };

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">My Addresses</h1>
        <Button onClick={() => setShowForm((v) => !v)} size="sm" icon={<Plus size={14} />}>
          Add address
        </Button>
      </div>

      <AnimatePresence>
        {showForm && (
          <motion.form
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            onSubmit={handleSubmit(onSubmit)}
            className="mb-6 grid grid-cols-2 gap-3 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm p-5"
          >
            <input {...register("full_name")} placeholder="Full name" className="col-span-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm" />
            <input {...register("phone")} placeholder="Phone" className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm" />
            <input {...register("city")} placeholder="City" className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm" />
            <input {...register("street")} placeholder="Street" className="col-span-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm" />
            <input {...register("building")} placeholder="Building (optional)" className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm" />
            <input {...register("apartment")} placeholder="Apartment (optional)" className="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm" />
            {(errors.full_name || errors.phone || errors.city || errors.street) && (
              <p className="col-span-2 text-xs text-red-500">Please fill all required fields correctly.</p>
            )}
            <Button type="submit" variant="accent" disabled={createAddress.isPending} fullWidth className="col-span-2 mt-1">
              {createAddress.isPending ? "Saving..." : "Save address"}
            </Button>
          </motion.form>
        )}
      </AnimatePresence>

      {isLoading ? (
        <p className="text-slate-500">Loading addresses...</p>
      ) : !addresses || addresses.length === 0 ? (
        <p className="text-slate-500">No saved addresses yet.</p>
      ) : (
        <div className="grid gap-3 sm:grid-cols-2">
          {addresses.map((addr) => (
            <div key={addr.id} className="relative rounded-xl border border-slate-200 bg-white shadow-sm p-4">
              {addr.is_default && (
                <span className="absolute right-3 top-3 rounded-full bg-accent-blue/15 px-2 py-0.5 text-[10px] text-accent-blue">
                  Default
                </span>
              )}
              <p className="font-medium">{addr.full_name}</p>
              <p className="text-sm text-slate-500">{addr.street}, {addr.city}, {addr.country}</p>
              <p className="text-sm text-slate-500">{addr.phone}</p>
              <button
                onClick={() => deleteAddress.mutate(addr.id)}
                className="mt-3 flex items-center gap-1.5 text-xs text-slate-500 hover:text-red-500"
              >
                <Trash2 size={13} /> Remove
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
