from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView


# Create your views here.
from .filters import ProductFilter
from .forms import VariationInventoryFormSet, ProductFilterForm
from .mixins import StaffRequiredMixin
from .models import Product, Variation, Category, ProductFeatured, Company, Brand, GenericName, ProductUnit, ProductCommon, ProductImage
from wsc.models import WaterSupplyCompany
from store.models import Store
from .pagination import ProductPagination, CategoryPagination, WSCPagination
from .serializers import (
		CategorySerializer, 
		ProductSerializer,
		 ProductDetailSerializer, 
		 ProductDetailUpdateSerializer,
		 ProductFeaturedSerializer,
		 CompanySerializer,
		 BrandSerializer,
		 GenericNameSerializer,
		 ProductUnitSerializer,
		 WSCSerializer,
		 CommonProductSerializer,
		 AllProductSerializer
		)





# API CBVS


class APIHomeView(APIView):
	# authentication_classes = [SessionAuthentication]
	# permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		data = {
			"auth": {
				"login_url":  api_reverse("auth_login_api", request=request),
				"refresh_url":  api_reverse("refresh_token_api", request=request), 
				"user_checkout":  api_reverse("user_checkout_api", request=request), 
			},
			"address": {
				"url": api_reverse("user_address_list_api", request=request),
				"create":   api_reverse("user_address_create_api", request=request),
			},
			"checkout": {
				"cart": api_reverse("cart_api", request=request),
				"checkout": api_reverse("checkout_api", request=request),
				"finalize": api_reverse("checkout_finalize_api", request=request),
			},
			"products": {
				"count": Product.objects.all().count(),
				"url": api_reverse("products_api", request=request)
			},
			"categories": {
				"count": Category.objects.all().count(),
				"url": api_reverse("categories_api", request=request)
			},
			"orders": {
				"url": api_reverse("orders_api", request=request),
			},
			"inquiry": {
				"url": api_reverse("inquiry_api", request=request),
			},
			"create_cart": {
				"url": api_reverse("create_cart_api", request=request),
			},

			"add_order": {
				"url": api_reverse("create_order_api", request=request),
			},

			"featured_products": {
				"url": api_reverse("product_featured_api", request=request),
			},


			"lists_apis": {
				"generic_names": api_reverse("generic_name_list_api", request=request),
				"brand_names": api_reverse("brands_list_api", request=request),
				"company_names": api_reverse("company_list_api", request=request),
				"product_units": api_reverse("product_unit_list_api", request=request),
			}

		}
		return Response(data)

class CommonProductListAPIView(generics.ListAPIView):
	queryset = ProductCommon.objects.all()
	serializer_class = ProductUnitSerializer

class CompanyListAPIView(generics.ListAPIView):
	queryset = Company.objects.all()
	serializer_class = CompanySerializer
	# pagination_class = CategoryPagination

class ProductUnitListAPIView(generics.ListAPIView):
	queryset = ProductUnit.objects.all()
	serializer_class = ProductUnitSerializer
	# pagination_class = CategoryPagination


class BrandListAPIView(generics.ListAPIView):
	queryset = Brand.objects.all()
	serializer_class = BrandSerializer
	# pagination_class = CategoryPagination


class GenericNameListAPIView(generics.ListAPIView):
	queryset = GenericName.objects.all()
	serializer_class = GenericNameSerializer
	# pagination_class = CategoryPagination


