# # news/signals.py

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import News

# @receiver(post_save, sender=News)
# def send_news_to_telegram(sender, instance, created, **kwargs):
#     if created:
#         instance.notify_telegram()  # Yangilik qo'shilganda Telegramga xabar yuborish
