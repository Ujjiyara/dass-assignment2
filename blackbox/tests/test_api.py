"""
Black Box API Tests for QuickCart REST API
"""
import pytest
import requests

BASE = "http://localhost:8080/api/v1"
ROLL = "2024115005"
HEADERS = {"X-Roll-Number": ROLL}
USER1 = {**HEADERS, "X-User-ID": "1"}
USER2 = {**HEADERS, "X-User-ID": "2"}
USER7 = {**HEADERS, "X-User-ID": "7"}  # has high wallet balance

# ═══════════════════════════════════════════════
# AUTHENTICATION & HEADER TESTS
# ═══════════════════════════════════════════════

class TestHeaders:
    def test_missing_roll_number(self):
        r = requests.get(f"{BASE}/admin/users")
        assert r.status_code == 401

    def test_invalid_roll_number(self):
        r = requests.get(f"{BASE}/admin/users", headers={"X-Roll-Number": "abc"})
        assert r.status_code == 400

    def test_valid_roll_number(self):
        r = requests.get(f"{BASE}/admin/users", headers=HEADERS)
        assert r.status_code == 200

    def test_missing_user_id_on_user_endpoint(self):
        r = requests.get(f"{BASE}/profile", headers=HEADERS)
        assert r.status_code == 400

    def test_invalid_user_id(self):
        h = {**HEADERS, "X-User-ID": "abc"}
        r = requests.get(f"{BASE}/profile", headers=h)
        assert r.status_code == 400

    def test_nonexistent_user_id(self):
        h = {**HEADERS, "X-User-ID": "99999"}
        r = requests.get(f"{BASE}/profile", headers=h)
        assert r.status_code in [400, 404]


# ═══════════════════════════════════════════════
# ADMIN ENDPOINTS
# ═══════════════════════════════════════════════

class TestAdmin:
    def test_get_all_users(self):
        r = requests.get(f"{BASE}/admin/users", headers=HEADERS)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "user_id" in data[0]

    def test_get_single_user(self):
        r = requests.get(f"{BASE}/admin/users/1", headers=HEADERS)
        assert r.status_code == 200
        data = r.json()
        assert data["user_id"] == 1

    def test_get_nonexistent_user(self):
        r = requests.get(f"{BASE}/admin/users/99999", headers=HEADERS)
        assert r.status_code == 404

    def test_get_all_products(self):
        r = requests.get(f"{BASE}/admin/products", headers=HEADERS)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)

    def test_get_all_carts(self):
        r = requests.get(f"{BASE}/admin/carts", headers=HEADERS)
        assert r.status_code == 200

    def test_get_all_orders(self):
        r = requests.get(f"{BASE}/admin/orders", headers=HEADERS)
        assert r.status_code == 200

    def test_get_all_coupons(self):
        r = requests.get(f"{BASE}/admin/coupons", headers=HEADERS)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)

    def test_get_all_tickets(self):
        r = requests.get(f"{BASE}/admin/tickets", headers=HEADERS)
        assert r.status_code == 200

    def test_get_all_addresses(self):
        r = requests.get(f"{BASE}/admin/addresses", headers=HEADERS)
        assert r.status_code == 200


# ═══════════════════════════════════════════════
# PROFILE
# ═══════════════════════════════════════════════

class TestProfile:
    def test_get_profile(self):
        r = requests.get(f"{BASE}/profile", headers=USER1)
        assert r.status_code == 200
        data = r.json()
        assert "name" in data
        assert "email" in data

    def test_update_profile_valid(self):
        r = requests.put(f"{BASE}/profile", headers=USER1,
                         json={"name": "Anita Updated", "phone": "9876543210"})
        assert r.status_code == 200

    def test_update_name_too_short(self):
        r = requests.put(f"{BASE}/profile", headers=USER1,
                         json={"name": "A", "phone": "9876543210"})
        assert r.status_code == 400

    def test_update_name_too_long(self):
        r = requests.put(f"{BASE}/profile", headers=USER1,
                         json={"name": "A" * 51, "phone": "9876543210"})
        assert r.status_code == 400

    def test_update_phone_wrong_length(self):
        r = requests.put(f"{BASE}/profile", headers=USER1,
                         json={"name": "Anita Johnson", "phone": "123"})
        assert r.status_code == 400

    def test_update_phone_not_digits(self):
        r = requests.put(f"{BASE}/profile", headers=USER1,
                         json={"name": "Anita Johnson", "phone": "abcdefghij"})
        assert r.status_code == 400


