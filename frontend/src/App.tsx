import { useState } from "react";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "react-hot-toast";
import AppRoutes from "./routes/AppRoutes";
import WelcomeSplash, { shouldShowWelcome } from "@/components/layout/WelcomeSplash";

const queryClient = new QueryClient();

export default function App() {
  const [showWelcome, setShowWelcome] = useState(shouldShowWelcome);

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {showWelcome && <WelcomeSplash onDone={() => setShowWelcome(false)} />}
        <AppRoutes />
        <Toaster position="top-center" />
      </BrowserRouter>
    </QueryClientProvider>
  );
}
