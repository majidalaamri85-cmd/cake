from django.db import migrations


def hide_product(apps, schema_editor):
    Cake = apps.get_model('bookings', 'Cake')
    catalog_product = Cake.objects.filter(is_available=True).order_by('id')[11:12].first()
    if catalog_product:
        catalog_product.is_available = False
        catalog_product.save(update_fields=['is_available'])


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0009_hide_catalog_product_7'),
    ]

    operations = [
        migrations.RunPython(hide_product, migrations.RunPython.noop),
    ]
