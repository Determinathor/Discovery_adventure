from django.test import TestCase

from viewer.models import Category, Manufacturer
from viewer.views import ProductModelForm


class ProductFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(name="Kategorie1")
        cls.category2 = Category.objects.create(name="Kategorie2")
        cls.category3 = Category.objects.create(name="Kategorie3")
        cls.manufacturer = Manufacturer.objects.create(name="Výrobce1")

    def setUp(self):
        print("-"*60)

    def test_product_valid_form(self):
        form = ProductModelForm(
            data={
                'title': '  Produkt_test  ',
                'product_type': 'OT',
                'description': 'Nějaký popis',
                'thumbnail': 'odkaz_test.jpg',
                'price': 100,
                'stock': 10,
                'manufacturer': '1',
                'categories': ['1', '2'],
            }
        )
        print(f"test_product_valid_form: {form.data}")
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_product_invalid_form(self):
        form = ProductModelForm(
            data={
                'title': 'Produkt_test',
                'product_type': 'OT',
                'description': 'Nějaký popis',
                'thumbnail': 'odkaz_test.jpg',
                'price': 0,
                'stock': 10,
                'manufacturer': '1',
                'categories': ['1', '2'],
            }
        )
        print(f"test_product_valid_form: {form.data}")
        self.assertFalse(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_clean_title(self):
        form = ProductModelForm(
            data={
                'title': '  Produkt_test  ',
                'product_type': 'OT',
                'description': 'Nějaký popis',
                'thumbnail': 'odkaz_test.jpg',
                'price': 100,
                'stock': 10,
                'manufacturer': '1',
                'categories': ['1', '2'],
            }
        )
        form.is_valid()
        cleaned_data = form.cleaned_data
        print(f"test_clean_title: '{cleaned_data['title']}'")
        self.assertEqual(cleaned_data['title'], 'Produkt_test')

    def test_clean_price_zero_or_negative(self):
        form = ProductModelForm(
            data={
                'title': '  Produkt_test  ',
                'product_type': 'OT',
                'description': 'Nějaký popis',
                'thumbnail': 'odkaz_test.jpg',
                'price': -10,
                'stock': 10,
                'manufacturer': '1',
                'categories': ['1', '2'],
            }
        )

        print(f"test_clean_price_zero_or_negative: Price must be greater than 0.'")
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)
        self.assertEqual(form.errors['price'],['Ensure this value is greater than or equal to 1.']
        )
        # self.assertEqual(
        #     form.errors['price'],
        #     ['Price must be greater than 0.']
        # )

    def test_clean_stock_positive(self):
        form = ProductModelForm(
            data={
                'title': '  Produkt_test  ',
                'product_type': 'OT',
                'description': 'Nějaký popis',
                'thumbnail': 'odkaz_test.jpg',
                'price': 100,
                'stock': 10,
                'manufacturer': '1',
                'categories': ['1', '2'],
            }
        )
        form.is_valid()
        cleaned_data = form.cleaned_data
        print(f"test_clean_stock_positive: {cleaned_data['stock']}")
        self.assertEqual(cleaned_data['stock'], 10)

    def test_clean_stock_zero(self):
        form = ProductModelForm(
            data={
                'title': '  Produkt_test  ',
                'product_type': 'OT',
                'description': 'Nějaký popis',
                'thumbnail': 'odkaz_test.jpg',
                'price': 100,
                'stock': 0,
                'manufacturer': '1',
                'categories': ['1', '2'],
            }
        )
        form.is_valid()
        cleaned_data = form.cleaned_data
        print(f"test_clean_stock_zero: {cleaned_data['stock']}")
        self.assertEqual(cleaned_data['stock'], 0)

    def test_clean_stock_negative(self):
        form = ProductModelForm(
            data={
                'title': '  Produkt_test  ',
                'product_type': 'OT',
                'description': 'Nějaký popis',
                'thumbnail': 'odkaz_test.jpg',
                'price': 100,
                'stock': -10,
                'manufacturer': '1',
                'categories': ['1', '2'],
            }
        )
        print(f"test_clean_stock_negative: Stock cannot be negative.")
        self.assertFalse(form.is_valid())
        self.assertIn('stock', form.errors)
        self.assertEqual(
            form.errors['stock'],
            ['Stock cannot be negative.']
        )