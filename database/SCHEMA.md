# WEBTECH — Database Schema (PostgreSQL)

Full database schema (text ERD) per the project specification. Every table uses a UUID primary key + `created_at`/`updated_at` + soft delete, via the shared `common.models.BaseModel`.

> **Status:** all tables below marked with real Django apps (`apps/*/models.py`) are implemented and migrated. This file remains the canonical design reference — the migrations are its concrete realization.

## Auth & Users
- **Users**: id, name, email, phone, password_hash, avatar, role, status, last_login
- **Roles**: id, name (super_admin, admin, manager, support, customer)
- **Permissions**: id, code, description
- **RolePermissions**: role_id, permission_id
- **UserProfiles**: user_id, gender, birth_date, country, city, language, timezone
- **UserAddresses**: user_id, country, city, street, building, apartment, postal_code, lat, lng

## Catalog
- **Categories**: id, name, slug, parent_id (self-FK for sub-categories), image
- **Brands**: id, name, slug, logo
- **Products**: id, name, slug, description, short_description, brand_id, category_id, price, discount_price, cost_price, currency, stock, sku, barcode, weight, warranty, featured, trending, published, seo_title, seo_description
- **ProductImages**: id, product_id, url, is_main, sort_order
- **ProductVideos**: id, product_id, url
- **ProductVariants**: id, product_id, color, storage, ram, size, material, edition, price_difference, stock, image
- **VariantAttributes / VariantValues**: attribute definitions + values for variants
- **Specifications**: id, key (CPU, GPU, RAM, Display...)
- **ProductSpecifications**: product_id, specification_id, value

## Inventory
- **Warehouses**: id, name, address
- **Inventory**: id, product_id, warehouse_id, quantity, reserved_quantity, available_quantity, low_stock_threshold
- **StockMovements**: id, inventory_id, type (purchase/sale/return/adjustment/transfer), quantity, note

## Shopping
- **ShoppingCart**: id, user_id (nullable for guest), session_key, coupon_id, currency
- **CartItems**: id, cart_id, product_id, variant_id, quantity, price
- **Wishlist**: id, user_id
- **WishlistItems**: id, wishlist_id, product_id

## Orders & Payments
- **Orders**: id, order_number, customer_id, address_id, status, payment_status, shipping_status, coupon_id, tax, discount, shipping_cost, grand_total
- **OrderItems**: id, order_id, product_id, variant_id, quantity, unit_price, discount, subtotal
- **OrderStatusHistory**: id, order_id, status, changed_at
- **Payments**: id, order_id, transaction_id, gateway, status, amount, currency, reference
- **PaymentMethods**: id, user_id, type, provider_token

## Marketing & Engagement
- **Coupons**: id, code, type (percentage/fixed), value, expiration, usage_limit, min_purchase
- **CouponUsage**: id, coupon_id, user_id, order_id
- **Reviews**: id, user_id, product_id, rating, comment, verified_purchase, helpful_count
- **ReviewImages**: id, review_id, url
- **ReviewLikes**: id, review_id, user_id

## System
- **Notifications**: id, user_id, title, body, read, priority
- **NotificationSettings**: user_id, email_enabled, push_enabled
- **SupportTickets**: id, user_id, subject, priority, department, status
- **TicketReplies**: id, ticket_id, sender_id, message
- **ActivityLogs**: id, user_id, action, created_at
- **AuditLogs**: id, actor_id, action, target_type, target_id, metadata
- **SystemSettings**: key, value
- **HomepageBanners**: id, image, link, sort_order
- **FeaturedProducts / TrendingProducts**: product_id, sort_order
- **RecentlyViewed**: id, user_id, product_id, viewed_at
- **SearchHistory**: id, user_id, keyword, results_count, timestamp
- **ProductComparison**: id, user_id, product_ids[]

## Indexing
Indexes on: email, phone, sku, barcode, slug, product name, category, brand, order_number (+ composite indexes for common filter/sort combos).

## Notes
- Use Django migrations (`apps/<app>/migrations/`) to materialize this schema — this file is the design reference the migrations must implement.
- Enforce FK cascade behavior per relationship (e.g. deleting a Product should soft-delete related CartItems, not hard-delete Orders history).