# ═══════════════════════════════════════════════
# ADDRESSES
# ═══════════════════════════════════════════════

class TestAddresses:
    def test_get_addresses(self):
        r = requests.get(f"{BASE}/addresses", headers=USER1)
        assert r.status_code == 200

    def test_add_address_valid(self):
        r = requests.post(f"{BASE}/addresses", headers=USER1, json={
            "label": "HOME",
            "street": "123 Main Street",
            "city": "Hyderabad",
            "pincode": "500001",
            "is_default": False
        })
        assert r.status_code in [200, 201]
        data = r.json()
        assert "address_id" in data or ("address" in data and "address_id" in data["address"])

    def test_add_address_invalid_label(self):
        r = requests.post(f"{BASE}/addresses", headers=USER1, json={
            "label": "SHOP",
            "street": "123 Main Street",
            "city": "Hyderabad",
            "pincode": "500001"
        })
        assert r.status_code == 400

    def test_add_address_short_street(self):
        r = requests.post(f"{BASE}/addresses", headers=USER1, json={
            "label": "HOME",
            "street": "Hi",
            "city": "Hyderabad",
            "pincode": "500001"
        })
        assert r.status_code == 400

    def test_add_address_short_city(self):
        r = requests.post(f"{BASE}/addresses", headers=USER1, json={
            "label": "HOME",
            "street": "123 Main Street",
            "city": "H",
            "pincode": "500001"
        })
        assert r.status_code == 400

    def test_add_address_invalid_pincode(self):
        r = requests.post(f"{BASE}/addresses", headers=USER1, json={
            "label": "HOME",
            "street": "123 Main Street",
            "city": "Hyderabad",
            "pincode": "123"
        })
        assert r.status_code == 400

    def test_add_address_pincode_not_digits(self):
        r = requests.post(f"{BASE}/addresses", headers=USER1, json={
            "label": "HOME",
            "street": "123 Main Street",
            "city": "Hyderabad",
            "pincode": "abcdef"
        })
        assert r.status_code == 400

    def test_delete_nonexistent_address(self):
        r = requests.delete(f"{BASE}/addresses/99999", headers=USER1)
        assert r.status_code == 404

    def test_default_address_uniqueness(self):
        # Add first as default
        r1 = requests.post(f"{BASE}/addresses", headers=USER2, json={
            "label": "HOME",
            "street": "First Default Street",
            "city": "Mumbai",
            "pincode": "400001",
            "is_default": True
        })
        assert r1.status_code in [200, 201]

        # Add second as default
        r2 = requests.post(f"{BASE}/addresses", headers=USER2, json={
            "label": "OFFICE",
            "street": "Second Default Street",
            "city": "Mumbai",
            "pincode": "400002",
            "is_default": True
        })
        assert r2.status_code in [200, 201]

        # Check only one is default
        r3 = requests.get(f"{BASE}/addresses", headers=USER2)
        addrs = r3.json()
        defaults = [a for a in addrs if a.get("is_default")]
        assert len(defaults) <= 1, f"BUG: Multiple default addresses found: {len(defaults)}"

    def test_update_address_returns_new_data(self):
        # Add an address first
        r1 = requests.post(f"{BASE}/addresses", headers=USER1, json={
            "label": "OTHER",
            "street": "Old Street Name Here",
            "city": "Delhi",
            "pincode": "110001",
            "is_default": False
        })
        data1 = r1.json()
        addr_id = data1.get("address_id") or data1.get("address", {}).get("address_id")

        if addr_id:
            r2 = requests.put(f"{BASE}/addresses/{addr_id}", headers=USER1,
                              json={"street": "New Updated Street"})
            assert r2.status_code == 200
            data2 = r2.json()
            # The returned data should show the NEW street
            addr_data = data2.get("address", data2)
            assert "New Updated Street" in str(addr_data), \
                f"BUG: Update returned old data instead of new: {addr_data}"


# ═══════════════════════════════════════════════
# PRODUCTS
# ═══════════════════════════════════════════════

