from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

@receiver(post_save, sender=Post)
def send_new_post_email(sender, instance, created, **kwargs):
    if created:
        subject = f"پست جدید: {instance.title}"
        message = f"{instance.title}\n\n{instance.text[:200]}...\n\nبرای مطالعه کامل به لینک زیر بروید:\nhttp://localhost:8000/posts/{instance.slug}/"
        from_email = 'noreply@yourdomain.com'

        users = User.objects.filter(is_active=True, email__isnull=False).exclude(email='')  # یوزرهای فعال با ایمیل
        recipient_list = [user.email for user in users]

        if recipient_list:
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
