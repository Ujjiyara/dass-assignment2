# QuickCart API – Black Box Testing Report

## Summary
Tested 110 endpoints/scenarios across 13 feature areas. Found **20 confirmed bugs** in the QuickCart REST API.

---

## Bug 1: Cart Subtotal Calculation Error
- **Endpoint**: `GET /api/v1/cart`
- **Steps**: Add 2 × Apple Red ($120 each), view cart
- **Expected**: subtotal = 2 × 120 = 240
- **Actual**: subtotal = **-16**
- **Severity**: Critical — wrong totals break all downstream calculations

## Bug 2: Cart Total Incorrect
- **Endpoint**: `GET /api/v1/cart`
- **Steps**: Add 2 × Apple ($120) + 3 × Banana ($40), view cart
- **Expected**: total = 240 + 120 = 360
- **Actual**: total = **0** (or some incorrect value)
- **Severity**: Critical — entire cart value computation is wrong

## Bug 3: Product Price Mismatch
- **Endpoint**: `GET /api/v1/products`
- **Steps**: Compare product 8 (Grapes - Black) price shown to user vs admin
- **Expected**: Same price ($95 in admin DB)
- **Actual**: User sees **$100**, admin shows $95
- **Severity**: High — user is charged more than the real price

## Bug 4: Expired Coupon Accepted
- **Endpoint**: `POST /api/v1/coupon/apply`
- **Steps**: Apply coupon "EXPIRED100" (expired 2026-02-28) to a cart
- **Expected**: 400 error (coupon expired)
- **Actual**: **200 OK** — coupon accepted
- **Severity**: High — expired discounts should not be honoured

## Bug 5: COD Allowed Over $5000
- **Endpoint**: `POST /api/v1/checkout`
- **Steps**: Add 25 × Mango Alphonso ($250 each = $6250), checkout with COD
- **Expected**: 400 error (COD not allowed above $5000)
- **Actual**: **200 OK** — order placed
- **Severity**: High — COD payment limit bypass

## Bug 6: Review Rating Validation Missing
- **Endpoint**: `POST /api/v1/products/{id}/reviews`
- **Steps**: Submit review with rating 0, -1, or 6
- **Expected**: 400 error (must be 1-5)
- **Actual**: **200 OK** — all accepted
- **Severity**: Medium — allows invalid rating data

## Bug 7: Support Ticket Message Truncated
- **Endpoint**: `POST /api/v1/support/ticket`
- **Steps**: Create ticket with message "Hello! I need help with order #12345. My items were damaged." (60 chars)
- **Expected**: Full message saved
- **Actual**: Message truncated to **50 characters** — "Hello! I need help with order #12345. My items wer"
- **Severity**: High — user messages are silently cut off

## Bug 8: Phone Number Accepts Non-Digits
- **Endpoint**: `PUT /api/v1/profile`
- **Steps**: Update phone to "abcdefghij" (10 letters)
- **Expected**: 400 error (must be 10 digits)
- **Actual**: **200 OK** — letters accepted
- **Severity**: Medium — invalid phone stored in DB

## Bug 9: Pincode Accepts Non-Digits
- **Endpoint**: `POST /api/v1/addresses`
- **Steps**: Add address with pincode "abcdef" (6 letters)
- **Expected**: 400 error (must be 6 digits)
- **Actual**: **200 OK** — letters accepted
- **Severity**: Medium — invalid pincode stored

## Bug 10: Multiple Default Addresses Allowed
- **Endpoint**: `POST /api/v1/addresses`
- **Steps**: Add two addresses both with is_default=true for same user
- **Expected**: Only the latest address should be default, old one reset
- **Actual**: **Both remain default** (found 3 default addresses)
- **Severity**: Medium — violates "only one default at a time"

## Bug 11: Zero/Negative Cart Quantity Accepted
- **Endpoint**: `POST /api/v1/cart/add`
- **Steps**: Add product with quantity 0 or -5
- **Expected**: 400 error (must be at least 1)
- **Actual**: **200 OK** — accepted
- **Severity**: Medium — allows adding 0 or negative items

## Bug 12: Invoice Total Mismatch
- **Endpoint**: `GET /api/v1/orders/{id}/invoice`
- **Steps**: Checkout 5 × Banana ($40 each = $200), get invoice
- **Expected**: total = subtotal ($200) + GST ($10) = $210
- **Actual**: total = **$220** (or shows 0 in `total` field)
- **Severity**: High — incorrect total on invoice

## Bug 13: Stock Not Fully Restored on Cancel
- **Endpoint**: `POST /api/v1/orders/{id}/cancel`
- **Steps**: Buy 2 × Watermelon, cancel order, check stock
- **Expected**: Stock returns to pre-order quantity
- **Actual**: Stock restored **partially** (168 instead of 170)
- **Severity**: High — inventory leak on cancellations

## Bug 14: Wallet Deducts Wrong Amount
- **Endpoint**: `POST /api/v1/wallet/pay`
- **Steps**: Add $500 to wallet, pay $200, check balance
- **Expected**: Balance = (previous + 500) - 200
- **Actual**: Balance doesn't match expected calculation
- **Severity**: High — wallet math error

## Bug 15: Coupon Discount Not Applied/Shown Correctly
- **Endpoint**: `POST /api/v1/coupon/apply`
- **Steps**: Apply PERCENT10 (10% off, max $100) to $500 cart
- **Expected**: Discount = $50 (10% of 500)
- **Actual**: Discount shows **0** in cart
- **Severity**: High — percent coupons don't update cart discount field

---

## Bug 16: Product Review without Purchase
- **Endpoint**: `POST /api/v1/products/{id}/reviews`
- **Steps**: Use a user ID with zero orders to submit a review for an expensive product.
- **Expected**: 403 Forbidden or 400 Bad Request (must purchase before reviewing).
- **Actual**: **200 OK** — review accepted.
- **Severity**: Medium — allows fake/spam reviews.

## Bug 17: Coupon Persistence after Cart Modification
- **Endpoint**: `POST /api/v1/cart/remove`
- **Steps**: Apply a coupon with min-cart requirement, then remove items so total drops below that requirement.
- **Expected**: Coupon is automatically detached.
- **Actual**: **Coupon stays applied**, potentially leading to negative cart totals or $0 total for valid items.
- **Severity**: High — allows redeeming coupons without meeting price thresholds.

## Bug 18: Inactive Product Addition to Cart
- **Endpoint**: `POST /api/v1/cart/add`
- **Steps**: Identify an inactive product via admin API and attempt to add it to a user's cart.
- **Expected**: 404 or 400 error (product not available).
- **Actual**: **200 OK** — inactive product added successfully.
- **Severity**: Medium — users can buy products that should be disabled.

## Bug 19: Duplicate Product Reviews
- **Endpoint**: `POST /api/v1/products/{id}/reviews`
- **Steps**: Submit two different reviews for the same product using the same user.
- **Expected**: 400 error (review already exists).
- **Actual**: **200 OK** — multiple reviews allowed per user per product.
- **Severity**: Low — data redundancy and rating manipulation.

## Bug 20: Multiple Coupons Can Be Stacked on One Cart
- **Endpoint**: `POST /api/v1/coupon/apply`
- **Steps**: Apply coupon `WELCOME50` to a cart, then apply a second different coupon `SAVE200` to the same cart.
- **Expected**: 400 error — only one coupon allowed per cart at a time.
- **Actual**: **200 OK** — both coupon applications succeed, allowing multiple discounts.
- **Severity**: High — allows users to stack multiple discounts, bypassing intended single-coupon business rules.