class TestProducts:
    def test_get_all_products(self):
        r = requests.get(f"{BASE}/products", headers=USER1)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)

    def test_products_only_active(self):
        # User endpoint should NOT show inactive products
        user_prods = requests.get(f"{BASE}/products", headers=USER1).json()
        admin_prods = requests.get(f"{BASE}/admin/products", headers=HEADERS).json()
        inactive = [p for p in admin_prods if not p["is_active"]]
        if inactive:
            inactive_ids = {p["product_id"] for p in inactive}
            user_ids = {p["product_id"] for p in user_prods}
            overlap = inactive_ids & user_ids
            assert len(overlap) == 0, \
                f"BUG: Inactive products shown to user: {overlap}"

    def test_get_single_product(self):
        r = requests.get(f"{BASE}/products/1", headers=USER1)
        assert r.status_code == 200
        data = r.json()
        assert data["product_id"] == 1

    def test_get_nonexistent_product(self):
        r = requests.get(f"{BASE}/products/99999", headers=USER1)
        assert r.status_code == 404

    def test_filter_by_category(self):
        r = requests.get(f"{BASE}/products", headers=USER1, params={"category": "Fruits"})
        assert r.status_code == 200
        data = r.json()
        for p in data:
            assert p["category"] == "Fruits"

    def test_sort_by_price_asc(self):
        r = requests.get(f"{BASE}/products", headers=USER1, params={"sort": "price_asc"})
        assert r.status_code == 200
        data = r.json()
        prices = [p["price"] for p in data]
        assert prices == sorted(prices), "BUG: Products not sorted ascending by price"

    def test_sort_by_price_desc(self):
        r = requests.get(f"{BASE}/products", headers=USER1, params={"sort": "price_desc"})
        assert r.status_code == 200
        data = r.json()
        prices = [p["price"] for p in data]
        assert prices == sorted(prices, reverse=True), "BUG: Products not sorted descending"

    def test_search_by_name(self):
        r = requests.get(f"{BASE}/products", headers=USER1, params={"search": "Apple"})
        assert r.status_code == 200
        data = r.json()
        if len(data) > 0:
            # If the API returns filtered results, all should contain 'apple'
            # BUG CHECK: API might ignore the search param entirely
            apple_count = sum(1 for p in data if "apple" in p["name"].lower())
            assert apple_count > 0, "BUG: No Apple products returned in search"

    def test_product_price_matches_admin(self):
        """Prices shown to user must match the real DB price."""
        admin_prods = requests.get(f"{BASE}/admin/products", headers=HEADERS).json()
        user_prods = requests.get(f"{BASE}/products", headers=USER1).json()
        admin_map = {p["product_id"]: p["price"] for p in admin_prods}
        for p in user_prods:
            expected = admin_map.get(p["product_id"])
            if expected is not None:
                assert p["price"] == expected, \
                    f"BUG: Product {p['product_id']} price mismatch: got {p['price']}, expected {expected}"


# ═══════════════════════════════════════════════
# CART
# ═══════════════════════════════════════════════

