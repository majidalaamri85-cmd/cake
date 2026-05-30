# Cake Booking

تطبيق Django لحجز الكيك مع تسجيل المستخدمين، اختيار المنتج، إنشاء الحجز، ومحاكاة الدفع.

## التشغيل المحلي

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py runserver
```

افتح المتصفح على:

```text
http://127.0.0.1:8000/
```

## الإعدادات

اضبط القيم التالية في ملف `.env` أو كمتغيرات بيئة:

```text
DJANGO_SECRET_KEY=change-this-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

## ملاحظات GitHub

- ملف قاعدة البيانات `db.sqlite3` مستبعد من Git.
- مجلد `media/` مستبعد لأنه مخصص للملفات المرفوعة محليًا.
- ملفات التشغيل والسجلات وملفات `__pycache__` مستبعدة من Git.

## النشر على Render

المشروع يحتوي على ملف `render.yaml` لتجهيز Web Service وقاعدة PostgreSQL تلقائيًا.

1. افتح Render واختر New Blueprint.
2. اربط مستودع GitHub الخاص بالمشروع.
3. اختر ملف `render.yaml` واتبع خطوات الإنشاء.

Render سيستخدم:

```text
Build Command: bash build.sh
Start Command: python -m gunicorn cake_booking.wsgi:application --bind 0.0.0.0:$PORT
```

ملاحظات مهمة:

- `DJANGO_DEBUG=False` مفعلة في Render.
- `SECRET_KEY` يتم توليده تلقائيًا من Render.
- `DATABASE_URL` مربوط بقاعدة PostgreSQL من Render.
- خطة Render المجانية لا تحفظ الملفات المرفوعة في `media/` بعد إعادة التشغيل أو إعادة النشر.
