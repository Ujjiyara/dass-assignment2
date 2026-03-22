"""
Additional Black Box API Tests for QuickCart
Focusing on newly discovered Bugs 16, 17, 18, and 19
"""
import pytest
import requests

BASE = "http://localhost:8080/api/v1"
ROLL = "2024115005"
USER1 = {"X-Roll-Number": ROLL, "X-User-ID": "1"}
USER6 = {"X-Roll-Number": ROLL, "X-User-ID": "6"} # Zero orders

def test_bug16_review_without_purchase():
    # User 6 has no orders
    r = requests.post(f"{BASE}/products/1/reviews", headers=USER6,
                      json={"rating": 5, "comment": "Fake review"})
    assert r.status_code != 200, "BUG 16: Allowed review without purchase"

def test_bug17_coupon_persistence_below_min():
    # Clear cart
    requests.delete(f"{BASE}/cart/clear", headers=USER1)
    # Add item > 100 for WELCOME50
    requests.post(f"{BASE}/cart/add", headers=USER1, json={"product_id": 1, "quantity": 1})
    # Apply coupon
    requests.post(f"{BASE}/coupon/apply", headers=USER1, json={"coupon_code": "WELCOME50"})
    # Remove item
    requests.post(f"{BASE}/cart/remove", headers=USER1, json={"product_id": 1})
    # Add cheaper item < 100
    requests.post(f"{BASE}/cart/add", headers=USER1, json={"product_id": 9, "quantity": 1}) # $30
    
    r = requests.get(f"{BASE}/cart", headers=USER1)
    cart = r.json()
    # Total should be 30, but if coupon stays it's 0 or -20
    assert cart["total"] == 30, f"BUG 17: Coupon persisted below min threshold. Total: {cart['total']}"

def test_bug18_inactive_product_bypass():
    # Admin products to find inactive
    admin_prods = requests.get(f"{BASE}/admin/products", headers={"X-Roll-Number": ROLL}).json()
    inactive_id = next(p["product_id"] for p in admin_prods if not p["is_active"])
    
    r = requests.post(f"{BASE}/cart/add", headers=USER1,
                      json={"product_id": inactive_id, "quantity": 1})
    assert r.status_code != 200, "BUG 18: Allowed adding inactive product to cart"

def test_bug19_duplicate_reviews():
    # Submit first
    requests.post(f"{BASE}/products/2/reviews", headers=USER1,
                  json={"rating": 5, "comment": "First"})
    # Submit second
    r = requests.post(f"{BASE}/products/2/reviews", headers=USER1,
                      json={"rating": 1, "comment": "Second"})
    assert r.status_code != 200, "BUG 19: Allowed duplicate reviews per user"
