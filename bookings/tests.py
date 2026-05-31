from datetime import timedelta
from urllib.parse import parse_qs, urlparse

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import BookingForm
from .models import Cake


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
        self.assertEqual(query['phone'], ['96895066175'])
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

    def test_missing_delivery_time_redirects_to_home(self):
        response = self.client.get(reverse('whatsapp_order'), {
            'cake': self.cake.id,
            'weight_kg': '3',
            'delivery_date': (timezone.localdate() + timedelta(days=1)).isoformat(),
        })

        self.assertRedirects(response, reverse('home'))
