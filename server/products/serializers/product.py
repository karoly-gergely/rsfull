from django.db import transaction
from rest_framework import serializers

from server.products.enums import CurrencyChoices
from server.products.models import Product
from server.products.serializers.image import ImageInstanceSerializer


class ProductListSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(max_length=255, required=True)
    price = serializers.DecimalField(
        min_value=0, decimal_places=2, max_digits=11, required=True
    )
    currency = serializers.ChoiceField(
        required=True, allow_blank=False,
        choices=CurrencyChoices.choices
    )

    # Creation specific
    description = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "thumbnail",
            "name",
            "price",
            "description",
            "currency",
        )
        read_only_fields = (
            "id",
        )

    def get_thumbnail(self, obj):
        first_image = obj.images.first()
        if first_image:
            return ImageInstanceSerializer(first_image).data
        return None

    def validate(self, data):
        validated_data = data

        validated_data['user'] = self.context['request'].user
        validated_data['name'] = data.get('name').strip()

        # Images
        if 'images' in self.context['request'].FILES:
            new_images = [
                {'s3_image': image} for image
                in self.context['request'].FILES.getlist('images')
            ]
            images_serializer = ImageInstanceSerializer(
                many=True, data=new_images
            )
            images_serializer.is_valid(raise_exception=True)
            validated_data['images'] = images_serializer.validated_data

        return data

    @transaction.atomic
    def create(self, validated_data):
        image_dicts = None
        if 'images' in validated_data:
            image_dicts = validated_data.pop('images')
        new_product = Product.objects.create(**validated_data)

        if image_dicts:
            image_and_product_dicts = [
                {'s3_image': image['s3_image'], 'product': new_product}
                for image in image_dicts
            ]
            images_serializer = ImageInstanceSerializer(many=True)
            images_serializer.create(image_and_product_dicts)

        return new_product
