# myproject/urls.py

from django.contrib import admin
from django.urls import path, include

# --- تأكد من وجود هذين السطرين ---
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')), # أو أي مسار تستخدمه
]

# --- تأكد من وجود هذا الجزء في نهاية الملف ---
# هذا الجزء يسمح بعرض الصور المرفوعة أثناء مرحلة التطوير
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)