from django.test import TestCase

from viewer.models import Product, Category, Manufacturer


class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        manufacturer_1 = Manufacturer.objects.create(name="Manufacturer1")
        product = Product.objects.create(
            title="Testovaný produkt 1",
            product_type="TST",
            description="Toto je test popisu 1",
            #thumbnail="test.jpg",
            price=100,
            stock=15,
            manufacturer=manufacturer_1,

        )

        # manufacturer_1 = Manufacturer.objects.create(name="Manufacturer1")
        # product.manufacturer.add(manufacturer_1)

        category_1 = Category.objects.create(name="Category1", thumbnail="test1.jpg")
        product.categories.add(category_1)

        product.save()

    def setUp(self):
        print('--'*30)

    def test_product_title(self):
        product = Product.objects.get(id=1)
        print(f"test_product_title: '{product.title}'")
        self.assertEqual(product.title, "Testovaný produkt 1")

    def test_product_product_type(self):
        product = Product.objects.get(id=1)
        print(f"test_product_type: '{product.product_type}'")
        self.assertEqual(product.product_type, "TST")

    def test_product_manufacturer(self):
        product = Product.objects.get(id=1)
        print(f"test_product_manufacturer: '{product.manufacturer}'")
        self.assertEqual(product.manufacturer.name, "Manufacturer1")

    def test_product_category(self):
        product = Product.objects.get(id=1)
        categories = product.categories.all()
        category_names = [category.name for category in categories]
        print(f"test_category: {category_names}")
        self.assertIn("Category1", category_names)

    def test_product_description(self):
        product = Product.objects.get(id=1)
        print(f"test_product_description: '{product.description}'")
        self.assertEqual(product.description, "Toto je test popisu 1")

    def test_product_price(self):
        product = Product.objects.get(id=1)
        print(f"test_product_price: '{product.price}'")
        self.assertEqual(product.price, 100)

    def test_product_stock(self):
        product = Product.objects.get(id=1)
        print(f"test_product_stock: '{product.stock}'")
        self.assertEqual(product.stock, 15)

    def test_product_str(self):
        product = Product.objects.get(id=1)
        print(f"test_product_str: '{product}'")
        self.assertEqual(product.__str__(), "Testovaný produkt 1, in stock: 15, price: 100 EUR")

    def test_product_repr(self):
        product = Product.objects.get(id=1)
        print(f"test_product_repr: '{product.__repr__()}'")
        self.assertEqual(product.__repr__(), "<Product: Testovaný produkt 1, in stock: 15, price: 100 EUR>")
