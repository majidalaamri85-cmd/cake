import uuid
from decimal import Decimal
from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_time

from .forms import WEIGHT_CHOICES, BookingForm, PaymentForm, RegisterForm
from .models import Booking, Cake, Payment


def home(request):
    cakes = Cake.objects.filter(is_available=True).order_by('id')
    return render(request, 'bookings/home.html', {
        'cakes': cakes,
        'weight_choices': WEIGHT_CHOICES,
        'price_per_kg': f'{settings.CAKE_PRICE_PER_KG:.3f}',
        'currency': settings.PAYMENT_CURRENCY,
        'today': timezone.localdate().isoformat(),
    })


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'تم إنشاء الحساب بنجاح. أهلاً بك!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def whatsapp_order(request):
    cake = get_object_or_404(Cake, id=request.GET.get('cake'), is_available=True)
    weight_kg = request.GET.get('weight_kg')
    valid_weights = {value for value, _label in WEIGHT_CHOICES}
    if weight_kg not in valid_weights:
        weight_kg = '0.5'
    delivery_date = parse_date(request.GET.get('delivery_date', ''))
    if not delivery_date or delivery_date < timezone.localdate():
        messages.error(request, 'اختر يوم تسليم صحيحاً قبل المتابعة إلى واتساب.')
        return redirect('home')
    delivery_time = parse_time(request.GET.get('delivery_time', ''))
    if not delivery_time:
        messages.error(request, 'اختر وقت التسليم قبل المتابعة إلى واتساب.')
        return redirect('home')
    delivery_time_display = delivery_time.strftime('%H:%M')
    cake_message = request.GET.get('cake_message', '').strip()[:100] or 'لا توجد كتابة'

    total_price = Decimal(weight_kg) * cake.price_per_kg
    if cake.catalog_image:
        product_url = request.build_absolute_uri(static(cake.catalog_image))
    elif cake.image:
        product_url = request.build_absolute_uri(cake.image.url)
    else:
        product_url = request.build_absolute_uri('/')
    message = (
        f'السلام عليكم، أريد طلب منتج من المخبز.\n'
        f'رقم الكعكة: {cake.id}\n'
        f'الوزن: {weight_kg} كجم\n'
        f'تاريخ التسليم: {delivery_date:%Y-%m-%d}\n'
        f'وقت التسليم: {delivery_time_display}\n'
        f'الكتابة على الكعكة: {cake_message}\n'
        f'السعر التقريبي: {total_price} {settings.PAYMENT_CURRENCY}\n'
        f'صورة الكعكة: {product_url}\n'
        'فضلاً أرسلوا لي تفاصيل التأكيد.'
    )
    phone = getattr(settings, 'BAKERY_WHATSAPP_PHONE', '').strip().replace('+', '')
    return redirect(f'https://api.whatsapp.com/send?phone={phone}&text={quote(message)}')


@login_required
def create_booking(request):
    initial = {}
    cake_id = request.GET.get('cake')
    weight_kg = request.GET.get('weight_kg')
    if cake_id:
        initial['cake'] = cake_id
    if weight_kg in {value for value, _label in WEIGHT_CHOICES}:
        initial['weight_kg'] = weight_kg

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            send_booking_email(booking)
            messages.success(request, 'تم إنشاء الحجز. أكمل الدفع لتأكيد الطلب.')
            return redirect('payment', booking_id=booking.id)
    else:
        form = BookingForm(initial=initial)

    return render(request, 'bookings/create_booking.html', {
        'form': form,
        'price_per_kg': f'{settings.CAKE_PRICE_PER_KG:.3f}',
        'cake_prices': {
            str(cake.id): str(cake.price_per_kg)
            for cake in Cake.objects.filter(is_available=True)
        },
        'currency': settings.PAYMENT_CURRENCY,
    })


@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.payment_status == 'paid':
        messages.info(request, 'هذا الحجز مدفوع مسبقاً.')
        return redirect('booking_detail', booking_id=booking.id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            transaction_prefix = {
                'thawani_omannet': 'THW',
                'bank_muscat_gateway': 'BM',
                'oman_bank_transfer': 'OM-BANK',
            }.get(form.cleaned_data['payment_method'], 'PAY')
            Payment.objects.create(
                booking=booking,
                amount=booking.total_price,
                payment_method=form.cleaned_data['payment_method'],
                transaction_id=f'{transaction_prefix}-{uuid.uuid4()}',
                paid_at=timezone.now(),
            )
            booking.payment_status = 'paid'
            booking.status = 'confirmed'
            booking.save(update_fields=['payment_status', 'status', 'total_price', 'updated_at'])
            send_payment_email(booking)
            messages.success(request, 'تم الدفع بنجاح وتم تأكيد الحجز.')
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = PaymentForm()

    return render(request, 'bookings/payment.html', {
        'booking': booking,
        'form': form,
        'currency': settings.PAYMENT_CURRENCY,
        'bank_transfer_details': settings.OMAN_BANK_TRANSFER_DETAILS,
    })


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_detail.html', {
        'booking': booking,
        'currency': settings.PAYMENT_CURRENCY,
    })


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('cake')
    return render(request, 'bookings/my_bookings.html', {
        'bookings': bookings,
        'currency': settings.PAYMENT_CURRENCY,
    })


def send_booking_email(booking):
    if not booking.user.email:
        return
    send_mail(
        f'تم استلام حجز الكعكة رقم {booking.id}',
        (
            f'مرحباً {booking.user.username}\n\n'
            f'تم استلام طلب {booking.cake.name} بوزن {booking.weight_kg} كجم.\n'
            f'موعد التسليم: {booking.delivery_date} - {format_delivery_time(booking)}.\n'
            f'الكتابة على الكعكة: {booking.cake_message or "لا توجد كتابة"}.\n'
            f'المبلغ الإجمالي: {booking.total_price} {settings.PAYMENT_CURRENCY}.\n'
            'يرجى إكمال الدفع لتأكيد الحجز.'
        ),
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        fail_silently=True,
    )


def send_payment_email(booking):
    if not booking.user.email:
        return
    send_mail(
        f'تم تأكيد دفع الحجز رقم {booking.id}',
        (
            f'مرحباً {booking.user.username}\n\n'
            f'تم تأكيد حجز {booking.cake.name} للتاريخ {booking.delivery_date} في الساعة {format_delivery_time(booking)}.\n'
            f'الكتابة على الكعكة: {booking.cake_message or "لا توجد كتابة"}.\n'
            f'المبلغ المدفوع: {booking.total_price} {settings.PAYMENT_CURRENCY}.'
        ),
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        fail_silently=True,
    )


def format_delivery_time(booking):
    return booking.delivery_time.strftime('%H:%M') if booking.delivery_time else 'غير محدد'
