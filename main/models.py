from django.db import models

# Create your models here.



class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    author = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


class NewsView(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='news_views')
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)