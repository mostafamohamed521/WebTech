import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

import { useRegister } from "@/hooks/useAuth";

const schema = z.object({
  first_name: z.string().min(2, "Too short"),
  username: z.string().min(3, "Too short"),
  email: z.string().email("Enter a valid email address"),
  password: z
    .string()
    .min(8, "At least 8 characters")
    .regex(/[A-Z]/, "Include an uppercase letter")
    .regex(/[0-9]/, "Include a number"),
});

type FormData = z.infer<typeof schema>;

export default function RegisterPage() {
  const navigate = useNavigate();
  const registerUser = useRegister();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const onSubmit = (data: FormData) => {
    registerUser.mutate(data, { onSuccess: () => navigate("/") });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-6">
      <motion.form
        initial={{ opacity: 0, y: 20, filter: "blur(6px)" }}
        animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
        transition={{ duration: 0.5 }}
        onSubmit={handleSubmit(onSubmit)}
        className="w-full max-w-md rounded-2xl border border-white/10 bg-surface/60 p-8 backdrop-blur-xl"
      >
        <h1 className="mb-1 text-2xl font-semibold text-white">Create your account</h1>
        <p className="mb-6 text-sm text-white/50">Join WEBTECH — the future of technology</p>

        <label className="mb-1 block text-sm text-white/70">First name</label>
        <input
          {...register("first_name")}
          className="mb-1 w-full rounded-lg border border-white/10 bg-black/30 px-4 py-2.5 text-white outline-none focus:border-accent-blue"
          placeholder="Mostafa"
        />
        {errors.first_name && <p className="mb-3 text-xs text-red-400">{errors.first_name.message}</p>}

        <label className="mb-1 mt-3 block text-sm text-white/70">Username</label>
        <input
          {...register("username")}
          className="mb-1 w-full rounded-lg border border-white/10 bg-black/30 px-4 py-2.5 text-white outline-none focus:border-accent-blue"
          placeholder="mostafa"
        />
        {errors.username && <p className="mb-3 text-xs text-red-400">{errors.username.message}</p>}

        <label className="mb-1 mt-3 block text-sm text-white/70">Email</label>
        <input
          type="email"
          {...register("email")}
          className="mb-1 w-full rounded-lg border border-white/10 bg-black/30 px-4 py-2.5 text-white outline-none focus:border-accent-blue"
          placeholder="you@example.com"
        />
        {errors.email && <p className="mb-3 text-xs text-red-400">{errors.email.message}</p>}

        <label className="mb-1 mt-3 block text-sm text-white/70">Password</label>
        <input
          type="password"
          {...register("password")}
          className="mb-1 w-full rounded-lg border border-white/10 bg-black/30 px-4 py-2.5 text-white outline-none focus:border-accent-blue"
          placeholder="••••••••"
        />
        {errors.password && <p className="mb-3 text-xs text-red-400">{errors.password.message}</p>}

        <button
          type="submit"
          disabled={registerUser.isPending}
          className="mt-4 w-full rounded-full bg-white py-2.5 font-medium text-background transition-transform hover:scale-[1.02] disabled:opacity-50"
        >
          {registerUser.isPending ? "Creating account..." : "Create Account"}
        </button>

        <p className="mt-5 text-center text-sm text-white/50">
          Already have an account?{" "}
          <Link to="/login" className="text-accent-blue hover:underline">
            Sign in
          </Link>
        </p>
      </motion.form>
    </div>
  );
}
