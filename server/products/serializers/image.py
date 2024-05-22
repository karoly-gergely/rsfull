from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from server.products.models import ImageInstance


class ImageInstanceSerializer(serializers.ModelSerializer):
    s3_image = serializers.ImageField(
        required=True,
        validators=[FileExtensionValidator(
            allowed_extensions=[
                'jpg', 'jpeg', 'webp', 'tiff', 'png', 'svg', 'avif'
            ]
        )],
    )

    def validate(self, data):
        file_object = data.get('s3_image')
        if file_object.size > 2097152:
            raise ValidationError(
                f"{file_object.name} file should be under 2MB!"
            )

        return data

    class Meta:
        model = ImageInstance
        fields = (
            "id",
            "s3_image",
        )
        read_only_fields = (
            "id",
        )
