import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

def send_email_to_all_users(post):
    subject = f"New Post Published: {post.title}"
    message = f"A New Post Has Been Published: {post.title}\n Please Check It Out This"
    from_email = settings.DEFAULT_FROM_EMAIL 

    recipient_list = list(User.objects.values_list("email",flat=True).exclude(email=""))

    if recipient_list:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

@receiver(post_save, sender=Post)
def notify_users_on_new_post(sender,instance,created,**kwargs):
    if created:
        threading.Thread(target=send_email_to_all_users, args=(instance,)).start()
