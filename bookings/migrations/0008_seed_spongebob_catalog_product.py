from django.db import migrations


CATALOG = [
    (
        'كيكة سبونج بوب',
        'vanilla',
        'كيكة أطفال صفراء بتصميم سبونج بوب وشخصيات كرتونية مبهجة مع كتابة مخصصة حسب الطلب.',
        'product-52.jpeg',
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
        ('bookings', '0007_seed_default_price_catalog_products'),
    ]

    operations = [
        migrations.RunPython(seed_catalog, clear_catalog_images),
    ]
