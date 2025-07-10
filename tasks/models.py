# tasks/models.py
from django.db import models
from django.utils import timezone

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('H', 'عالية'),
        ('M', 'متوسطة'),
        ('L', 'منخفضة'),
    ]

    title = models.CharField(max_length=200, verbose_name="عنوان المهمة")
    description = models.TextField(null=True, blank=True, verbose_name="الوصف")
    
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default='M',
        verbose_name="الأولوية"
    )
    
    # --- التغييرات الجديدة هنا ---
    # 1. غيرنا `due_date` إلى `expiration_date` وغيرنا نوعه لدعم الوقت
    expiration_date = models.DateTimeField(
        default=timezone.now, 
        verbose_name="تاريخ/وقت الانتهاء"
    )
    
    completed = models.BooleanField(default=False, verbose_name="مكتملة")
    image = models.ImageField(upload_to='task_images/', null=True, blank=True, verbose_name="صورة المهمة")

    # 2. أعدنا تسمية `created_at` ليظهر كـ "تاريخ الإنشاء"
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    # 3. خاصية جديدة لمعرفة إذا كانت المهمة منتهية الصلاحية
    @property
    def is_expired(self):
        # المهمة منتهية إذا كان وقت الانتهاء في الماضي ولم تكن مكتملة
        return self.expiration_date < timezone.now() and not self.completed

    def __str__(self):
        return self.title

    class Meta:
        # الترتيب الافتراضي الآن حسب تاريخ الانتهاء
        ordering = ['completed', 'expiration_date']
        verbose_name = "مهمة"
        verbose_name_plural = "المهام"