from rest_framework import serializers
from .models import Product, Category  ,ProductImage



class CategorySerilaizer(serializers.ModelSerializer):

    class Meta:
        model =Category
        fields = '__all__'
        read_only_fields = ('id','slug')


class ProductImageSerilaizer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields ='__all__'


class ProductBasicInfoSerializer(serializers.Serializer):

    title = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField()
    product_type = serializers.CharField()
    category = serializers.CharField(allow_null=True)


class ProductPriceInfoSerializer(serializers.Serializer):

    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    original_price = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    in_stock = serializers.BooleanField()
    stock_quantity = serializers.IntegerField()


class ProductMetaInfoSerializer(serializers.Serializer):

    meta_title = serializers.CharField(allow_blank=True, allow_null=True)
    meta_description = serializers.CharField(allow_blank=True, allow_null=True)
    meta_keywords = serializers.ListField()


class ProductSourceInfoSerializer(serializers.Serializer):
    source_url = serializers.URLField(allow_blank = True,allow_null = True)
    source_website = serializers.CharField(allow_blank=True, allow_null=True)



class ProductCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('id', 'slug')


class ProductDetailSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    basic_info = serializers.SerializerMethodField()
    price_info = serializers.SerializerMethodField()
    seo_info   = serializers.SerializerMethodField()
    source_info = serializers.SerializerMethodField()
    product_images = ProductImageSerilaizer(many =True)


    def get_basic_info(self,obj):
        return ProductBasicInfoSerializer({
            'title': obj.title,
            'slug': obj.slug,
            'description': obj.description,
            'product_type': obj.product_type,
            'category': obj.category.name if obj.category else None
        }).data
    
    
    def get_price_info(self,obj):
        return ProductPriceInfoSerializer({
            'price': obj.price,
            'original_price': obj.original_price,
            'in_stock': obj.in_stock,
            'stock_quantity': obj.stock_quantity
        }).data 
    

    def get_seo_info(self, obj):
        return ProductMetaInfoSerializer({
            'meta_title': obj.meta_title,
            'meta_description': obj.meta_description,
            'meta_keywords': obj.meta_keywords
        }).data

    def get_source_info(self, obj):
        return ProductSourceInfoSerializer({
            'source_url': obj.source_url,
            'source_website': obj.source_website
        }).data
    














    
