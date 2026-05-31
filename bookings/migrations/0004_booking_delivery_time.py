from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_cake_catalog_image_seed_catalog'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='delivery_time',
            field=models.TimeField(null=True, verbose_name='وقت الاستلام أو التوصيل'),
        ),
    ]
