import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";

import { useLogin } from "@/hooks/useAuth";

const schema = z.object({
  email: z.string().email("Enter a valid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

type FormData = z.infer<typeof schema>;

export default function LoginPage() {
  const navigate = useNavigate();
  const login = useLogin();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const onSubmit = (data: FormData) => {
    login.mutate(data, { onSuccess: () => navigate("/") });
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
        <h1 className="mb-1 text-2xl font-semibold text-white">Welcome back</h1>
        <p className="mb-6 text-sm text-white/50">Sign in to your WEBTECH account</p>

        <label className="mb-1 block text-sm text-white/70">Email</label>
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
          disabled={login.isPending}
          className="mt-4 w-full rounded-full bg-white py-2.5 font-medium text-background transition-transform hover:scale-[1.02] disabled:opacity-50"
        >
          {login.isPending ? "Signing in..." : "Sign In"}
        </button>

        <p className="mt-5 text-center text-sm text-white/50">
          Don't have an account?{" "}
          <Link to="/register" className="text-accent-blue hover:underline">
            Create one
          </Link>
        </p>
      </motion.form>
    </div>
  );
}
