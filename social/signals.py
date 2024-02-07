from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from .models import Post
from django.core.mail import send_mail


@receiver(m2m_changed, sender=Post.likes.through)
def user_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()


@receiver(post_delete, sender=Post)
def user_post_delete(sender, instance, **kwargs):
    author = instance.author
    subject = "delete post"
    message = f"your below post has been deleted:\n{instance.description}"
    send_mail(subject, message, 'socialwebproject2024@gmail.com', [author.email], fail_silently=False)