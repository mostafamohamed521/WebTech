import { lazy, Suspense } from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "@/components/layout/Navbar";
import ScrollToTop from "@/components/layout/ScrollToTop";
import CompareBar from "@/components/compare/CompareBar";
import HomePage from "@/pages/Home/HomePage";

// Route-level code splitting: everything except the landing page loads
// on demand. This keeps the initial bundle lean — heavy dependencies
// like Three.js (product viewer) and Recharts (admin charts) only
// download when a person actually navigates to a page that needs them.
const LoginPage = lazy(() => import("@/pages/Auth/LoginPage"));
const RegisterPage = lazy(() => import("@/pages/Auth/RegisterPage"));
const CartPage = lazy(() => import("@/pages/Cart/CartPage"));
const CheckoutPage = lazy(() => import("@/pages/Checkout/CheckoutPage"));
const ProductDetailPage = lazy(() => import("@/pages/Product/ProductDetailPage"));
const CategoryPage = lazy(() => import("@/pages/Category/CategoryPage"));
const SearchResultsPage = lazy(() => import("@/pages/Search/SearchResultsPage"));
const ComparePage = lazy(() => import("@/pages/Compare/ComparePage"));
const SupportPage = lazy(() => import("@/pages/Support/SupportPage"));
const NotFoundPage = lazy(() => import("@/pages/Errors/NotFoundPage"));

const AccountLayout = lazy(() => import("@/components/account/AccountLayout"));
const OverviewPage = lazy(() => import("@/pages/Account/OverviewPage"));
const OrdersListPage = lazy(() => import("@/pages/Account/OrdersListPage"));
const OrderDetailPage = lazy(() => import("@/pages/Account/OrderDetailPage"));
const AddressesPage = lazy(() => import("@/pages/Account/AddressesPage"));
const WishlistPage = lazy(() => import("@/pages/Account/WishlistPage"));
const SettingsPage = lazy(() => import("@/pages/Account/SettingsPage"));

const AdminLayout = lazy(() => import("@/components/admin/AdminLayout"));
const AdminOverviewPage = lazy(() => import("@/pages/Admin/AdminOverviewPage"));
const AdminProductsPage = lazy(() => import("@/pages/Admin/AdminProductsPage"));
const AdminOrdersPage = lazy(() => import("@/pages/Admin/AdminOrdersPage"));
const AdminAnalyticsPage = lazy(() => import("@/pages/Admin/AdminAnalyticsPage"));
const AdminSupportPage = lazy(() => import("@/pages/Admin/AdminSupportPage"));

function RouteFallback() {
  return (
    <div className="flex min-h-[60vh] items-center justify-center bg-background">
      <div className="h-8 w-8 animate-spin rounded-full border-2 border-slate-200 border-t-accent-blue" />
    </div>
  );
}

export default function AppRoutes() {
  return (
    <>
      <ScrollToTop />
      <Navbar />
      <CompareBar />
      <Suspense fallback={<RouteFallback />}>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/checkout" element={<CheckoutPage />} />
          <Route path="/product/:slug" element={<ProductDetailPage />} />
          <Route path="/category/:slug" element={<CategoryPage />} />
          <Route path="/search" element={<SearchResultsPage />} />
          <Route path="/compare" element={<ComparePage />} />
          <Route path="/support" element={<SupportPage />} />

          <Route path="/account" element={<AccountLayout />}>
            <Route index element={<OverviewPage />} />
            <Route path="orders" element={<OrdersListPage />} />
            <Route path="orders/:orderNumber" element={<OrderDetailPage />} />
            <Route path="addresses" element={<AddressesPage />} />
            <Route path="wishlist" element={<WishlistPage />} />
            <Route path="settings" element={<SettingsPage />} />
          </Route>

          <Route path="/admin" element={<AdminLayout />}>
            <Route index element={<AdminOverviewPage />} />
            <Route path="products" element={<AdminProductsPage />} />
            <Route path="orders" element={<AdminOrdersPage />} />
            <Route path="analytics" element={<AdminAnalyticsPage />} />
            <Route path="support" element={<AdminSupportPage />} />
          </Route>

          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Suspense>
    </>
  );
}