class TestCart:
    def setup_method(self):
        """Clear cart before each test."""
        requests.delete(f"{BASE}/cart/clear", headers=USER1)

    def test_get_empty_cart(self):
        r = requests.get(f"{BASE}/cart", headers=USER1)
        assert r.status_code == 200

    def test_add_item_to_cart(self):
        r = requests.post(f"{BASE}/cart/add", headers=USER1,
                          json={"product_id": 1, "quantity": 2})
        assert r.status_code == 200

    def test_add_item_zero_quantity(self):
        r = requests.post(f"{BASE}/cart/add", headers=USER1,
                          json={"product_id": 1, "quantity": 0})
        assert r.status_code == 400

    def test_add_item_negative_quantity(self):
        r = requests.post(f"{BASE}/cart/add", headers=USER1,
                          json={"product_id": 1, "quantity": -5})
        assert r.status_code == 400

    def test_add_nonexistent_product(self):
        r = requests.post(f"{BASE}/cart/add", headers=USER1,
                          json={"product_id": 99999, "quantity": 1})
        assert r.status_code == 404

    def test_add_exceeds_stock(self):
        r = requests.post(f"{BASE}/cart/add", headers=USER1,
                          json={"product_id": 1, "quantity": 999999})
        assert r.status_code == 400

    def test_add_same_product_twice_adds_quantities(self):
        """Adding the same product twice should ADD quantities, not replace."""
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 3, "quantity": 2})
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 3, "quantity": 3})
        r = requests.get(f"{BASE}/cart", headers=USER1)
        cart = r.json()
        items = cart.get("items", cart.get("cart_items", []))
        prod3 = [i for i in items if i.get("product_id") == 3]
        assert len(prod3) == 1
        assert prod3[0]["quantity"] == 5, \
            f"BUG: Quantity should be 2+3=5, got {prod3[0]['quantity']}"

    def test_update_cart_item(self):
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 1, "quantity": 2})
        r = requests.post(f"{BASE}/cart/update", headers=USER1,
                          json={"product_id": 1, "quantity": 5})
        assert r.status_code == 200

    def test_update_cart_zero_quantity(self):
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 1, "quantity": 2})
        r = requests.post(f"{BASE}/cart/update", headers=USER1,
                          json={"product_id": 1, "quantity": 0})
        assert r.status_code == 400

    def test_remove_item(self):
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 1, "quantity": 2})
        r = requests.post(f"{BASE}/cart/remove", headers=USER1,
                          json={"product_id": 1})
        assert r.status_code == 200

    def test_remove_item_not_in_cart(self):
        r = requests.post(f"{BASE}/cart/remove", headers=USER1,
                          json={"product_id": 99999})
        assert r.status_code == 404

    def test_cart_subtotals_correct(self):
        """Each item subtotal should be quantity * unit price."""
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 1, "quantity": 3})
        r = requests.get(f"{BASE}/cart", headers=USER1)
        cart = r.json()
        items = cart.get("items", cart.get("cart_items", []))
        for item in items:
            if item.get("product_id") == 1:
                expected = item["quantity"] * item.get("unit_price", item.get("price", 0))
                assert item.get("subtotal", item.get("total", 0)) == expected, \
                    f"BUG: Subtotal mismatch: {item}"

    def test_cart_total_correct(self):
        """Cart total must be sum of all item subtotals."""
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 1, "quantity": 2})
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 3, "quantity": 3})
        r = requests.get(f"{BASE}/cart", headers=USER1)
        cart = r.json()
        items = cart.get("items", cart.get("cart_items", []))
        expected_total = sum(i.get("subtotal", i.get("total", 0)) for i in items)
        actual_total = cart.get("total", cart.get("cart_total", 0))
        assert actual_total == expected_total, \
            f"BUG: Cart total {actual_total} != sum of subtotals {expected_total}"

    def test_clear_cart(self):
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 1, "quantity": 1})
        r = requests.delete(f"{BASE}/cart/clear", headers=USER1)
        assert r.status_code == 200


# ═══════════════════════════════════════════════
# COUPONS
# ═══════════════════════════════════════════════

class TestCoupons:
    def setup_method(self):
        requests.delete(f"{BASE}/cart/clear", headers=USER1)
        requests.post(f"{BASE}/coupon/remove", headers=USER1)

    def test_apply_expired_coupon(self):
        """Expired coupons should be rejected."""
        # EXPIRED100 expired 2026-02-28
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 1, "quantity": 10})
        r = requests.post(f"{BASE}/coupon/apply", headers=USER1,
                          json={"coupon_code": "EXPIRED100"})
        assert r.status_code == 400, f"BUG: Expired coupon accepted! Status: {r.status_code}"

    def test_apply_valid_coupon(self):
        # WELCOME50 is FIXED 50, min 100, expires 2026-06-03
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 1, "quantity": 2})  # 240
        r = requests.post(f"{BASE}/coupon/apply", headers=USER1,
                          json={"coupon_code": "WELCOME50"})
        assert r.status_code == 200

    def test_apply_coupon_below_min_cart(self):
        # WELCOME50 min_cart_value=100, add item worth < 100
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 9, "quantity": 1})  # Watermelon 30
        r = requests.post(f"{BASE}/coupon/apply", headers=USER1,
                          json={"coupon_code": "WELCOME50"})
        assert r.status_code == 400

    def test_percent_coupon_discount_correct(self):
        """PERCENT coupon should take percentage off, capped by max_discount."""
        # PERCENT10: 10% off, min 300, max 100
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 5, "quantity": 2})  # Alphonso 250*2=500
        r = requests.post(f"{BASE}/coupon/apply", headers=USER1,
                          json={"coupon_code": "PERCENT10"})
        assert r.status_code == 200
        cart = requests.get(f"{BASE}/cart", headers=USER1).json()
        # 10% of 500 = 50, max cap 100, so discount should be 50
        discount = cart.get("discount", cart.get("coupon_discount", 0))
        assert discount == 50, f"BUG: Expected discount 50, got {discount}"

    def test_percent_coupon_capped(self):
        """When % discount exceeds max_discount, it should be capped."""
        # PERCENT10: 10% off, max 100. Cart = 2000 -> 10% = 200 but cap is 100
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 5, "quantity": 8})  # 250*8=2000
        r = requests.post(f"{BASE}/coupon/apply", headers=USER1,
                          json={"coupon_code": "PERCENT10"})
        assert r.status_code == 200
        cart = requests.get(f"{BASE}/cart", headers=USER1).json()
        discount = cart.get("discount", cart.get("coupon_discount", 0))
        assert discount == 100, f"BUG: Expected capped discount 100, got {discount}"

    def test_remove_coupon(self):
        requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": 1, "quantity": 2})
        requests.post(f"{BASE}/coupon/apply", headers=USER1,
                      json={"coupon_code": "WELCOME50"})
        r = requests.post(f"{BASE}/coupon/remove", headers=USER1)
        assert r.status_code == 200


