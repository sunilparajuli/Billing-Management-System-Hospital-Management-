from rest_framework import serializers

from carts.mixins import TokenMixin
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import UserAddress, Order, Quotation, UserCheckout
from products.models import Product, ProductImage
from carts.models import Cart, CartItem
import pprint

# parse order token
# check order not complete
# nonce is coming through
# mark cart complete
# mark order done

class QuotationSerializer(serializers.ModelSerializer):
	authentication_classes = [SessionAuthentication, BasicAuthentication]
	permission_classes = [IsAuthenticated]
	class Meta:
		model = Quotation
		fields= '__all__'
		# fields = []


class FinalizedOrderSerializer(TokenMixin, serializers.Serializer):
	order_token = serializers.CharField()
	payment_method_nonce = serializers.CharField()
	order_id =  serializers.IntegerField(required=False)
	user_checkout_id = serializers.IntegerField(required=False)


	def validate(self, data):
		order_token = data.get("order_token")
		order_data = self.parse_token(order_token)
		order_id = order_data.get("order_id")
		user_checkout_id = order_data.get("user_checkout_id")

		try:
			order_obj = Order.objects.get(id=order_id, user__id=user_checkout_id)
			data["order_id"] = order_id
			data["user_checkout_id"] = user_checkout_id
		except:
			raise serializers.ValidationError("This is not a valid order for this user.")

		payment_method_nonce = data.get("payment_method_nonce")
		if payment_method_nonce == None:
			raise serializers.ValidationError("This is not a valid payment method nonce")

		return data
	


class OrderDetailSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="order_detail_api")
	subtotal = serializers.SerializerMethodField()
	class Meta:
		model = Order
		fields = [
			"url",
			"order_id",
			"user",
			"shipping_address",
			"billing_address",
			"shipping_total_price",
			"subtotal",
			"order_total",
		]

	def get_subtotal(self, obj):
		return obj.cart.subtotal



class OrderSerializer(serializers.ModelSerializer):
	subtotal = serializers.SerializerMethodField()
	class Meta:
		model = Order
		fields = [
			"id",
			"user",
			"shipping_address",
			"billing_address",
			"shipping_total_price",
			"subtotal",
			"order_total",
		]

	def get_subtotal(self, obj):
		return obj.cart.subtotal



class UserAddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserAddress
		fields = [
			"id",
			"user",
			"type",
			"street",
			"state",
			"city",
			"zipcode",
			"phone"
		]

	def create(self,  validated_data):
		user = self.context['request'].user
		usercheckout = UserCheckout.objects.filter(user_id=user.id).first()
		
		if usercheckout is None:

			usercheckout = UserCheckout()
			usercheckout.user_id = user.id
			usercheckout.email = user.email
			usercheckout.braintree_id = '0'
			usercheckout.save()

		useraddress = UserAddress.objects.filter(user_id=usercheckout.id).first()
		if useraddress is None:
			print('sadsd')
			useraddress = UserAddress()

		useraddress.user_id = usercheckout.id
		useraddress.type = validated_data.get('type')
		useraddress.street = validated_data.get('street')
		useraddress.city =  validated_data.get('city')
		useraddress.zipcode = validated_data.get('zipcode')
		useraddress.state = validated_data.get('state')
		useraddress.phone = validated_data.get('phone')
		useraddress.save()
		return useraddress





class CartOrderSerializer(serializers.ModelSerializer):
	order_total = serializers.DecimalField(required=False, max_digits=50, decimal_places=2,)
	class Meta:
		model = Order
		fields = '__all__'

	def create(self, validated_data):
		#pprint.pprint(self.context['request'].__dict__)
		pprint.pprint(validated_data)
		user =  self.context['request'].user
		
		# item_quantity = validated_data.pop('item_quantity')
		cart = Cart.objects.filter(user_id=user.id).filter(active=1).first()
		if cart is None:
			raise serializers.ValidationError("This is not a valid cart, first make cart, /api/cart/ or add item to cart ")
		usercheckout_user = UserCheckout.objects.filter(user_id=user).first()
		if usercheckout_user is None:
			usercheckout_user = UserCheckout()
			usercheckout_user.user_id = user.id
			usercheckout_user.email = user.email
			usercheckout_user.braintree_id = '0'

			usercheckout_user.save()

		useraddress = UserAddress.objects.filter(user_id=usercheckout_user.id).first()
		if useraddress is None:
			useraddress = UserAddress()
			useraddress.user_id = usercheckout_user.id
			useraddress.save()

		order = Order()
		order.order_id = cart.id
		order.status = 1
		order.shipping_total_price = 100
		order.order_total = cart.total
		order.billing_address = useraddress
		order.shipping_address = useraddress
		order.user_id = usercheckout_user.id
		order.cart_id = cart.id
		order.order_latitude = validated_data.get("order_latitude")
		order.order_longitude = validated_data.get("order_longitude")

		print(self.context['request'].__dict__)
		order.fk_ordered_store = validated_data.get("fk_ordered_store")
		order.fk_payment_method = validated_data.get("fk_payment_method")

		print(order.__dict__)
		order.save()


		cart.active=0
		cart.save()

		return order



class OrderListStoreSerializer(serializers.ModelSerializer):
	billing_address = serializers.SerializerMethodField()
	mobile = serializers.SerializerMethodField()
	class Meta:
		model = Order
		fields = ['id', 'status', 'is_delivered', 'is_paid', 
		'order_longitude', 'order_latitude', 'cart', 'user', 'order_total',
		'billing_address', 'fk_ordered_store', 'fk_delivery_user',
		 'fk_payment_method', 'mobile']

	def get_billing_address(self, obj):
		return str(obj.billing_address.street)

	def get_mobile(self, obj):
		return obj.user.user.mobile



class CartOrderListStoreSerializer(serializers.ModelSerializer):
	# cart_orders = serializers.SerializerMethodField()
	class Meta:
		model = CartItem
		fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
	#item = CartVariationSerializer(read_only=True)
	# url = serializers.HyperlinkedIdentityField(view_name='products_detail_api')
	item = serializers.SerializerMethodField()
	product_id = serializers.SerializerMethodField()
	item_title = serializers.SerializerMethodField()
	product = serializers.SerializerMethodField()
	price = serializers.SerializerMethodField()
	image = serializers.SerializerMethodField()
	class Meta:
		model = CartItem
		fields = [
			# "url",
			"product_id",
			"image",
			"item",
			"item_title",
			"price",
			"product",
			"quantity",
			"line_item_total",
		]

	def get_item(self,obj):
		return obj.item.id

	def get_product_id(self, obj):
		return obj.id
		
	def get_item_title(self, obj):
		return "%s %s" %(obj.item.product.title, obj.item.title)

	def get_product(self, obj):
		return obj.item.product.id

	def get_price(self, obj):
		print(obj.item.sale_price)
		print(obj.item.price)
		print(obj.item.id)
		# print(obj.item.sale_price)
		if obj.item.sale_price is None:
			return obj.item.price
		return obj.item.sale_price

	def get_image(self, obj):
		# image_url = ProductImage.objects.filter(product_id=obj.item.id).first()
		variation = obj.item
		product = variation.product

		image_url = ProductImage.objects.filter(product=product).first()
		print(obj.item.id)
		print(obj.__dict__)
		print(image_url)
		# return ""
		# print(list(image_url.values('image')))
		
		imageUrl = "/static/no-image.jpg"
		d = image_url.__dict__
		if 'image' in d:
			imageUrl = d['image']



		# return image_url.image

		return imageUrl


		# cart_items = CartItem.objects.filter(cart_id=cart.id)





