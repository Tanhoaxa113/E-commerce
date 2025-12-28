from django.shortcuts import render
from rest_framework import generics
from .models import Builder
from .serializers import BuilderSerializer

class BuilderView(generics.ListAPIView):
    serializer_class = BuilderSerializer

    def get_queryset(self):
        data = super().get(self.request, filter = 'CPU')
        data['CPU'] = Builder.objects.filter('CPU')

        return data
        
