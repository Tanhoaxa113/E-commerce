from .models import *
from rest_framework import serializers

class BuilderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Builder
        fields = '__all__'

    def get_price(self, obj):
        return obj.get_price()