# ═══════════════════════════════════════════════
# CHECKOUT
# ═══════════════════════════════════════════════

class TestCheckout:
    def setup_method(self):
        requests.delete(f"{BASE}/cart/clear", headers=USER7)

    def test_checkout_empty_cart(self):
        r = requests.post(f"{BASE}/checkout", headers=USER7,
                          json={"payment_method": "COD"})
        assert r.status_code == 400

    def test_checkout_invalid_payment(self):
        requests.post(f"{BASE}/cart/add", headers=USER7,
                      json={"product_id": 1, "quantity": 1})
        r = requests.post(f"{BASE}/checkout", headers=USER7,
                          json={"payment_method": "BITCOIN"})
        assert r.status_code == 400

    def test_checkout_cod(self):
        requests.post(f"{BASE}/cart/add", headers=USER7,
                      json={"product_id": 9, "quantity": 1})  # Watermelon 30
        r = requests.post(f"{BASE}/checkout", headers=USER7,
                          json={"payment_method": "COD"})
        assert r.status_code == 200
        data = r.json()
        order = data.get("order", data)
        assert order.get("payment_status") == "PENDING", \
            f"BUG: COD should start as PENDING, got {order.get('payment_status')}"

    def test_checkout_card(self):
        requests.post(f"{BASE}/cart/add", headers=USER7,
                      json={"product_id": 9, "quantity": 1})
        r = requests.post(f"{BASE}/checkout", headers=USER7,
                          json={"payment_method": "CARD"})
        assert r.status_code == 200
        data = r.json()
        order = data.get("order", data)
        assert order.get("payment_status") == "PAID", \
            f"BUG: CARD should start as PAID, got {order.get('payment_status')}"

    def test_cod_over_5000_rejected(self):
        """COD not allowed if order total > 5000."""
        requests.post(f"{BASE}/cart/add", headers=USER7,
                      json={"product_id": 5, "quantity": 25})  # 250*25=6250
        r = requests.post(f"{BASE}/checkout", headers=USER7,
                          json={"payment_method": "COD"})
        assert r.status_code == 400, \
            f"BUG: COD should be rejected for orders > 5000, got {r.status_code}"

    def test_gst_applied_correctly(self):
        """GST is 5% added only once."""
        requests.post(f"{BASE}/cart/add", headers=USER7,
                      json={"product_id": 1, "quantity": 10})  # 120*10=1200
        r = requests.post(f"{BASE}/checkout", headers=USER7,
                          json={"payment_method": "CARD"})
        assert r.status_code == 200
        data = r.json()
        order = data.get("order", data)
        total = order.get("total", order.get("order_total", 0))
        # 1200 + 5% GST = 1260
        assert total == 1260 or total == 1200 * 1.05, \
            f"BUG: Expected total 1260 (1200 + 5% GST), got {total}"


# ═══════════════════════════════════════════════
# WALLET
# ═══════════════════════════════════════════════

