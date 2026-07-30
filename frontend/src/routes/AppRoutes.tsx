import { Routes, Route } from "react-router-dom";
import Navbar from "@/components/layout/Navbar";
import HomePage from "@/pages/Home/HomePage";
import LoginPage from "@/pages/Auth/LoginPage";
import RegisterPage from "@/pages/Auth/RegisterPage";
import CartPage from "@/pages/Cart/CartPage";
import CheckoutPage from "@/pages/Checkout/CheckoutPage";
import OrderDetailPage from "@/pages/Account/OrderDetailPage";
import ProductDetailPage from "@/pages/Product/ProductDetailPage";
import NotFoundPage from "@/pages/Errors/NotFoundPage";

export default function AppRoutes() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/checkout" element={<CheckoutPage />} />
        <Route path="/account/orders/:orderNumber" element={<OrderDetailPage />} />
        <Route path="/product/:slug" element={<ProductDetailPage />} />
        {/* TODO: category, account dashboard, admin routes */}
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </>
  );
}
