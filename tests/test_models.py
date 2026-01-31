import pytest
from your_module.models import User, Product, validate_data, process_data, Address, CustomModel, validate_custom_data

@pytest.mark.parametrize("name, age, expected", [
    ("Alice", 30, None),
    ("Bob", 15, ValueError),
    ("Charlie", "thirty", TypeError),
    ("David", -5, ValueError),
    ("Eve", 100, ValueError),
])
def test_user_validation(name, age, expected):
    if expected:
        with pytest.raises(expected):
            User(name=name, age=age)
    else:
        user = User(name=name, age=age)
        assert user.name == name
        assert user.age == age

@pytest.mark.parametrize("data, expected", [
    ({"name": "John", "age": 25}, {"name": "John", "age": 25}),
    ({"name": "", "age": 30}, ValueError),
    ({"age": "twenty-five"}, ValueError),
    ({"name": "Jane", "age": 30, "email": "jane@example.com"}, {"name": "Jane", "age": 30, "email": "jane@example.com"}),
])
def test_validate_data(data, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            validate_data(data)
    else:
        result = validate_data(data)
        assert result == expected

class TestUserModel:
    def test_valid_user_creation(self):
        user = User(name="Alice", age=30)
        assert user.name == "Alice"
        assert user.age == 30
        assert user.email == "alice@example.com"

    def test_invalid_user_missing_name(self):
        with pytest.raises(ValueError):
            User(age=30)

    def test_invalid_user_wrong_type_age(self):
        with pytest.raises(TypeError):
            User(name="Alice", age="thirty")

    def test_optional_fields_default_values(self):
        user = User(name="Bob")
        assert user.email == "bob@example.com"

    def test_nested_model_valid(self):
        address = Address(city="New York", zip_code="10001")
        user = User(name="Charlie", age=25, address=address)
        assert user.address.city == "New York"
        assert user.address.zip_code == "10001"

    def test_nested_model_invalid(self):
        with pytest.raises(ValueError):
            User(name="David", age=40, address={"city": "Los Angeles"})

class TestProductModel:
    def test_valid_product_creation(self):
        product = Product(name="Laptop", price=999.99, stock=100)
        assert product.name == "Laptop"
        assert product.price == 999.99
        assert product.stock == 100

    def test_invalid_product_negative_stock(self):
        with pytest.raises(ValueError):
            Product(name="Phone", price=599.99, stock=-10)

    def test_product_price_type_check(self):
        with pytest.raises(TypeError):
            Product(name="Monitor", price="nine hundred", stock=50)

    def test_product_required_fields(self):
        with pytest.raises(ValueError):
            Product(name="Tablet")

    def test_product_enum_validation(self):
        product = Product(name="Keyboard", category="Electronics")
        assert product.category == "Electronics"

        with pytest.raises(ValueError):
            Product(name="Mouse", category="InvalidCategory")

class TestErrorHandling:
    def test_invalid_data_raises_error(self):
        with pytest.raises(ValueError):
            User(name="Invalid", age=-5)

    def test_type_checking_failure(self):
        with pytest.raises(TypeError):
            User(name=123, age=30)

    def test_field_constraints_failure(self):
        with pytest.raises(ValueError):
            User(name="LongNameExceedingMaxLength", age=30)

    def test_custom_exception_raised(self):
        with pytest.raises(ValueError):
            CustomModel(value="invalid").validate()

    def test_invalid_enum_value(self):
        with pytest.raises(ValueError):
            CustomModel(status="pending", category="InvalidCategory")

    def test_custom_data_validation(self):
        with pytest.raises(ValueError):
            validate_custom_data({"value": "invalid", "status": "active"})

    def test_custom_data_success(self):
        result = validate_custom_data({"value": "valid", "status": "active"})
        assert result == {"value": "valid", "status": "active"}

    def test_custom_data_missing_required_field(self):
        with pytest.raises(ValueError):
            validate_custom_data({"status": "active"})

class TestValidationRules:
    def test_min_max_value_validation(self):
        user = User(name="Eve", age=20)
        assert user.age == 20

        with pytest.raises(ValueError):
            User(name="Frank", age=150)

    def test_enum_validation_correct(self):
        user = User(name="Grace", role="admin")
        assert user.role == "admin"

    def test_enum_validation_invalid(self):
        with pytest.raises(ValueError):
            User(name="Helen", role="manager")

    def test_custom_validation_rule(self):
        user = User(name="Ian", age=17)
        with pytest.raises(ValueError):
            user.validate()

    def test_field_length_constraints(self):
        with pytest.raises(ValueError):
            User(name="A" * 101, age=30)

    def test_field_format_validation(self):
        with pytest.raises(ValueError):
            User(name="InvalidEmail", email="invalid-email")

    def test_field_unique_constraint(self):
        user1 = User(name="John", email="john@example.com")
        user2 = User(name="Jane", email="john@example.com")
        with pytest.raises(ValueError):
            user2.validate()

    def test_field_default_values(self):
        user = User(name="Kevin")
        assert user.email == "kevin@example.com"