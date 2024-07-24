# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth.models import User, Permission
# from viewer.models import Product, Category, Manufacturer
# from django.utils import timezone
#
#
# class ShopViewTests(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Inicializace testovacího klienta
#         cls.client = Client()
#         # Vytvoření běžného uživatele
#         cls.user = User.objects.create_user(username='testuser', password='password')
#         # Vytvoření uživatele s právy administrátora (staff)
#         cls.staff_user = User.objects.create_user(username='staffuser', password='password', is_staff=True)
#
#         # Vytvoření testovací kategorie
#         cls.category = Category.objects.create(name='Test Category')
#         # Vytvoření testovacího výrobce
#         cls.manufacturer = Manufacturer.objects.create(name='Test Manufacturer')
#
#         # Vytvoření testovacích produktů
#         cls.product1 = Product.objects.create(
#             title='Test Product 1',
#             description='Description for product 1',
#             price=100,
#             stock=10,
#             manufacturer=cls.manufacturer
#         )
#         cls.product1.categories.add(cls.category)  # Přiřazení kategorie k produktu
#
#         cls.product2 = Product.objects.create(
#             title='Test Product 2',
#             description='Description for product 2',
#             price=200,
#             stock=5,
#             manufacturer=cls.manufacturer
#         )
#         cls.product2.categories.add(cls.category)  # Přiřazení kategorie k produktu
#
#         cls.product1.save()
#         cls.product2.save()
#
#     def setUp(self):
#         print("-"*60)
#
#     def test_product_list_view(self):
#         # Test zobrazení seznamu produktů
#         response = self.client.get(reverse('shop'))
#         self.assertEqual(response.status_code, 200)  # Očekáváme úspěšný HTTP status kód 200
#         self.assertContains(response, 'Test Product 1')  # Ověření, že stránka obsahuje 'Test Product 1'
#         self.assertContains(response, 'Test Product 2')  # Ověření, že stránka obsahuje 'Test Product 2'
#
#     def test_product_create_view_permission(self):
#         # Test oprávnění pro vytvoření produktu
#         self.client.login(username='testuser', password='password')
#         response = self.client.get(reverse('product_create'))
#         self.assertEqual(response.status_code, 403)  # Očekáváme zakázaný HTTP status kód 403 (bez oprávnění)
#
#         # Přiřazení oprávnění k uživateli pro přidání produktu
#         self.user.user_permissions.add(Permission.objects.get(codename='add_product'))
#         response = self.client.get(reverse('product_create'))
#         self.assertEqual(response.status_code, 200)  # Očekáváme úspěšný HTTP status kód 200 (s oprávněním)
#
#     def test_product_create_view(self):
#         # Test vytvoření nového produktu
#         self.client.login(username='staffuser', password='password')
#         response = self.client.post(reverse('product_create'), {
#             'title': 'New Product',
#             'description': 'New product description',
#             'price': 300,
#             'stock': 15,
#             'manufacturer': self.manufacturer.id,
#             'categories': [self.category.id]
#         })
#         self.assertEqual(response.status_code, 302)  # Očekáváme přesměrování (status kód 302)
#         self.assertTrue(Product.objects.filter(title='New Product').exists())  # Ověření, že nový produkt byl vytvořen
#
#     def test_product_update_view_permission(self):
#         # Test oprávnění pro úpravu produktu
#         self.client.login(username='testuser', password='password')
#         response = self.client.get(reverse('product_create', args=[self.product1.id]))
#         self.assertEqual(response.status_code, 403)  # Očekáváme zakázaný HTTP status kód 403 (bez oprávnění)
#
#         # Přiřazení oprávnění k uživateli pro úpravu produktu
#         self.user.user_permissions.add(Permission.objects.get(codename='change_product'))
#         response = self.client.get(reverse('product_create', args=[self.product1.id]))
#         self.assertEqual(response.status_code, 200)  # Očekáváme úspěšný HTTP status kód 200 (s oprávněním)
#
#     def test_product_update_view(self):
#         # Test úpravy produktu
#         self.client.login(username='staffuser', password='password')
#         response = self.client.post(reverse('product_create', args=[self.product1.id]), {
#             'title': 'Updated Product',
#             'description': 'Updated description',
#             'price': 150,
#             'stock': 20,
#             'manufacturer': self.manufacturer.id,
#             'categories': [self.category.id]
#         })
#         self.assertEqual(response.status_code, 302)  # Očekáváme přesměrování (status kód 302)
#         self.product1.refresh_from_db()  # Obnovení produktu z databáze
#         self.assertEqual(self.product1.title, 'Updated Product')  # Ověření, že titul produktu byl aktualizován
#
#     def test_product_delete_view_permission(self):
#         # Test oprávnění pro smazání produktu
#         self.client.login(username='testuser', password='password')
#         response = self.client.get(reverse('product_delete', args=[self.product1.id]))
#         self.assertEqual(response.status_code, 403)  # Očekáváme zakázaný HTTP status kód 403 (bez oprávnění)
#
#         # Přiřazení oprávnění k uživateli pro smazání produktu
#         self.user.user_permissions.add(Permission.objects.get(codename='delete_product'))
#         response = self.client.get(reverse('product_delete', args=[self.product1.id]))
#         self.assertEqual(response.status_code, 200)  # Očekáváme úspěšný HTTP status kód 200 (s oprávněním)
#
#     def test_product_delete_view(self):
#         # Test smazání produktu
#         self.client.login(username='staffuser', password='password')
#         response = self.client.post(reverse('product_delete', args=[self.product1.id]))
#         self.assertEqual(response.status_code, 302)  # Očekáváme přesměrování (status kód 302)
#         self.assertFalse(Product.objects.filter(id=self.product1.id).exists())  # Ověření, že produkt byl smazán