class TestWallet:
    def test_get_wallet(self):
        r = requests.get(f"{BASE}/wallet", headers=USER1)
        assert r.status_code == 200
        data = r.json()
        assert "balance" in data or "wallet_balance" in data

    def test_add_money_valid(self):
        r = requests.post(f"{BASE}/wallet/add", headers=USER1,
                          json={"amount": 100})
        assert r.status_code == 200

    def test_add_money_zero(self):
        r = requests.post(f"{BASE}/wallet/add", headers=USER1,
                          json={"amount": 0})
        assert r.status_code == 400

    def test_add_money_negative(self):
        r = requests.post(f"{BASE}/wallet/add", headers=USER1,
                          json={"amount": -50})
        assert r.status_code == 400

    def test_add_money_over_limit(self):
        r = requests.post(f"{BASE}/wallet/add", headers=USER1,
                          json={"amount": 100001})
        assert r.status_code == 400

    def test_add_money_max_boundary(self):
        r = requests.post(f"{BASE}/wallet/add", headers=USER1,
                          json={"amount": 100000})
        assert r.status_code == 200

    def test_pay_insufficient_balance(self):
        r = requests.post(f"{BASE}/wallet/pay", headers=USER1,
                          json={"amount": 9999999})
        assert r.status_code == 400

    def test_pay_zero(self):
        r = requests.post(f"{BASE}/wallet/pay", headers=USER1,
                          json={"amount": 0})
        assert r.status_code == 400

    def test_pay_exact_deduction(self):
        """Wallet must deduct the exact amount, not more."""
        # Get current balance
        bal_before = requests.get(f"{BASE}/wallet", headers=USER1).json()
        before = bal_before.get("balance", bal_before.get("wallet_balance", 0))
        # Add money to be safe
        requests.post(f"{BASE}/wallet/add", headers=USER1, json={"amount": 500})
        bal_after_add = requests.get(f"{BASE}/wallet", headers=USER1).json()
        after_add = bal_after_add.get("balance", bal_after_add.get("wallet_balance", 0))
        # Pay 200
        requests.post(f"{BASE}/wallet/pay", headers=USER1, json={"amount": 200})
        bal_after_pay = requests.get(f"{BASE}/wallet", headers=USER1).json()
        after_pay = bal_after_pay.get("balance", bal_after_pay.get("wallet_balance", 0))
        assert abs(after_pay - (after_add - 200)) < 0.01, \
            f"BUG: Wallet deducted wrong amount. Expected {after_add - 200}, got {after_pay}"


# ═══════════════════════════════════════════════
# LOYALTY POINTS
# ═══════════════════════════════════════════════

class TestLoyalty:
    def test_get_loyalty(self):
        r = requests.get(f"{BASE}/loyalty", headers=USER1)
        assert r.status_code == 200

    def test_redeem_zero(self):
        r = requests.post(f"{BASE}/loyalty/redeem", headers=USER1,
                          json={"points": 0})
        assert r.status_code == 400

    def test_redeem_more_than_available(self):
        loyalty = requests.get(f"{BASE}/loyalty", headers=USER1).json()
        pts = loyalty.get("points", loyalty.get("loyalty_points", 0))
        r = requests.post(f"{BASE}/loyalty/redeem", headers=USER1,
                          json={"points": pts + 10000})
        assert r.status_code == 400

    def test_redeem_valid(self):
        loyalty = requests.get(f"{BASE}/loyalty", headers=USER1).json()
        pts = loyalty.get("points", loyalty.get("loyalty_points", 0))
        if pts >= 1:
            r = requests.post(f"{BASE}/loyalty/redeem", headers=USER1,
                              json={"points": 1})
            assert r.status_code == 200


# ═══════════════════════════════════════════════
# ORDERS
# ═══════════════════════════════════════════════