class CategoryListAPIView(generics.ListAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	pagination_class = CategoryPagination



class CategoryRetrieveAPIView(generics.RetrieveAPIView):
	#authentication_classes = [SessionAuthentication]
	#permission_classes = [IsAuthenticated]
	queryset = Category.objects.all()
	serializer_class = CategorySerializer


class WSCListAPIView(generics.ListAPIView):
	queryset = Store.objects.all()
	serializer_class = WSCSerializer
	pagination_class = CategoryPagination



class WSCRetrieveAPIView(generics.RetrieveAPIView):
	#authentication_classes = [SessionAuthentication]
	#permission_classes = [IsAuthenticated]
	queryset = WaterSupplyCompany.objects.all()
	serializer_class = WSCSerializer

class ProductListAPIView(generics.ListAPIView):
	#permission_classes = [IsAuthenticated]
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	filter_backends = [
					filters.SearchFilter, 
					filters.OrderingFilter, 
					DjangoFilterBackend
					]
	# search_fields = ["title", "description"] // old version
	filterset_fields = ["title", "description"]
	ordering_fields  = ["title", "id"]
	filter_class = ProductFilter

	def get_queryset(self):
		user_store = Store.objects.filter(fk_user_id=self.request.user.id).first() #
		
		if user_store is not None:
			print(1)
			if self.request.GET.get('view_my_products', None):
				queryset = Product.objects.filter(fk_store_id=user_store.id)
				return queryset
			# Depo login bhayeko cha bhane 
			# water supply company ko matrai product dekhnu paryo

			queryset = Product.objects.exclude(fk_store_id=None).exclude(fk_store__fk_store_type_id=None).exclude(fk_store__fk_store_type_id=2)
			print(queryset.query)
			return queryset
		if self.request.query_params.get('id'):
			id = self.request.query_params.get('id')
			queryset = Product.objects.filter(id__gte=id)
		queryset = Product.objects.all()
		return queryset


class AllProductListAPIView(generics.ListAPIView): ##for pharma
	#permission_classes = [IsAuthenticated]
	queryset = Product.objects.all()
	serializer_class = AllProductSerializer
	filter_backends = [
					filters.SearchFilter, 
					filters.OrderingFilter, 
					DjangoFilterBackend
					]
	# search_fields = ["title", "description"] // old version
	filterset_fields = ["title", "description"]
	ordering_fields  = ["title", "id"]
	filter_class = ProductFilter

	def get_queryset(self):
		user_store = Store.objects.filter(fk_user_id=self.request.user.id).first() #
		
		if user_store is not None:
			print(1)
			if self.request.GET.get('view_my_products', None):
				queryset = Product.objects.all().order_by('-id')
				return queryset
			# Depo login bhayeko cha bhane 
			# water supply company ko matrai product dekhnu paryo

			queryset = Product.objects.exclude(fk_store_id=None).exclude(fk_store__fk_store_type_id=None).exclude(fk_store__fk_store_type_id=2)
			print(queryset.query)
			return queryset
		if self.request.query_params.get('id'):
			id = self.request.query_params.get('id')
			queryset = Product.objects.filter(id__gte=id)
		queryset = Product.objects.all()
		return queryset


	#pagination_class = ProductPagination


class ProductRetrieveAPIView(generics.RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductDetailSerializer


class ProductFeaturedListAPIView(generics.ListAPIView):
	#permission_classes = [IsAuthenticated]
	# try:
	queryset = Product.objects.all()
	# except Product.DoesNotExist:
	# 	get_queryset = None

	
	serializer_class = ProductFeaturedSerializer
	filter_backends = [
					filters.SearchFilter, 
					filters.OrderingFilter, 
					#filters.DjangoFilterBackend
					]
	search_fields = ["title", "show_price"]
	ordering_fields  = ["title", "id"]
	# filter_class = ProductFilter
	#pagination_class = ProductPagination

# class ProductCreateAPIView(generics.CreateAPIView):
# 	queryset = Product.objects.all()
# 	serializer_class = ProductDetailUpdateSerializer
	
### Product insertion from api #####
class CreateProductAPIView(APIView):
	# authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]
	def post(self, request, *args, **kwargs):
		print(request.POST)
		product_title = request.data.get('title', False)
		description = request.data.get('description', False)
		price = request.data.get('price', False)
		categories = request.data.get('categories', False)
		product_id = request.data.get('product_id', None)
		image  = request.FILES.get('file', None)
		print(image)
		if product_id:
			pass
		else:
			if image is None:
				return Response({"Fail": "Select product image"}, status.HTTP_400_BAD_REQUEST)

		if product_title is None:
			return Response({"Fail": "Product name must be provided"}, status.HTTP_400_BAD_REQUEST)
		if description is None:
			return Response({"Fail": "product description must be provided"}, status.HTTP_400_BAD_REQUEST)
		if price is None:
			return Response({"Fail": "product price must be provided"}, status.HTTP_400_BAD_REQUEST)



		# if categories is None:
		# 	return Response({"Fail": "Select product categories"}, status.HTTP_400_BAD_REQUEST)

			# common = ProductCommon.objects.filter(pk=common_product).first()
	
		if product_id:
			print(product_id)
			product = Product.objects.filter(pk=product_id).first()

			variation = Variation.objects.filter(product_id=product_id).first()
			common_product = ProductCommon.objects.filter(pk=product.fk_common_product_id).first()
			print(price)
			product_image = ProductImage.objects.filter(product_id=product.id).first()
			print(product_image)
			if product_image is None:
				product_image = ProductImage()
			variation.price = price
			variation.save()
		else:
			print(3)
			product = Product()
			common_product = ProductCommon()
			product_image = ProductImage()

		# if common:
		fk_store = Store.objects.filter(fk_user_id=request.user.id).first()
		if not fk_store:
			return Response({"Fail": "Permission denied"}, status.HTTP_400_BAD_REQUEST)

		common_product.title = product_title
		common_product.save()

		product.fk_common_product_id = common_product.id
		product.description = description
		product.price = price
		product.title = common_product.title
		product.fk_store_id = fk_store.id
		product.save()

		if image:
			product_image.product = product
			product_image.image = image
			product_image.save()
			

		return Response({
					'status': True,
					'detail': 'Product Saved successfully'
					})



#### Medical 
class AddProductAPIView(APIView):
	# authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]
	def post(self, request, *args, **kwargs):
		print(request.POST)
		product_title = request.data.get('title', '')
		description = request.data.get('description', '')
		price = request.data.get('price', '')
		category_id = request.data.get('category_id', None)
		brand_id = request.data.get('brand_id', None)
		product_unit_id =request.data.get('product_unit_id', None)
		product_quantity =  request.data.get('product_quantity', None)
		product_id = request.data.get('product_id', None)
		product_amount = request.data.get('product_amount', '')
		generic_names_id =request.data.get('generic_names_id', None)
		company_id =request.data.get('company_id', None)
		image  = request.FILES.get('file', None)
		
		print(image)
		if product_id:
			pass
		else:
			if image is None:
				return Response({"Fail": "Select product image"}, status.HTTP_400_BAD_REQUEST)

		if product_title is None:
			return Response({"Fail": "Product name must be provided"}, status.HTTP_400_BAD_REQUEST)
		if description is None:
			return Response({"Fail": "product description must be provided"}, status.HTTP_400_BAD_REQUEST)
		if price is None:
			return Response({"Fail": "product price must be provided"}, status.HTTP_400_BAD_REQUEST)
		if category_id is None:
			return Response({"Fail": "category must be provided"}, status.HTTP_400_BAD_REQUEST)
		if brand_id is None:
			return Response({"Fail": "brand must be provided"}, status.HTTP_400_BAD_REQUEST)
		if product_unit_id is None:
			return Response({"Fail": "product unit must be provided"}, status.HTTP_400_BAD_REQUEST)
		if generic_names_id is None:
			return Response({"Fail": "Generic name must be provided"}, status.HTTP_400_BAD_REQUEST)
		if company_id is None:
			return Response({"Fail": "Company name must be provided"}, status.HTTP_400_BAD_REQUEST)



		# if categories is None:
		# 	return Response({"Fail": "Select product categories"}, status.HTTP_400_BAD_REQUEST)

			# common = ProductCommon.objects.filter(pk=common_product).first()
	
		if product_id:
			print(product_id)
			product = Product.objects.filter(pk=product_id).first()

			variation = Variation.objects.filter(product_id=product_id).first()
			common_product = ProductCommon.objects.filter(pk=product.fk_common_product_id).first()
			print(price)
			product_image = ProductImage.objects.filter(product_id=product.id).first()
			print(product_image)
			if product_image is None:
				product_image = ProductImage()
			variation.price = price
			variation.save()
		else:
			print(3)
			product = Product()
			common_product = ProductCommon()
			product_image = ProductImage()

		# if common:
		# fk_store = Store.objects.filter(fk_user_id=request.user.id).first()
		# if not fk_store:
		# 	return Response({"Fail": "Permission denied"}, status.HTTP_400_BAD_REQUEST)

		common_product.title = product_title
		common_product.save()

		product.fk_common_product_id = common_product.id
		product.description = description
		product.price = price
		product.title = common_product.title
		product.product_unit_id = product_unit_id
		product.generic_name_id = generic_names_id
		product.company_id = company_id
		product.brand_id = brand_id
		product.amount = product_amount
		# product.fk_store_id = fk_store.id
		product.save()

		if product_quantity:
			variation = Variation.objects.filter(product_id=product.id).first()
			variation.inventory = product_quantity
			variation.save()


		if image:
			product_image.product = product
			product_image.image = image
			product_image.save()
			

		return Response({
					'status': True,
					'detail': 'Product Saved successfully'
					})




# CBVs

class CategoryListView(ListView):
	model = Category
	queryset = Category.objects.all()
	template_name = "products/product_list.html"


class CategoryDetailView(DetailView):
	model = Category

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		product_set = obj.product_set.all()
		default_products = obj.default_category.all()
		products = ( product_set | default_products ).distinct()
		context["products"] = products
		return context



class VariationListView(StaffRequiredMixin, ListView):
	model = Variation
	queryset = Variation.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(VariationListView, self).get_context_data(*args, **kwargs)
		context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
		return context

	def get_queryset(self, *args, **kwargs):
		product_pk = self.kwargs.get("pk")
		if product_pk:
			product = get_object_or_404(Product, pk=product_pk)
			queryset = Variation.objects.filter(product=product)
		return queryset

	def post(self, request, *args, **kwargs):
		formset = VariationInventoryFormSet(request.POST, request.FILES)
		if formset.is_valid():
			formset.save(commit=False)
			for form in formset:
				new_item = form.save(commit=False)
				#if new_item.title:
				product_pk = self.kwargs.get("pk")
				product = get_object_or_404(Product, pk=product_pk)
				new_item.product = product
				new_item.save()
				
			messages.success(request, "Your inventory and pricing has been updated.")
			return redirect("products")
		raise Http404






def product_list(request):
	qs = Product.objects.all()
	ordering = request.GET.get("ordering")
	if ordering:
		qs = Product.objects.all().order_by(ordering)
	f = ProductFilter(request.GET, queryset=qs)
	return render(request, "products/product_list.html", {"object_list": f })


class FilterMixin(object):
	filter_class = None
	search_ordering_param = "ordering"

	def get_queryset(self, *args, **kwargs):
		try:
			qs = super(FilterMixin, self).get_queryset(*args, **kwargs)
			return qs
		except:
			raise ImproperlyConfigured("You must have a queryset in order to use the FilterMixin")

	def get_context_data(self, *args, **kwargs):
		context = super(FilterMixin, self).get_context_data(*args, **kwargs)
		qs = self.get_queryset()
		ordering = self.request.GET.get(self.search_ordering_param)
		if ordering:
			qs = qs.order_by(ordering)
		filter_class = self.filter_class
		if filter_class:
			f = filter_class(self.request.GET, queryset=qs)
			context["object_list"] = f
		return context




class ProductListView(FilterMixin, ListView):
	model = Product
	queryset = Product.objects.all()
	filter_class = ProductFilter


	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		context["now"] = timezone.now()
		context["query"] = self.request.GET.get("q") #None
		context["filter_form"] = ProductFilterForm(data=self.request.GET or None)
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query)
				)
			try:
				qs2 = self.model.objects.filter(
					Q(price=query)
				)
				qs = (qs | qs2).distinct()
			except:
				pass
		return qs


import random
class ProductDetailView(DetailView):
	model = Product
	#template_name = "product.html"
	#template_name = "<appname>/<modelname>_detail.html"
	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		instance = self.get_object()
		#order_by("-title")
		context["related"] = sorted(Product.objects.get_related(instance)[:6], key= lambda x: random.random())
		return context





def product_detail_view_func(request, id):
	#product_instance = Product.objects.get(id=id)
	product_instance = get_object_or_404(Product, id=id)
	try:
		product_instance = Product.objects.get(id=id)
	except Product.DoesNotExist:
		raise Http404
	except:
		raise Http404

	template = "products/product_detail.html"
	context = {	
		"object": product_instance
	}
	return render(request, template, context)

