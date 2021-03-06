# from django_filters import FilterSet
import django_filters
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import Adjustment, Purchase
from products.models import Variation
from products.filters import VariationFilter
from .filters import AdjustmentFilter
from django_filters import FilterSet, CharFilter, NumberFilter
from .filters import PurchaseFilter, SalesFilter
from carts.models import Cart

class UsersDataTableFilterSet(django_filters.FilterSet):
    
    class Meta:
        model = Variation
        fields= '__all__'
        # maybe works
        #exclude=''
        #
        #fields=None
        #fields=['id'] #works
        #fields=None
        #filter_fields = __all__

class ProductFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Variation
        fields = ['title']
# class VariationDataTableFilterSet(FilterSet):
#     class Meta:
#         model = Variation
#         # fields= '__all__'
#         # maybe works
#         # exclude=''
#         #
#         #fields=None
#         fields=['title'] #works
#         #fields=None
#         #filter_fields = __all__
    

from rest_framework import serializers
class VariationDataTableSerializer(serializers.ModelSerializer):
	class Meta:
		model = Variation
		fields= '__all__'
from rest_framework import pagination
from rest_framework.response import Response
# https://github.com/encode/django-rest-framework/blob/master/rest_framework/pagination.py
# see fields to overide from PageNumberPagination
class DataTablePagination(pagination.PageNumberPagination):
    page_size = 100
    #page_size_query_param = 'page_size'
    page_size_query_param = 'length'
    max_page_size = 1000

    # Client can control the page using this query parameter.
    #page_query_param = 'page'
    #page_query_param = 'draw'

    # copied form
    #.venv\Lib\site-packages\rest_framework\pagination.py
    #
    # on upgraded djano rest framework, can override get_page_number only
    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        # page_number = request.query_params.get(self.page_query_param, 1)
        page_number = self.get_page_number(request, paginator) #changed on new django
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        #except InvalidPage as exc:
        except Exception as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message='six.text_type(exc)'
            )
            raise exc
            #raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    # on new django can override this only
    def get_page_number(self, request, paginator):
    	#datatable sends start and length
        page_size = request.query_params.get('length', 1)
        start = request.query_params.get('start', 0)
        
        page_number = int(start)/int(page_size)
        page_number += 1 # (pgno starts from 1 to n) not 0 to n-1
        # page_number= page_number if page_number else 1
        
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        print("print(page_size, start, page_number)")
        print(page_size, start, page_number)
        return page_number

    def get_paginated_response(self, data):
        #print(data)
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'recordsTotal': self.page.paginator.count,
            'recordsFiltered' : self.page.paginator.count,
           
            'data': data
        })

from rest_framework.generics import  ListAPIView
# from users.views import ( UsersDataTable )
# urlpatterns += [ re_path(r'^api/UsersDataTable/$', UsersDataTable.as_view(), name="inquiry_user"), ]
# 
# /api/UsersDataTable?id=
class VariationDataTable(generics.ListAPIView):
    serializer_class = VariationDataTableSerializer
    pagination_class = DataTablePagination
    filterset_class = VariationFilter

    filter_backends = [
                filters.SearchFilter, 
                filters.OrderingFilter, 
                DjangoFilterBackend
                ]
    # search_fields = ["title", "description"] // old version
    filterset_fields = ["title"]
    ordering_fields  = ["title", "id"]
    #ordering_fields = '__all__'
    # filterset_fields = ['title']
    #ordering = ['id']
    def get_queryset(self):
        print(self.request)
        return Variation.objects.all()







#purchase detail or report datatables






from rest_framework import serializers
class PurchaseDataTableSerializer(serializers.ModelSerializer):
    supplier = serializers.SerializerMethodField()
    class Meta:
        model = Purchase
        fields= '__all__'
    
    def get_supplier(self, obj):
        supplier = ''
        if obj.fk_vendor:
            supplier = obj.fk_vendor.name
        return supplier

