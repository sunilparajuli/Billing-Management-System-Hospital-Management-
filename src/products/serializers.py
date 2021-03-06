from rest_framework import serializers
from django.conf import settings

from .models import Category, Product, Variation, ProductFeatured, Company, GenericName, Brand, ProductUnit, ProductImage, ProductCommon, UserVariationQuantityHistory, VariationBatch
from store.models import Store
from store.serializers import *



class CommonProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductCommon
		fields = '__all__' 

class ImageSerializer(serializers.ModelSerializer):
	# discount = serializers.SerializerMethodField()
	class Meta:
		model = ProductImage
		fields = '__all__'

class UserVariationQuantityHistorySerializer(serializers.ModelSerializer):
	class Meta:
		model = UserVariationQuantityHistory
		fields = '__all__'


class VariationSerializer(serializers.ModelSerializer):
	# discount = serializers.SerializerMethodField()
	class Meta:
		model = Variation
		fields = '__all__'




class VariationBatchSerializer(serializers.ModelSerializer):
	fk_variation_name = serializers.SerializerMethodField()
	# fk_variation = VariationSerializer()
	class Meta:
		model = VariationBatch
		fields ='__all__'

	def get_fk_variation_name(self, obj):
		if obj.batchno:
			return obj.fk_variation.title + ' ' + obj.batchno
		return obj.fk_variation.title




class UserVariationQuantityHistorySerializer(serializers.ModelSerializer):
	variation = VariationSerializer()
	class Meta:
		model = UserVariationQuantityHistory
		fields = '__all__'


class ProductVariationListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Variation
		fields = '__all__'





class ProductDetailUpdateSerializer(serializers.ModelSerializer):
	variation_set = VariationSerializer(many=True, read_only=True)
	
	image = serializers.SerializerMethodField()
	class Meta:
		model = Product
		fields = [
			"id",
			"title",
			"description",
			"price",
			"image",

			"variation_set",
			
		]


	def get_image(self, obj):
		try:
			return obj.productimage_set.first().image.url
		except:
			return None



	def create(self, validated_data):
		title = validated_data["title"]
		Product.objects.get(title=title)
		product = Product.objects.create(**validated_data)
		return product

	def update(self, instance, validated_data):
		instance.title = validated_data["title"]
		instance.save()
		return instance
	# def update


class ProductDetailSerializer(serializers.ModelSerializer):
	# variation_set =  #VariationSerializer(many=True, read_only=True)
	# variation_set = serializers.SerializerMethodField(source='get_variation_set', read_only=True)
	# image = serializers.SerializerMethodField()
	# fk_common_product = CommonProductSerializer()
	class Meta:
		model = Variation
		fields = '__all__'
		
	def get_variation_set(self, obj):
		return VariationSerializer(obj.variation_set.filter(is_internal=False), many=True).data

		# variation_set1 = serializers.SerializerMethodField('_get_children')
		# def _get_children(self, obj):
		# 	serializer = VariationSerializer(Variation.objects.filter(is_internal=False).filter(product=obj), many=True, read_only=True)
		# 	print(serializer)
		# 	return serializer.data

	def get_image(self, obj):
		image_url = obj.productimage_set.first()
		url = '/no-image.jpg'
		if image_url is not None:
			url=image_url.image.url
		return url
		#return obj.productimage_set.first().image.url



# class AllProductDetailSerializer(serializers.ModelSerializer):
# 	variation_set = VariationSerializer(many=True, read_only=True)
# 	image = serializers.SerializerMethodField()
# 	class Meta:
# 		model = Product
# 		fields = [
# 			"id",
# 			"title",
# 			"description",
# 			"price",
# 			"image",
# 			"variation_set",
# 		]

# 	def get_image(self, obj):
# 		image_url = obj.productimage_set.first()
# 		url = '/no-image.jpg'
# 		if image_url is not None:
# 			url=image_url.image.url
# 		return url
# 		#return obj.productimage_set.first().image.url



class ProductSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='products_detail_api')
	variation_set = VariationSerializer(many=True)
	fk_store = StoreSerializer(read_only=True)
	image = serializers.SerializerMethodField()
	productimage_set = ImageSerializer(many=True, read_only=True)

	class Meta:
		model = Product
		fields = [
			"url",
			"id",
			"title",
			"image",
			"description",
			"variation_set",
			"productimage_set",
			'fk_common_product_id',
			"fk_store"
		]

	def get_image(self, obj):
		try:
			return  obj.productimage_set.first().image.url
		except:
			return None




	# def get_images_set(self, obj):
	# 	try:
	# 		# return obj.productimage_set.filter().image.url
	# 		return ProductImage.objects.filter(product_id=2).get().__dict__['image']
	# 	except:
	# 		return None


class ProductFilterSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='products_detail_api')
	variation_set = VariationSerializer(many=True)
	image = serializers.SerializerMethodField()
	class Meta:
		model = Product
		fields = [
			"url",
			"id",
			"title",
			"image",
			"variation_set",
		]

	def get_image(self, obj):
		try:
			return obj.productimage_set.first().image.url
		except:
			return None


