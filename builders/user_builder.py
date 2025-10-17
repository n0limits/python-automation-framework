from typing import Optional, List
from faker import Faker

fake = Faker()

class UserBuilder:
    """Builder for creating complex user objects"""

    def __init__(self):
        self._user = {
            "username": fake.user_name(),
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }

    def with_username(self, username: str):
        """Set username"""
        self._user["username"] = username
        return self

    def with_email(self, email: str):
        """Set email"""
        self._user["email"] = email
        return self

    def with_name(self, first_name: str, last_name: str):
        """Set full name"""
        self._user["first_name"] = first_name
        self._user["last_name"] = last_name
        return self

    def with_password(self, password: str):
        """Set password"""
        self._user["password"] = password
        return self

    def with_role(self, role: str):
        """Set role"""
        self._user["role"] = role
        return self

    def with_permissions(self, permissions: List[str]):
        """Set permissions"""
        self._user["permissions"] = permissions
        return self

    def with_address(self, street: str, city: str, country: str):
        """Set address"""
        self._user["address"] = {
            "street": street,
            "city": city,
            "country": country
        }
        return self

    def with_phone(self, phone: str):
        """Set phone"""
        self._user["phone"] = phone
        return self

    def as_admin(self):
        """Configure as admin user"""
        self._user["role"] = "admin"
        self._user["permissions"] = ["read", "write", "delete", "manage_users"]
        return self

    def as_premium(self):
        """Configure as premium user"""
        self._user["role"] = "premium"
        self._user["subscription"] = {
            "plan": "premium",
            "features": ["advanced_analytics", "priority_support", "api_access"]
        }
        return self

    def build(self) -> dict:
        """Build and return the user object"""
        return self._user

# Usage in tests
def test_create_admin_user():
    admin = (
        UserBuilder()
        .with_username("admin_user")
        .with_email("admin@company.com")
        .with_password("SecurePass123!")
        .as_admin()
        .with_phone("+1234567890")
        .build()
    )

    response = api_client.post("/users", json=admin)
    assert response.status_code == 201
    assert response.json()["role"] == "admin"

def test_create_premium_user():
    premium_user = (
        UserBuilder()
        .with_email("premium@example.com")
        .as_premium()
        .with_address("123 Main St", "New York", "USA")
        .build()
    )

    response = api_client.post("/users", json=premium_user)
    assert "subscription" in response.json()