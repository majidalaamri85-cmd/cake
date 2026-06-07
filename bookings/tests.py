from datetime import timedelta
from decimal import Decimal
from urllib.parse import parse_qs, urlparse

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .forms import BookingForm
from .models import Cake


@override_settings(STORAGES={
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
})
class HomeTests(TestCase):
    def test_cakes_are_ordered_by_number(self):
        Cake.objects.update(is_available=False)
        first_cake = Cake.objects.create(name='Z cake', flavor='vanilla')
        second_cake = Cake.objects.create(name='A cake', flavor='vanilla')

        response = self.client.get(reverse('home'))

        self.assertEqual(
            list(response.context['cakes'].values_list('id', flat=True)),
            [first_cake.id, second_cake.id],
        )

    def test_weight_choices_start_at_half_kilo_and_increase_by_half_kilo(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(
            [value for value, _label in response.context['weight_choices']],
            ['0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '4.5', '5', '5.5', '6'],
        )

    def test_first_cake_uses_special_starting_price(self):
        cake = Cake.objects.get(id=1)

        response = self.client.get(reverse('home'))

        self.assertContains(response, f'يبدأ من {cake.price_per_kg} ريال')

    def test_twelfth_cake_uses_special_starting_price(self):
        cake = Cake.objects.get(id=12)

        response = self.client.get(reverse('home'))

        self.assertContains(response, f'يبدأ من {cake.price_per_kg} ريال')

    def test_selected_cakes_use_five_nine_hundred_starting_price(self):
        response = self.client.get(reverse('home'))

        for cake_id in [5, 6, 8, 15, 17, 18, 19, 26, 27]:
            cake = Cake.objects.get(id=cake_id)
            self.assertEqual(cake.price_per_kg, Decimal('5.900'))
            self.assertContains(response, f'يبدأ من {cake.price_per_kg_display} ريال')

        spongebob_cake = Cake.objects.get(catalog_image='images/cakes/product-52.jpeg')
        self.assertEqual(spongebob_cake.price_per_kg, Decimal('5.900'))
        self.assertContains(response, f'يبدأ من {spongebob_cake.price_per_kg_display} ريال')

    def test_new_catalog_cakes_use_default_starting_price(self):
        response = self.client.get(reverse('home'))
        new_images = [f'images/cakes/product-{number}.jpeg' for number in range(46, 52)]

        cakes = Cake.objects.filter(catalog_image__in=new_images)

        self.assertEqual(cakes.count(), 6)
        for cake in cakes:
            self.assertEqual(cake.price_per_kg, Decimal('4.900'))
            self.assertContains(response, f'يبدأ من {cake.price_per_kg_display} ريال')


class BookingFormTests(TestCase):
    def setUp(self):
        self.cake = Cake.objects.create(name='Test cake', flavor='vanilla')
        self.data = {
            'cake': self.cake.id,
            'weight_kg': '2',
            'quantity': '1',
            'delivery_date': (timezone.localdate() + timedelta(days=1)).isoformat(),
            'delivery_time': '14:30',
            'delivery_address': 'Test address',
            'cake_message': 'Happy birthday',
            'special_requests': '',
        }

    def test_delivery_time_is_required(self):
        self.data['delivery_time'] = ''

        form = BookingForm(data=self.data)

        self.assertFalse(form.is_valid())
        self.assertIn('delivery_time', form.errors)

    def test_delivery_time_is_accepted(self):
        form = BookingForm(data=self.data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['delivery_time'].strftime('%H:%M'), '14:30')
        self.assertEqual(form.cleaned_data['cake_message'], 'Happy birthday')


class WhatsappOrderTests(TestCase):
    def setUp(self):
        self.cake = Cake.objects.create(name='Test cake', flavor='chocolate')

    def test_delivery_date_and_time_are_included_in_whatsapp_message(self):
        delivery_date = (timezone.localdate() + timedelta(days=1)).isoformat()

        response = self.client.get(reverse('whatsapp_order'), {
            'cake': self.cake.id,
            'weight_kg': '3',
            'delivery_date': delivery_date,
            'delivery_time': '16:45',
            'cake_message': 'كل عام وأنت بخير',
        })

        self.assertEqual(response.status_code, 302)
        whatsapp_url = urlparse(response.url)
        query = parse_qs(whatsapp_url.query)
        message = query['text'][0]
        self.assertEqual(whatsapp_url.netloc, 'api.whatsapp.com')
        self.assertEqual(query['phone'], ['96894032727'])
        self.assertIn(f'تاريخ التسليم: {delivery_date}', message)
        self.assertIn('وقت التسليم: 16:45', message)
        self.assertIn('الكتابة على الكعكة: كل عام وأنت بخير', message)

    def test_missing_delivery_date_redirects_to_home(self):
        response = self.client.get(reverse('whatsapp_order'), {
            'cake': self.cake.id,
            'weight_kg': '3',
            'delivery_time': '16:45',
        })

        self.assertRedirects(response, reverse('home'))

    def test_half_kilo_weight_is_included_in_whatsapp_message(self):
        response = self.client.get(reverse('whatsapp_order'), {
            'cake': self.cake.id,
            'weight_kg': '0.5',
            'delivery_date': (timezone.localdate() + timedelta(days=1)).isoformat(),
            'delivery_time': '16:45',
        })

        message = parse_qs(urlparse(response.url).query)['text'][0]
        self.assertIn('0.5', message)
        self.assertIn(str(Decimal('0.5') * self.cake.price_per_kg), message)

    def test_missing_delivery_time_redirects_to_home(self):
        response = self.client.get(reverse('whatsapp_order'), {
            'cake': self.cake.id,
            'weight_kg': '3',
            'delivery_date': (timezone.localdate() + timedelta(days=1)).isoformat(),
        })

        self.assertRedirects(response, reverse('home'))