class ProductFeaturedSerializer(serializers.ModelSerializer):
	# url = serializers.HyperlinkedIdentityField(view_name='products_detail_api')
	# variation_set = VariationSerializer(many=True)
	image = serializers.SerializerMethodField()
	# title = serializers.SerializerMethodField()
	class Meta:
		model = ProductCommon
		fields = '__all__'

	
	def get_image(self, obj):
		try:
			product = Product.objects.filter(fk_common_product_id=obj.id).first()
			return product.productimage_set.first().image.url
		except:
			return None

	def get_title(self, obj):
		title = obj.title
		store = obj.fk_store.title
		return title+store
class SubCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'title']



class CategorySerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='category_detail_api')
	product_set = ProductSerializer(many=True)
	# fk_category = SubCategorySerializer(many=True)
	children_list = serializers.SerializerMethodField('_get_children')
	def _get_children(self, obj):
		serializer = SubCategorySerializer(Category.objects.filter(fk_category=obj.id), many=True)
		return serializer.data


	class Meta:
		model = Category
		fields = [
			"url",
			"id",
			"title",
			"image",
			"description",
			"product_set", ## obj.product_set.all()
			"children_list"
			# 'fk_category'
			#"default_category",

		]




	class Meta:
		model = Store
		fields = [
			"url",
			"id",
			"title",
			# "image",
			# "description",
			"product_set", ## obj.product_set.all()
			# "children_list"
			# 'fk_category'
			#"default_category",

		]




class CompanySerializer(serializers.ModelSerializer):
	# company_id = serializers.SerializerMethodField()
	# title = serializers.SerializerMethodField()


	class Meta:
		model = Company
		fields = ['id','title'] 


class GenericNameSerializer(serializers.ModelSerializer):
	# company_id = serializers.SerializerMethodField()
	# title = serializers.SerializerMethodField()


	class Meta:
		model = GenericName
		fields = ['id','title'] 


class BrandSerializer(serializers.ModelSerializer):
	# company_id = serializers.SerializerMethodField()
	# title = serializers.SerializerMethodField()


	class Meta:
		model = Brand
		fields = ['id','title'] 


class ProductUnitSerializer(serializers.ModelSerializer):
	# company_id = serializers.SerializerMethodField()
	# title = serializers.SerializerMethodField()


	class Meta:
		model = ProductUnit
		fields = ['id','title'] 

class CategoriesSerializer(serializers.ModelSerializer):
	# company_id = serializers.SerializerMethodField()
	# title = serializers.SerializerMethodField()


	class Meta:
		model = Category
		fields = '__all__'


class AllProductSerializer(serializers.ModelSerializer): ##pharma
	url = serializers.HyperlinkedIdentityField(view_name='all_products_detail_api')
	variation_set = VariationSerializer(many=True)
	image = serializers.SerializerMethodField()
	productimage_set = ImageSerializer(many=True, read_only=True)
	company = CompanySerializer()
	brand = BrandSerializer()
	category = serializers.SerializerMethodField()
	generic_name = GenericNameSerializer()
	
	class Meta:
		model = Product
		fields = [
			"url",
			"id",
			"title",
			"image",
			"price",
			"description",
			"variation_set",
			"productimage_set",
			"company",
			"brand",
			"generic_name",
			"category"
		]

	def get_image(self, obj):
		try:
			return  obj.productimage_set.first().image.url
		except:
			return None
	def get_category(self, obj):
		serializer = SubCategorySerializer(Category.objects.filter(fk_category=obj.id), many=True)
		return serializer.data

#CREATE RETRIEVE UPDATE DESTROY

class AllProductDetailSerializer(serializers.ModelSerializer):
	variation_set = VariationSerializer(many=True, read_only=True)
	image = serializers.SerializerMethodField()
	generic_name_id = serializers.SerializerMethodField()
	company_id = serializers.SerializerMethodField()
	product_unit_id = serializers.SerializerMethodField()
	category_id = serializers.SerializerMethodField()
	brand_id = serializers.SerializerMethodField()

	
	class Meta:
		model = Product
		fields = [
			"id",
			"title",
			"description",
			"price",
			"image",
			"variation_set",
			"brand_id",
			"category_id",
			"product_unit_id",
			"company_id",
			"generic_name_id",
			"amount"

		]

	def get_company_id(self, obj):
		return obj.company_id

	def get_product_unit_id(self, obj):
		return obj.product_unit_id

	def get_generic_name_id(self, obj):
		return obj.brand_id

	def get_company_id(self, obj):
		return obj.company_id
	
	def get_brand_id(self, obj):
		return obj.brand_id

	def get_category_id(self, obj):
		cat = obj.categories.all().first()
		if cat:
			return cat.id
		return None

	def get_image(self, obj):
		image_url = obj.productimage_set.first()
		url = '/no-image.jpg'
		if image_url is not None:
			url=image_url.image.url
		return url



class ProductVariationSerializer(serializers.ModelSerializer):
	# variation_set = VariationSerializer(many=True, read_only=True)
	# image = serializers.SerializerMethodField()
	product = ProductSerializer()
	class Meta:
		model = Variation
		fields = '__all__'
		#return obj.productimage_set.first().image.url	 