from rest_framework import serializers
from .models import Product, Category  ,ProductImage
from django.utils.crypto import get_random_string
from django.utils.text import slugify



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

    title = serializers.CharField(max_length =255)
    slug = serializers.CharField(required =True)
    sku = serializers.CharField(max_length =100)
    description = serializers.CharField()
    product_type = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    category_name = serializers.CharField(source='category.name', read_only=True)


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
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:

        model = Product

        fields = [ 

            "title",
            "slug",
            "description",
            "product_type",
            "sku",
            "category",
            "catogoty_name",
            "price",
            "original_price",
            "in_stock",
            "stock_quantity"
            "meta_title",
            "meta_description",
            "meta_keywords",

            ]
        
        extra_kewargs ={
            "meta_title": {"required": False, "allow_blank": True},
            "meta_description": {"required": False, "allow_blank": True},
            "meta_keywords": {"required": False},
        }

        def validate_price(self,value):

            if value  is not None and value < 0:
                raise serializers.ValidationError("Price should be greater than zero ")
            return value 
        
        
            
        def validate_original_price(self,value):

            if value is not None and value < 0:
                raise serializers.ValidationError("Original price cannot be negative.")
            
            return value
            

        def validate_meta_keywords(self,value):
                if value is None:
                    return value
                
                if not isinstance(value,list):
                    raise serializers.ValidationError("meta_keywords should be a list ")
                
                if len(value) > 0 :
                    raise serializers.ValidationError(" only maximum 10 keywords are allowed  ")
                
                for keyword in value:
                    if not isinstance(keyword,str):
                        raise serializers.ValidationError("keywords should me  a string ") 
                
                return value
                

        def validate(self,attrs):
            price = attrs.get("price")
            original_price = attrs.get("original_price")

            if price is not None and original_price is not None:

                if price > original_price :

                    raise serializers.ValidationError({
                    "price": "Price cannot be greater than original price."
                })

            return attrs 
        

        def generate_unique_sku(self, title):
            base_sku = title[:3].upper()
            while True:
                sku = f"{base_sku}-{get_random_string(6).upper()}"
                if not Product.objects.filter(sku=sku).exists():
                    return sku
                
            
        def create(self ,validated_data):
            if "slug" in validated_data or not validated_data["slug"]:

                validated_data["slug"] = slugify(validated_data["title"])
                validated_data["sku"] = self.generate_unique_sku(validated_data["title"])

            return super().create(validated_data)
        


        def update(self,instance, validated_data):
                  
            if "slug" in validated_data or not validated_data["slug"]:

                validated_data["slug"] = slugify(validated_data.get("title", instance.title))
                
            return super().update(instance,validated_data)
        
            
        
     


class ProductDetailSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    basic_info = serializers.SerializerMethodField()
    price_info = serializers.SerializerMethodField()
    seo_info   = serializers.SerializerMethodField()
    source_info = serializers.SerializerMethodField()
    images = ProductImageSerilaizer(many =True)


    def get_basic_info(self,obj):

        return ProductBasicInfoSerializer({
            'title': obj.title,
            'slug': obj.slug,
            'description': obj.description,
            'product_type': obj.product_type,
            'sku':obj.sku,
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
    














    
