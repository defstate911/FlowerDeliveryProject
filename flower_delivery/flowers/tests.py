from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
#from .models import Bouquet
from flowers.models import Bouquet

# Тесты для модели Bouquet
class BouquetModelTest(TestCase):
    def setUp(self):
        # Создаем тестовый файл для ImageField
        test_image = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg"
        )
        # Создаем тестовые данные
        self.bouquet = Bouquet.objects.create(
            name="Роза в облаке",
            description="Розы в белых облаках гипсофилы",
            price=1500.00,
            image=test_image  # Передаем файл
        )

    def test_bouquet_creation(self):
        """Проверяем, что букет корректно создаётся."""
        self.assertEqual(Bouquet.objects.count(), 1)
        self.assertEqual(self.bouquet.name, "Роза в облаке")
        self.assertEqual(self.bouquet.price, 1500.00)

    def test_bouquet_str_method(self):
        """Проверяем, что метод __str__ возвращает имя букета."""
        self.assertEqual(str(self.bouquet), "Роза в облаке")


# Тесты для представления home
class HomeViewTest(TestCase):
    def setUp(self):
        test_image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        Bouquet.objects.create(name="Роза", price=1200, image=test_image)
        Bouquet.objects.create(name="Тюльпан", price=800, image=test_image)

    def test_home_view_status_code(self):
        """Проверяем, что домашняя страница доступна."""
        response = self.client.get(reverse('flowers:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_context(self):
        """Проверяем, что в контексте домашней страницы передаются букеты."""
        response = self.client.get(reverse('flowers:home'))
        self.assertContains(response, "Роза")
        self.assertContains(response, "Тюльпан")


# Тесты для представления about
class AboutViewTest(TestCase):

    def test_about_view_status_code(self):
        """Проверяем, что страница 'О нас' доступна."""
        response = self.client.get(reverse('flowers:about'))
        self.assertEqual(response.status_code, 200)

    def test_about_view_template(self):
        """Проверяем, что используется правильный шаблон."""
        response = self.client.get(reverse('flowers:about'))
        self.assertTemplateUsed(response, 'flowers/about.html')


# Тесты для представления contacts
class ContactsViewTest(TestCase):

    def test_contacts_view_status_code(self):
        """Проверяем, что страница 'Контакты' доступна."""
        response = self.client.get(reverse('flowers:contacts'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_view_template(self):
        """Проверяем, что используется правильный шаблон."""
        response = self.client.get(reverse('flowers:contacts'))
        self.assertTemplateUsed(response, 'flowers/contacts.html')