class TestOrders:
    def test_get_orders(self):
        r = requests.get(f"{BASE}/orders", headers=USER7)
        assert r.status_code == 200

    def test_get_nonexistent_order(self):
        r = requests.get(f"{BASE}/orders/99999", headers=USER7)
        assert r.status_code == 404

    def test_cancel_nonexistent_order(self):
        r = requests.post(f"{BASE}/orders/99999/cancel", headers=USER7)
        assert r.status_code == 404

    def test_cancel_order_restores_stock(self):
        """When cancelled, items must be added back to stock."""
        # Get initial stock
        prod = requests.get(f"{BASE}/products/9", headers=USER7).json()
        initial_stock = prod["stock_quantity"]

        # Add to cart and checkout
        requests.delete(f"{BASE}/cart/clear", headers=USER7)
        requests.post(f"{BASE}/cart/add", headers=USER7,
                      json={"product_id": 9, "quantity": 2})
        r = requests.post(f"{BASE}/checkout", headers=USER7,
                          json={"payment_method": "CARD"})
        if r.status_code == 200:
            data = r.json()
            order = data.get("order", data)
            order_id = order.get("order_id")

            # Check stock decreased
            prod_after = requests.get(f"{BASE}/products/9", headers=USER7).json()
            assert prod_after["stock_quantity"] == initial_stock - 2

            # Cancel the order
            r2 = requests.post(f"{BASE}/orders/{order_id}/cancel", headers=USER7)
            if r2.status_code == 200:
                # Stock must be restored
                prod_restored = requests.get(f"{BASE}/products/9", headers=USER7).json()
                assert prod_restored["stock_quantity"] == initial_stock, \
                    f"BUG: Stock not restored after cancel. Expected {initial_stock}, got {prod_restored['stock_quantity']}"

    def test_invoice_totals_correct(self):
        """Invoice subtotal + GST = total."""
        requests.delete(f"{BASE}/cart/clear", headers=USER7)
        requests.post(f"{BASE}/cart/add", headers=USER7,
                      json={"product_id": 3, "quantity": 5})  # Banana 40*5=200
        r = requests.post(f"{BASE}/checkout", headers=USER7,
                          json={"payment_method": "CARD"})
        if r.status_code == 200:
            data = r.json()
            order = data.get("order", data)
            order_id = order.get("order_id")
            inv = requests.get(f"{BASE}/orders/{order_id}/invoice", headers=USER7)
            if inv.status_code == 200:
                invoice = inv.json()
                subtotal = invoice.get("subtotal", 0)
                gst = invoice.get("gst", invoice.get("gst_amount", 0))
                total = invoice.get("total", 0)
                assert abs(total - (subtotal + gst)) < 0.01, \
                    f"BUG: Invoice total {total} != subtotal {subtotal} + GST {gst}"


# ═══════════════════════════════════════════════
# REVIEWS
# ═══════════════════════════════════════════════

class TestReviews:
    def test_get_reviews(self):
        r = requests.get(f"{BASE}/products/1/reviews", headers=USER1)
        assert r.status_code == 200

    def test_add_review_valid(self):
        r = requests.post(f"{BASE}/products/1/reviews", headers=USER1,
                          json={"rating": 4, "comment": "Good quality apples"})
        assert r.status_code in [200, 201]

    def test_add_review_rating_zero(self):
        r = requests.post(f"{BASE}/products/1/reviews", headers=USER1,
                          json={"rating": 0, "comment": "Terrible"})
        assert r.status_code == 400

    def test_add_review_rating_six(self):
        r = requests.post(f"{BASE}/products/1/reviews", headers=USER1,
                          json={"rating": 6, "comment": "Amazing"})
        assert r.status_code == 400

    def test_add_review_negative_rating(self):
        r = requests.post(f"{BASE}/products/1/reviews", headers=USER1,
                          json={"rating": -1, "comment": "Bad"})
        assert r.status_code == 400

    def test_add_review_empty_comment(self):
        r = requests.post(f"{BASE}/products/1/reviews", headers=USER1,
                          json={"rating": 3, "comment": ""})
        assert r.status_code == 400

    def test_add_review_comment_too_long(self):
        r = requests.post(f"{BASE}/products/1/reviews", headers=USER1,
                          json={"rating": 3, "comment": "x" * 201})
        assert r.status_code == 400

    def test_review_average_is_decimal(self):
        """Average rating must be proper decimal, not rounded-down int."""
        # Add reviews with different ratings
        requests.post(f"{BASE}/products/2/reviews", headers=USER1,
                      json={"rating": 3, "comment": "Okay apple"})
        requests.post(f"{BASE}/products/2/reviews", headers=USER2,
                      json={"rating": 4, "comment": "Pretty good"})
        r = requests.get(f"{BASE}/products/2/reviews", headers=USER1)
        data = r.json()
        avg = data.get("average_rating", data.get("avg_rating", 0))
        # If both reviews exist, average should be 3.5, not 3
        if isinstance(avg, float) and avg > 0:
            assert avg != int(avg) or avg == 5.0 or avg == 1.0, \
                f"BUG: Average rating {avg} looks like rounded-down integer"


# ═══════════════════════════════════════════════
# SUPPORT TICKETS
# ═══════════════════════════════════════════════

