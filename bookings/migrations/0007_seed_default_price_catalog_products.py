from django.db import migrations


CATALOG = [
    (
        'كيكة شوكولاتة بالفواكه',
        'chocolate',
        'كيكة كريمية بصوص الشوكولاتة وتزيين فراولة وتوت وكريمة بيضاء لمظهر أنيق ومناسب للمناسبات.',
        'product-46.jpeg',
    ),
    (
        'كيكة شوكولاتة بزهور بيضاء',
        'chocolate',
        'كيكة شوكولاتة ناعمة مزينة بزهور كريمة بيضاء وحبات حمراء بسيطة لتصميم راق وهادئ.',
        'product-47.jpeg',
    ),
    (
        'كيكة عيد بالزهور الوردية',
        'chocolate',
        'كيكة عيد مبارك بصوص الشوكولاتة وزهور وردية مع كتابة مخصصة حسب المناسبة.',
        'product-48.jpeg',
    ),
    (
        'كيكة كلاسيكية بشرائط سوداء',
        'vanilla',
        'كيكة بيضاء كلاسيكية مزينة بشرائط سوداء وتفاصيل كريمة ناعمة لمناسبة أنيقة.',
        'product-49.jpeg',
    ),
    (
        'كيكة القلوب الوردية',
        'vanilla',
        'كيكة بيضاء مزينة بشرائط وردية وقلوب صغيرة مع إمكانية كتابة الاسم حسب الطلب.',
        'product-50.jpeg',
    ),
    (
        'كيكة الفراولة بصوص الشوكولاتة',
        'chocolate',
        'كيكة بصوص الشوكولاتة والفراولة والتوت بتصميم بسيط وطازج للمناسبات اليومية والخاصة.',
        'product-51.jpeg',
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
        ('bookings', '0006_seed_additional_catalog_products'),
    ]

    operations = [
        migrations.RunPython(seed_catalog, clear_catalog_images),
    ]
