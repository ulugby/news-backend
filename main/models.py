from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

# from aiogram import Bot
# from aiogram.enums.parse_mode import ParseMode

from django.utils.html import strip_tags
import requests,json, html, re
from django.urls import reverse
from bs4 import BeautifulSoup


# Create your models here.


class Config(models.Model):
    telegram_bot_token = models.CharField(max_length=255, help_text="Telegram bot uchun token")
    telegram_channel_id = models.CharField(max_length=255, help_text="Telegram kanalining ID yoki username")
    telegram_channel_name = models.CharField(max_length=255, help_text="Telegram kanal nomi majburiy emas", null=True, blank=True)

    class Meta:
        verbose_name = "Bot Sozlamasi"
        verbose_name_plural = "Bot Sozlamalari"

    def __str__(self):
        if self.telegram_channel_name:
            return f"Kanal ID: {self.telegram_channel_id}, Kanal Nomi: {self.telegram_channel_name}"
        else:
            return f"Kanal ID: {self.telegram_channel_id}"

        
    def save(self, *args, **kwargs):
        if not self.pk:
            if Config.objects.exists():
                existing_config = Config.objects.first()
                existing_config.telegram_bot_token = self.telegram_bot_token
                existing_config.telegram_channel_id = self.telegram_channel_id
                existing_config.save()
                return
        super().save(*args, **kwargs)


class News(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField(help_text="Yangilik kontentini shu yerda yozing")
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    author = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"

    def get_absolute_url(self):
            return reverse("news_detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # self.send_to_telegram()

    def send_to_telegram(self, request=None):
        config = Config.objects.last()
        if config:
            bot_token = config.telegram_bot_token
            channel_id = config.telegram_channel_id

            full_content = html.unescape(self.content)

            allowed_html_tags = re.sub(r'</?[^builcodea]+>', '', full_content)

            allowed_html_tags = re.sub(r'<img[^>]*>', '', allowed_html_tags)
            allowed_html_tags = re.sub(r'<a([^>]+)>([^<]+)(?!</a>)', r'<a\1>\2</a>', allowed_html_tags)
            allowed_html_tags = re.sub(r'<a([^>]+)>(.*?)</a>', r'<a\1>\2</a>', allowed_html_tags)

            soup = BeautifulSoup(allowed_html_tags, 'html.parser')

            fixed_message = str(soup)

            max_caption_length = 1024
            if len(fixed_message) > max_caption_length:
                short_content = fixed_message[:max_caption_length - 50] + "..."
                more_button = {
                    "text": "Yana...",
                    "url": f"https://a80b-188-113-207-218.ngrok-free.app{self.get_absolute_url()}"
                }
                reply_markup = {
                    "inline_keyboard": [[more_button]]
                }
            else:
                short_content = fixed_message
                reply_markup = {}

            message = f"📰 <b>{self.title}</b>\n\n{short_content}"

            if self.image:
                with open(self.image.path, 'rb') as photo:
                    files = {
                        'photo': photo
                    }
                    data = {
                        "chat_id": channel_id,
                        "caption": message[:max_caption_length],
                        "parse_mode": "HTML",
                        "reply_markup": json.dumps(reply_markup) if reply_markup else None,
                        "disable_web_page_preview": "true" if "http" in short_content else "false"
                    }
                    response = requests.post(f"https://api.telegram.org/bot{bot_token}/sendPhoto", data=data, files=files)
            else:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                payload = {
                    "chat_id": channel_id,
                    "text": message[:max_caption_length],
                    "parse_mode": "HTML",
                    "reply_markup": json.dumps(reply_markup) if reply_markup else None,
                    "disable_web_page_preview": "true" if "http" in short_content else "false"
                }
                response = requests.post(url, data=payload)

            if response.status_code != 200:
                print(f"Error sending message to Telegram: {response.text}")
                # Admin panelda xatolikni ko'rsatish uchun shu yerda qo'shimcha kodlar yozishingiz mumkin
                # Masalan, xatolikni modelga yozish yoki alert ko'rinishida foydalanuvchiga xabar berish
                # admin_panel_show_error(response.text)

class NewsView(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news_views')
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

