from rest_framework import serializers
from .models import Shoes, Supplier


class ShoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoes
        fields = ['brand', 'name', 'description', 'price', 'exist', 'supplier']
