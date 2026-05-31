from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Booking, Cake


WEIGHT_CHOICES = [(value, f'{value} كجم') for value in range(1, 7)]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label='البريد الإلكتروني')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'اسم المستخدم',
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('cake', 'weight_kg', 'quantity', 'delivery_date', 'delivery_time', 'delivery_address', 'special_requests')
        widgets = {
            'cake': forms.Select(attrs={'class': 'form-select'}),
            'weight_kg': forms.Select(choices=WEIGHT_CHOICES, attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'delivery_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'cake': 'نوع الكعكة',
            'weight_kg': 'الوزن بالكيلو',
            'quantity': 'الكمية',
            'delivery_date': 'تاريخ الاستلام أو التوصيل',
            'delivery_time': 'وقت الاستلام أو التوصيل',
            'delivery_address': 'العنوان',
            'special_requests': 'طلبات خاصة',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cake'].queryset = Cake.objects.filter(is_available=True)

    def clean_delivery_date(self):
        delivery_date = self.cleaned_data['delivery_date']
        if delivery_date < timezone.localdate():
            raise forms.ValidationError('اختر تاريخاً اليوم أو بعده.')
        return delivery_date


class PaymentForm(forms.Form):
    PAYMENT_METHODS = [
        ('thawani_omannet', 'ثواني - بطاقات عمان نت والبطاقات البنكية'),
        ('bank_muscat_gateway', 'بوابة بنك مسقط للدفع الإلكتروني'),
        ('oman_bank_transfer', 'تحويل بنكي داخل سلطنة عمان'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHODS,
        widget=forms.RadioSelect(attrs={'class': 'payment-options'}),
        label='طريقة الدفع',
    )
