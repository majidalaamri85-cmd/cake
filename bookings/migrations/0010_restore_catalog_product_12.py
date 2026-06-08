from django.db import migrations


CATALOG_IMAGE = 'images/cakes/product-17.jpeg'


def restore_product(apps, schema_editor):
    Cake = apps.get_model('bookings', 'Cake')
    Cake.objects.filter(catalog_image=CATALOG_IMAGE).update(is_available=True)


def hide_product(apps, schema_editor):
    Cake = apps.get_model('bookings', 'Cake')
    Cake.objects.filter(catalog_image=CATALOG_IMAGE).update(is_available=False)


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0009_hide_catalog_product_7'),
    ]

    operations = [
        migrations.RunPython(restore_product, hide_product),
    ]
