from django.db import migrations


def hide_product(apps, schema_editor):
    Cake = apps.get_model('bookings', 'Cake')
    Cake.objects.filter(id=7).update(is_available=False)


def show_product(apps, schema_editor):
    Cake = apps.get_model('bookings', 'Cake')
    Cake.objects.filter(id=7).update(is_available=True)


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0008_seed_spongebob_catalog_product'),
    ]

    operations = [
        migrations.RunPython(hide_product, show_product),
    ]
