from images.models import Image

class ArtPieceService:
    @staticmethod
    def create(model, validated_data, uploaded_images=None):
        instance = model.objects.create(**validated_data)

        if uploaded_images:
            for img in uploaded_images:
                Image.objects.create(content_object=instance, image=img)

        return instance
    
    @staticmethod
    def update(instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance        
    
    @staticmethod
    def delete(instance):
        instance.delete()

    