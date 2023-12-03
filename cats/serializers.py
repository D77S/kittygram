from rest_framework import serializers

from .models import Cat


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        #  вместо всех полей...
        #  fields = '__all__'
        #  сериализуем только некоторые. Например, без поля "id"
        fields = ('name', 'color', 'birth_year')
