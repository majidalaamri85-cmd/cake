from django.db import migrations


CATALOG = [
    (
        'كيكة شخصيات أطفال',
        'vanilla',
        'كيكة أطفال ملونة مزينة بشخصيات كرتونية لطيفة وتفاصيل وردية وبنفسجية.',
        'product-40.jpeg',
    ),
    (
        'كيكة زهور رقيقة',
        'lemon',
        'كيكة كريمية ناعمة مزينة بزهور صغيرة بيضاء ووردية لمظهر أنيق وهادئ.',
        'product-41.jpeg',
    ),
    (
        'كيكة الكرز',
        'vanilla',
        'كيكة بيضاء بتزيين كرز بسيط ومرح، مناسبة لأعياد الميلاد والمناسبات الخاصة.',
        'product-42.jpeg',
    ),
    (
        'كيكة رسم طريف',
        'vanilla',
        'كيكة مخصصة برسمة مرحة وكتابة حسب الطلب لإضافة لمسة شخصية للمناسبة.',
        'product-43.jpeg',
    ),
    (
        'كيكة شوكولاتة بالقهوة',
        'chocolate',
        'كيكة كريمية بنكهة القهوة مع صوص الشوكولاتة وتزيين أنيق لأعياد الميلاد.',
        'product-44.jpeg',
    ),
    (
        'كيكة الفراشات الوردية',
        'strawberry',
        'كيكة وردية وزرقاء مزينة بفراشات رقيقة وحبات فضية لمناسبة مبهجة.',
        'product-45.jpeg',
    ),
]


def seed_catalog(apps, schema_editor):
    Cake = apps.get_model('bookings', 'Cake')
    for name, flavor, description, filename in CATALOG:
        cake, _ = Cake.objects.get_or_create(
            name=name,
            defaults={
                'flavor': flavor,
                'description': description,
                'is_available': True,
            },
        )
        cake.catalog_image = f'images/cakes/{filename}'
        cake.save(update_fields=['catalog_image'])


def clear_catalog_images(apps, schema_editor):
    Cake = apps.get_model('bookings', 'Cake')
    Cake.objects.filter(
        name__in=[name for name, _, _, _ in CATALOG],
        catalog_image__in=[f'images/cakes/{filename}' for _, _, _, filename in CATALOG],
    ).update(catalog_image='')


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_booking_cake_message'),
    ]

    operations = [
        migrations.RunPython(seed_catalog, clear_catalog_images),
    ]
