from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import News
from .serializers import NewsSerializer



class NewsListAPIView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class NewsDetailAPIView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        client_ip = self.get_client_ip(request)

        if not NewsView.objects.filter(news=instance, ip_address=client_ip).exists():
            instance.views += 1
            instance.save()
            NewsView.objects.create(news=instance, ip_address=client_ip, viewed_at=timezone.now())

        return super().retrieve(request, *args, **kwargs)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip