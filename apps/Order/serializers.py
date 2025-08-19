from .models import Cart ,CartItem 
from rest_framework import serializers 
from apps.Auth.models import User
from apps.ProductsManagement.models import Product,Inventory


class CartItemInputSerializers(serializers.Serializer):
    product_id = serializers.IntegerField(required =True)
    quantity = serializers.IntegerField(required =True)


class AddtoCartItemSerilaizer(serializers.Serializer):
    items = CartItemInputSerializers(many=True)

    def validate(self, attrs):

        validated_items = []
        for item in attrs['items']:

            try:
                product = Product.objects.get(id=item['product_id'])
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {item['product_id']} not found")

            if not product:
                raise serializers.ValidationError("Product not found")
            
            product_in_inventory = Inventory.objects.filter(product=product).first()


            if not product_in_inventory:
                raise serializers.ValidationError("Product not found in inventory")
            
            if product_in_inventory.quantity < item['quantity']:
                raise serializers.ValidationError("Not enough quantity in inventory")
            
            if item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than 0")
            

            validated_items.append({
                'product_id': item['product_id'],
                'quantity': item['quantity'],
                'product_price_at_time': product.price
            })


        
        attrs['validated_items']= validated_items
        return attrs
    

   
    def create(self, validated_data):
            
            user = self.context['request'].user
            cart, _ = Cart.objects.get_or_create(user=user)

            for item in validated_data['validated_items']:

                CartItem.objects.update_or_create(
                    cart=cart,
                    product_id=item['product_id'],
                    defaults={
                        'quantity': item['quantity'],
                        'price_at_time': item['product_price_at_time']
                    }
                )
            return cart   

    
    def update(self, instance, validated_data):
       
        for item in validated_data['validated_items']:

            try:
                cart_item = CartItem.objects.get(cart=instance, product=item['product_id'])
                cart_item.quantity = item['quantity']
                cart_item.save()

            except CartItem.DoesNotExist:
                raise serializers.ValidationError("Invalid product in cart")

        return instance  




    

class ProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class CartItemSerializer(serializers.ModelSerializer):

    product = ProductMiniSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'price_at_time','total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.price_at_time
    

class CartItemDetailSerializer(serializers.ModelSerializer):
    cart_id = serializers.IntegerField(source="id")
    items =CartItemSerializer(many=True,source='cart_item',read_only=True)
    total_price = serializers.SerializerMethodField(read_only =True)
    

    class Meta:
        model = Cart
        fields = ['cart_id','total_price', 'items' ]

    def get_total_price(self, obj):
        return   (sum([item.quantity * item.price_at_time for item in obj.cart_item.all()]))
   





        
    
    
            
        





        
            
            

            


     
        

        
        

       
        

        