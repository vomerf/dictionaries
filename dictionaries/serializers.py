from rest_framework import serializers
from dictionaries.models import Dictionary, DictionaryItem


class DictionarySerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="pk")

    class Meta:
        model = Dictionary
        fields = ("id", "code", "name")


class DictionaryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DictionaryItem
        fields = ("code", "value")


class DictionaryElementsSerializer(serializers.Serializer):
    elements = DictionaryItemSerializer(many=True)