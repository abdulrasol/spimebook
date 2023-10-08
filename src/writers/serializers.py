from rest_framework import serializers
from writers.models import Writer


class WriterSerializer(serializers.HyperlinkedModelSerializer):
    # image = serializers.HyperlinkedIdentityField()

    class Meta:
        model = Writer
        fields = ['id', 'name', 'bio', 'image', 'short', 'born_date']
