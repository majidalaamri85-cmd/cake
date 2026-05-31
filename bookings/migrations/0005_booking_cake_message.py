from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_booking_delivery_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='cake_message',
            field=models.CharField(blank=True, max_length=100, verbose_name='الكتابة على الكعكة'),
        ),
    ]
