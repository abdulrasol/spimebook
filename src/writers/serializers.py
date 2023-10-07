from rest_framework import serializers
from writers.models import Writer


class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ['name', 'bio', 'image', 'short', 'born_date']
