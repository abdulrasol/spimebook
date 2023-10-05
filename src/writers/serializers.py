from rest_framework import serializers
from writers.models import Writer

class WriterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    short = serializers.CharField()
    bio = serializers.CharField()
    image = serializers.ImageField(allow_null=True)
    born_date = serializers.DateField()

    def create(self, validated_data):
        return Writer.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.short = validated_data.get('short', instance.short)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.image = validated_data.get('image', instance.image)
        instance.born_date = validated_data.get('born_date', instance.born_date)
        instance.save()
        return instance


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Writer
        fields = ['name', 'short', 'bio', 'image', 'born_date']



class SerializerWriter(serializers.ModelSerializer):
    image_url = serializers.URLField(write_only=True)  # Add a field to accept the image URL

    class Meta:
        model = Writer
        fields = ['name', 'short', 'bio', 'image', 'born_date']

    def create(self, validated_data):
        image_url = validated_data.pop('image_url', None)

        # If an image URL is provided, download and save it
        if image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_name = image_url.split('/')[-1]
                validated_data['image'] = ContentFile(response.content, name=image_name)

        return super().create(validated_data)
        
    def update(self, instance, validated_data):
        # Similar to create, handle image URL if provided during update
        image_url = validated_data.pop('image_url', None)
        if image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_name = image_url.split('/')[-1]
                instance.image = ContentFile(response.content, name=image_name)

        return super().update(instance, validated_data)


#{'name': 'AbdulRasol','short': 'Google','bio': 'From Google','image': image_file,'born_date': '2023-10-05'}