from rest_framework import pagination
from rest_framework.response import Response
# https://github.com/encode/django-rest-framework/blob/master/rest_framework/pagination.py
# see fields to overide from PageNumberPagination
class DataTablePagination(pagination.PageNumberPagination):
    page_size = 100
    #page_size_query_param = 'page_size'
    page_size_query_param = 'length'
    max_page_size = 1000

    # Client can control the page using this query parameter.
    #page_query_param = 'page'
    #page_query_param = 'draw'

    # copied form
    #.venv\Lib\site-packages\rest_framework\pagination.py
    #
    # on upgraded djano rest framework, can override get_page_number only
    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        # page_number = request.query_params.get(self.page_query_param, 1)
        page_number = self.get_page_number(request, paginator) #changed on new django
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        #except InvalidPage as exc:
        except Exception as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message='six.text_type(exc)'
            )
            raise exc
            #raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    # on new django can override this only
    def get_page_number(self, request, paginator):
    	#datatable sends start and length
        page_size = request.query_params.get('length', 1)
        start = request.query_params.get('start', 0)
        
        page_number = int(start)/int(page_size)
        page_number += 1 # (pgno starts from 1 to n) not 0 to n-1
        # page_number= page_number if page_number else 1
        
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        print("print(page_size, start, page_number)")
        print(page_size, start, page_number)
        return page_number

    def get_paginated_response(self, data):
        #print(data)
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'recordsTotal': self.page.paginator.count,
            'recordsFiltered' : self.page.paginator.count,
            'totalSales' : '',
            'data': data
        })

from rest_framework.generics import  ListAPIView
# from users.views import ( UsersDataTable )
# urlpatterns += [ re_path(r'^api/UsersDataTable/$', UsersDataTable.as_view(), name="inquiry_user"), ]
# 
# /api/UsersDataTable?id=
class PurchaseDataTable(generics.ListAPIView):
    serializer_class = PurchaseDataTableSerializer
    pagination_class = DataTablePagination
    filterset_class = PurchaseFilter

    filter_backends = [
                filters.SearchFilter, 
                filters.OrderingFilter, 
                DjangoFilterBackend
                ]
    # search_fields = ["title", "description"] // old version
    filterset_fields = ["title"]
    ordering_fields  = ["title", "id"]
    #ordering_fields = '__all__'
    # filterset_fields = ['title']
    #ordering = ['id']
    def get_queryset(self):
        print(self.request)
        return Purchase.objects.all()



class AdjustmentDataTableSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    batchno = serializers.SerializerMethodField()
    class Meta:
        model = Adjustment
        fields= '__all__'
    
    def get_product(self, obj):
        product = ""
        var_batch_obj = obj.fk_variation_batch
        if var_batch_obj:
            var_obj = var_batch_obj.fk_variation
            if var_obj:
                product = var_obj.title
        return product

    def get_batchno(self, obj):
        batchno = ""
        var_batch_obj = obj.fk_variation_batch
        if var_batch_obj:
           batchno = var_batch_obj.batchno
           
        return batchno            

class AdjustmentDataTable(generics.ListAPIView):
    serializer_class = AdjustmentDataTableSerializer
    pagination_class = DataTablePagination
    filterset_class = AdjustmentFilter

    filter_backends = [
                filters.SearchFilter, 
                filters.OrderingFilter, 
                DjangoFilterBackend
                ]
    # search_fields = ["title", "description"] // old version
    filterset_fields = ["fk_variation__title"]
    ordering_fields  = ["id"]
    #ordering_fields = '__all__'
    # filterset_fields = ['title']
    #ordering = ['id']
    def get_queryset(self):
        print(self.request)
        return Adjustment.objects.all().order_by('-id')



class SalesDataTableSerializer(serializers.ModelSerializer): #order ko data-table Cart
    payment_mode = serializers.SerializerMethodField()
    visit_id = serializers.SerializerMethodField()
    bill_counter = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields= '__all__'
    
    def get_payment_mode(self, obj):
        payment_mode = "n/a"
        if obj.fk_payment_method:
            payment_mode = obj.fk_payment_method.title

        return payment_mode

    def get_visit_id(self, obj):
        visit_id = "n/a"
        if obj.fk_visit:
            visit_id = obj.fk_visit.visit_id
        return visit_id

    def get_bill_counter(self, obj):
        bill_counter = "n/a"
        if obj.fk_counter:
            bill_counter = obj.fk_counter.name
        return bill_counter        

    def get_total(self, obj):
        total = obj.total        
        if obj.transaction_total > 0:
           total = obj.total - obj.transaction_total                      
        return total

class SalesDataTable(generics.ListAPIView):
    serializer_class = SalesDataTableSerializer
    pagination_class = DataTablePagination
    filterset_class = SalesFilter

    filter_backends = [
                filters.SearchFilter, 
                filters.OrderingFilter, 
                DjangoFilterBackend
                ]
    # search_fields = ["title", "description"] // old version
    filterset_fields = ["fk_variation__title"]
    ordering_fields  = ["id"]
    #ordering_fields = '__all__'
    # filterset_fields = ['title']
    #ordering = ['id']
    def get_queryset(self):
        print(self.request)
        return Cart.objects.all().order_by('-id')