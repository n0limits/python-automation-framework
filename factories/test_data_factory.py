from faker import Faker
from typing import Dict, Any
import random

from utils.bvnk import api_client

fake = Faker()

class TestDataFactory:
    """
    Factory Pattern for generating realistic test data.

    Example:
        # Create test user
        admin = TestDataFactory.create_user("admin")
        response = api_client.post("/users", json=admin)

        # Create test product
        laptop = TestDataFactory.create_product("electronics")
        response = api_client.post("/products", json=laptop)
    """

    @staticmethod
    def create_user(user_type: str = "standard") -> Dict[str, Any]:
        """Create user test data based on type"""

        base_user = {
            "username": fake.user_name(),
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "phone": fake.phone_number(),
        }

        if user_type == "standard":
            base_user["password"] = "Test@1234"
            base_user["role"] = "user"

        elif user_type == "admin":
            base_user["password"] = "Admin@1234"
            base_user["role"] = "admin"
            base_user["permissions"] = ["read", "write", "delete"]

        elif user_type == "premium":
            base_user["password"] = "Premium@1234"
            base_user["role"] = "premium_user"
            base_user["subscription"] = {
                "plan": "premium",
                "valid_until": fake.future_date()
            }
        else:
            raise ValueError(f"Unknown user type: {user_type}")

        return base_user

    @staticmethod
    def create_product(category: str = "electronics") -> Dict[str, Any]:
        """Create product test data"""

        products_by_category = {
            "electronics": {
                "name": fake.word().capitalize() + " " + random.choice(["Phone", "Laptop", "Tablet"]),
                "price": round(random.uniform(299, 1999), 2),
                "category": "electronics",
                "stock": random.randint(0, 100)
            },
            "books": {
                "name": fake.catch_phrase(),
                "price": round(random.uniform(9.99, 49.99), 2),
                "category": "books",
                "author": fake.name(),
                "stock": random.randint(0, 50)
            },
            "clothing": {
                "name": random.choice(["T-Shirt", "Jeans", "Jacket"]),
                "price": round(random.uniform(19.99, 149.99), 2),
                "category": "clothing",
                "size": random.choice(["S", "M", "L", "XL"]),
                "stock": random.randint(0, 200)
            }
        }

        return products_by_category.get(category, products_by_category["electronics"])
