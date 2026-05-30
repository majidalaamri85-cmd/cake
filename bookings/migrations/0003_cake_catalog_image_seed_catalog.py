from django.db import migrations, models


CATALOG = [
    ('كيكة أسد للأطفال', 'vanilla', 'كيكة مرحة بطابع الأسد والنجوم لحفلات الأطفال.', 'product-17.jpeg'),
    ('كيكة أطفال مميزة', 'chocolate', 'تصميم مناسب لحفلات الأطفال ويمكن تخصيص الاسم.', 'product-11.jpeg'),
    ('كيكة احتفال فاخرة', 'chocolate', 'طبقات طازجة وتزيين مرتب لتقديم جميل في المناسبات.', 'product-04.jpeg'),
    ('كيكة باترول', 'vanilla', 'تصميم أطفال مميز بألوان جميلة ولمسة احتفالية.', 'product-03.jpeg'),
    ('كيكة بيت الطفلة', 'strawberry', 'تصميم طفولي لطيف مع شخصية وديكور نخيل وفراشات.', 'product-23.jpeg'),
    ('كيكة تخرج', 'vanilla', 'كيكة تخرج بتفاصيل قبعة وشهادة وتزيين فاخر.', 'product-24.jpeg'),
    ('كيكة تراميسو', 'chocolate', 'حلى تراميسو بطبقات كريمية ونكهة قهوة وشوكولاتة.', 'product-29.jpeg'),
    ('كيكة تمور بالكراميل', 'caramel', 'كيكة تمر غنية مغطاة بصوص الكراميل.', 'product-28.jpeg'),
    ('كيكة جابي للأطفال', 'strawberry', 'كيكة أطفال ملونة بشخصيات كرتونية وتفاصيل وردية.', 'product-31.jpeg'),
    ('كيكة حروف بارزة', 'vanilla', 'كيكة بيضاء بتفاصيل بسيطة واسم بارز حسب الطلب.', 'product-22.jpeg'),
    ('كيكة حليب بالفواكه', 'strawberry', 'كيكة حليب خفيفة مزينة بالفراولة والتوت.', 'product-30.jpeg'),
    ('كيكة حول حول أوتين', 'vanilla', 'تصميم احتفالي عربي مع ورود حمراء وتفاصيل تراثية.', 'product-36.jpeg'),
    ('كيكة دكتورز داي', 'caramel', 'كيكة مناسبة للاحتفاء بالأطباء والمناسبات المهنية.', 'product-18.jpeg'),
    ('كيكة رمضان بالتمر', 'caramel', 'كيكة رمضان بتفاصيل هلال وتمر ولمسة عربية.', 'product-34.jpeg'),
    ('كيكة زهور راقية', 'vanilla', 'كيكة كريمية مزينة بزهور ناعمة لمظهر رقيق وفاخر.', 'product-21.jpeg'),
    ('كيكة سيارات زرقاء', 'vanilla', 'كيكة أطفال زرقاء مزينة بالنجوم والسيارات والسحب.', 'product-25.jpeg'),
    ('كيكة سيارات ورسومات', 'vanilla', 'كيكة بيضاء برسومات سيارات وغيوم وشمس للأطفال.', 'product-35.jpeg'),
    ('كيكة شموع كلاسيكية', 'vanilla', 'تصميم أنيق ومناسب لأعياد الميلاد والمناسبات الخاصة.', 'product-01.jpeg'),
    ('كيكة شوكولاتة', 'chocolate', 'كعكة غنية بطعم الشوكولاتة وتزيين شهي.', 'product-07.jpeg'),
    ('كيكة عائلية', 'caramel', 'كيكة مناسبة للتجمعات العائلية بطابع دافئ.', 'product-12.jpeg'),
    ('كيكة عسكرية', 'chocolate', 'كيكة بتصميم عسكري وتفاصيل مخصصة لمحبي الثيمات الخاصة.', 'product-37.jpeg'),
    ('كيكة عيد مبارك', 'vanilla', 'كيكة بيضاء بتزيين كريمي وعبارة عيد مبارك.', 'product-33.jpeg'),
    ('كيكة عيد ميلاد', 'vanilla', 'كيكة احتفال كلاسيكية يمكن تخصيصها حسب المناسبة.', 'product-15.jpeg'),
    ('كيكة عيد ميلاد قلوب', 'vanilla', 'تصميم أبيض ناعم مع قلوب حمراء وكتابة مخصصة للمناسبات.', 'product-16.jpeg'),
    ('كيكة فانيليا', 'vanilla', 'كعكة فانيليا طازجة بطابع كلاسيكي ناعم.', 'product-08.jpeg'),
    ('كيكة فراولة', 'strawberry', 'نكهة فراولة خفيفة وتزيين جذاب للمناسبات.', 'product-09.jpeg'),
    ('كيكة فيونكات كلاسيكية', 'vanilla', 'تصميم أبيض أنيق مع فيونكات سوداء ولمسة فاخرة.', 'product-20.jpeg'),
    ('كيكة قوس ألوان', 'vanilla', 'كيكة باستيل مبهجة بألوان ناعمة مناسبة للاحتفالات.', 'product-32.jpeg'),
    ('كيكة كراميل دائرية', 'caramel', 'كيكة كريمية بصوص الكراميل وتزيين مقرمش شهي.', 'product-27.jpeg'),
    ('كيكة معدات صفراء', 'caramel', 'تصميم معدات بناء باللون الأصفر مناسب لحفلات الأولاد.', 'product-26.jpeg'),
    ('كيكة مكعبات الحليب', 'strawberry', 'قطع ميلك كيك كريمية مزينة بالفراولة والتوت.', 'product-19.jpeg'),
    ('كيكة مناسبات خاصة', 'caramel', 'اختيار مناسب للهدايا والطلبات المخصصة.', 'product-06.jpeg'),
    ('كيكة ميلك فردية', 'strawberry', 'قطعة ميلك كيك فردية كريمية مزينة بالفراولة والتوت.', 'product-38.jpeg'),
    ('كيكة ميلك كيك صينية', 'strawberry', 'صينية ميلك كيك مقطعة ومزينة بالفراولة والتوت.', 'product-39.jpeg'),
    ('كيكة ورد ناعمة', 'vanilla', 'مظهر هادئ وراقي لمحبي التفاصيل البسيطة.', 'product-05.jpeg'),
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
    Cake.objects.filter(catalog_image__startswith='images/cakes/').update(catalog_image='')


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_alter_payment_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='cake',
            name='catalog_image',
            field=models.CharField(blank=True, editable=False, max_length=255),
        ),
        migrations.RunPython(seed_catalog, clear_catalog_images),
    ]
