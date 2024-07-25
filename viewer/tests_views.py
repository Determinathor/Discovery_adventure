from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Profile, Product
from viewer.models import Category, Product, Profile
from django.core.paginator import Paginator


class ContactviewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')  # Zajistěte, aby URL jméno odpovídalo cestě k šabloně

        # Vytvoření testovacích kategorií
        self.category1 = Category.objects.create(name="Category 1")
        self.category2 = Category.objects.create(name="Category 2")

        # Vytvoření testovacího uživatele a profilu
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = Profile.objects.create(user=self.user, city="Brno")

    def test_view_with_logged_in_user(self):
        # Přihlášení uživatele
        self.client.login(username='testuser', password='12345')

        # Získání odpovědi
        response = self.client.get(self.url)

        # Ověření status kódu odpovědi
        self.assertEqual(response.status_code, 200)

        # Ověření, že všechny kategorie jsou v kontextu
        categories = response.context['categories']
        self.assertIn(self.category1, categories)
        self.assertIn(self.category2, categories)

        # Ověření, že aktuální šablona je správně nastavena
        self.assertEqual(response.context['current_template'], "kONTAKT")

        # Ověření, že město uživatele je správně vráceno
        self.assertEqual(response.context['user_city'], "Brno")

    def test_view_with_anonymous_user(self):
        # Získání odpovědi jako anonymní uživatel
        response = self.client.get(self.url)

        # Ověření status kódu odpovědi
        self.assertEqual(response.status_code, 200)

        # Ověření, že všechny kategorie jsou v kontextu
        categories = response.context['categories']
        self.assertIn(self.category1, categories)
        self.assertIn(self.category2, categories)

        # Ověření, že aktuální šablona je správně nastavena
        self.assertEqual(response.context['current_template'], "kONTAKT")

        # Ověření, že město uživatele je nastaveno na 'Praha'
        self.assertEqual(response.context['user_city'], "Praha")


class CategoryListViewTest(TestCase):

    def setUp(self):
        """Příprava prostředí pro testování seznamu kategorií"""
        self.client = Client()  # Inicializace testovacího klienta
        self.user = User.objects.create_user(username='testuser', password='password')  # Vytvoření testovacího uživatele
        self.profile = Profile.objects.create(user=self.user, city='Brno')  # Vytvoření profilu pro uživatele
        self.category1 = Category.objects.create(name='Category 1')  # Vytvoření testovací kategorie
        self.category2 = Category.objects.create(name='Category 2')  # Vytvoření další testovací kategorie
        self.product1 = Product.objects.create(title='Product 1')  # Vytvoření testovacího produktu
        self.product2 = Product.objects.create(title='Product 2')  # Vytvoření dalšího testovacího produktu
        self.product1.categories.add(self.category1)  # Přiřazení produktu do kategorie
        self.product2.categories.add(self.category2)  # Přiřazení dalšího produktu do jiné kategorie

    def test_view_with_logged_in_user(self):
        """Testování seznamu kategorií s přihlášeným uživatelem"""
        self.client.login(username='testuser', password='password')  # Přihlášení testovacího uživatele
        response = self.client.get(reverse('home'))  # Získání odpovědi ze seznamu kategorií
        self.assertEqual(response.status_code, 200)  # Ověření, že odpověď má status kód 200 (OK)
        self.assertTemplateUsed(response, 'home.html')  # Ověření, že je použita správná šablona
        self.assertIn('categories', response.context)  # Ověření, že kontext obsahuje kategorie
        self.assertEqual(len(response.context['categories']), 2)  # Ověření počtu kategorií
        self.assertEqual(response.context['categories'][0].product_count, 1)  # Ověření počtu produktů v první kategorii
        self.assertEqual(response.context['categories'][1].product_count, 1)  # Ověření počtu produktů v druhé kategorii
        self.assertEqual(response.context['current_template'], "Kategorie")  # Ověření aktuální šablony
        self.assertEqual(response.context['user_city'], 'Brno')  # Ověření města uživatele

    def test_view_with_anonymous_user(self):
        """Testování seznamu kategorií s anonymním uživatelem"""
        response = self.client.get(reverse('home'))  # Získání odpovědi ze seznamu kategorií jako anonymní uživatel
        self.assertEqual(response.status_code, 200)  # Ověření, že odpověď má status kód 200 (OK)
        self.assertTemplateUsed(response, 'home.html')  # Ověření, že je použita správná šablona
        self.assertIn('categories', response.context)  # Ověření, že kontext obsahuje kategorie
        self.assertEqual(len(response.context['categories']), 2)  # Ověření počtu kategorií
        self.assertEqual(response.context['categories'][0].product_count, 1)  # Ověření počtu produktů v první kategorii
        self.assertEqual(response.context['categories'][1].product_count, 1)  # Ověření počtu produktů v druhé kategorii
        self.assertEqual(response.context['current_template'], "Kategorie")  # Ověření aktuální šablony
        self.assertEqual(response.context['user_city'], 'Praha')  # Ověření města pro anonymního uživatele


class CategoryTemplateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.profile = Profile.objects.create(user=self.user, city='Brno')
        self.category1 = Category.objects.create(name='Category 1')
        self.category2 = Category.objects.create(name='Category 2')

        # Vytvoření produktů
        for i in range(1, 20):
            product = Product.objects.create(
                title=f'Product {i}',
                description=f'Description {i}',
                price=i * 10,
                stock=i
            )
            if i % 2 == 0:
                product.categories.add(self.category1)
            else:
                product.categories.add(self.category2)

        # Vyberte jednu kategorii pro testy
        self.url = reverse('category', args=[self.category1.pk])

    def test_view_with_logged_in_user(self):
        # Přihlášení uživatele
        self.client.login(username='testuser', password='password')

        # Získání odpovědi
        response = self.client.get(self.url)

        # Ověření status kódu odpovědi
        self.assertEqual(response.status_code, 200)

        # Ověření, že správné produkty jsou vráceny
        products = response.context['products']
        self.assertTrue(all(product in products for product in Product.objects.filter(categories=self.category1)))
        self.assertFalse(any(product in products for product in Product.objects.filter(categories=self.category2)))

        # Ověření paginace
        self.assertEqual(len(response.context['page_obj']), 9)  # Očekáváme 9 produktů na první stránce
        self.assertEqual(response.context['page_obj'].number, 1)  # Očekáváme, že jsme na první stránce

    def test_pagination(self):
        # Testování stránkování
        self.client.login(username='testuser', password='password')

        # Paginace test
        response = self.client.get(self.url + '?page=2')

        # Ověření, že stránkování funguje
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].number, 2)
        self.assertEqual(len(response.context['page_obj']), 1)  # Na druhé stránce by měl být pouze jeden produkt

    def test_view_with_anonymous_user(self):
        # Získání odpovědi jako anonymní uživatel
        response = self.client.get(self.url)

        # Ověření status kódu odpovědi
        self.assertEqual(response.status_code, 200)

        # Ověření, že správné produkty jsou vráceny
        products = response.context['products']
        self.assertTrue(all(product in products for product in Product.objects.filter(categories=self.category1)))
        self.assertFalse(any(product in products for product in Product.objects.filter(categories=self.category2)))

        # Ověření, že město uživatele je nastaveno na 'Praha'
        self.assertEqual(response.context['user_city'], 'Praha')