class TestSupportTickets:
    def test_create_ticket(self):
        r = requests.post(f"{BASE}/support/ticket", headers=USER1,
                          json={"subject": "Order not delivered",
                                "message": "My order has not arrived yet"})
        assert r.status_code in [200, 201]
        data = r.json()
        ticket = data.get("ticket", data)
        assert ticket.get("status") == "OPEN", \
            f"BUG: New ticket should be OPEN, got {ticket.get('status')}"

    def test_create_ticket_short_subject(self):
        r = requests.post(f"{BASE}/support/ticket", headers=USER1,
                          json={"subject": "Hi", "message": "Help me"})
        assert r.status_code == 400

    def test_create_ticket_long_subject(self):
        r = requests.post(f"{BASE}/support/ticket", headers=USER1,
                          json={"subject": "x" * 101, "message": "Help"})
        assert r.status_code == 400

    def test_create_ticket_empty_message(self):
        r = requests.post(f"{BASE}/support/ticket", headers=USER1,
                          json={"subject": "Need help here", "message": ""})
        assert r.status_code == 400

    def test_create_ticket_long_message(self):
        r = requests.post(f"{BASE}/support/ticket", headers=USER1,
                          json={"subject": "Need help here", "message": "x" * 501})
        assert r.status_code == 400

    def test_get_tickets(self):
        r = requests.get(f"{BASE}/support/tickets", headers=USER1)
        assert r.status_code == 200

    def test_status_transition_open_to_in_progress(self):
        r = requests.post(f"{BASE}/support/ticket", headers=USER1,
                          json={"subject": "Transition test ticket",
                                "message": "Testing status flow"})
        data = r.json()
        ticket = data.get("ticket", data)
        tid = ticket.get("ticket_id")
        if tid:
            r2 = requests.put(f"{BASE}/support/tickets/{tid}", headers=USER1,
                              json={"status": "IN_PROGRESS"})
            assert r2.status_code == 200

    def test_status_transition_in_progress_to_closed(self):
        r = requests.post(f"{BASE}/support/ticket", headers=USER1,
                          json={"subject": "Closing test ticket",
                                "message": "Testing close flow"})
        data = r.json()
        ticket = data.get("ticket", data)
        tid = ticket.get("ticket_id")
        if tid:
            requests.put(f"{BASE}/support/tickets/{tid}", headers=USER1,
                         json={"status": "IN_PROGRESS"})
            r2 = requests.put(f"{BASE}/support/tickets/{tid}", headers=USER1,
                              json={"status": "CLOSED"})
            assert r2.status_code == 200

    def test_status_cannot_skip(self):
        """OPEN -> CLOSED should NOT be allowed."""
        r = requests.post(f"{BASE}/support/ticket", headers=USER1,
                          json={"subject": "Skip test ticket",
                                "message": "Testing invalid skip"})
        data = r.json()
        ticket = data.get("ticket", data)
        tid = ticket.get("ticket_id")
        if tid:
            r2 = requests.put(f"{BASE}/support/tickets/{tid}", headers=USER1,
                              json={"status": "CLOSED"})
            assert r2.status_code == 400, \
                f"BUG: OPEN->CLOSED should be rejected, got {r2.status_code}"

    def test_status_cannot_reopen(self):
        """CLOSED -> OPEN should NOT be allowed."""
        r = requests.post(f"{BASE}/support/ticket", headers=USER1,
                          json={"subject": "Reopen test ticket",
                                "message": "Testing reopen block"})
        data = r.json()
        ticket = data.get("ticket", data)
        tid = ticket.get("ticket_id")
        if tid:
            requests.put(f"{BASE}/support/tickets/{tid}", headers=USER1,
                         json={"status": "IN_PROGRESS"})
            requests.put(f"{BASE}/support/tickets/{tid}", headers=USER1,
                         json={"status": "CLOSED"})
            r2 = requests.put(f"{BASE}/support/tickets/{tid}", headers=USER1,
                              json={"status": "OPEN"})
            assert r2.status_code == 400, \
                f"BUG: CLOSED->OPEN should be rejected, got {r2.status_code}"

    def test_message_saved_exactly(self):
        """Full message must be saved exactly as written."""
        msg = "Hello! I need help with order #12345. My items were damaged."
        r = requests.post(f"{BASE}/support/ticket", headers=USER1,
                          json={"subject": "Damaged items complaint",
                                "message": msg})
        data = r.json()
        ticket = data.get("ticket", data)
        saved_msg = ticket.get("message", "")
        assert saved_msg == msg, \
            f"BUG: Message not saved exactly. Expected '{msg}', got '{saved_msg}'"
