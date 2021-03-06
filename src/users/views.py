from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from django.contrib.auth.models import User
from .serializers import InqueryUserSerializer, InquiryUsersListForPharmacistSerializer, DeliveryUserSerializer
from rest_framework import generics
from .models import UserType
from inquiry.models import Message
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# from store.service import getUserStoreService
from store.models import Store, StoreUser
User = get_user_model()


# Create your views here.
class UserInquiryList1(generics.ListAPIView):
	serializer_class = InqueryUserSerializer

	def get_queryset(self):
		pharmasicts = UserType.objects.filter(user_type=1)
		return pharmasicts

class UserInquiryList(generics.ListAPIView):
	serializer_class = InquiryUsersListForPharmacistSerializer

	def get_queryset(self):
		user =  self.request.user
		user_type = UserType.objects.filter(user_id=user.id).first()

		if user_type is not None:
			if user_type.user_type_id==1:
				users = User.objects.raw('select DISTINCT sender_id as id FROM inquiry_message WHERE receiver_id=%s', [user.id])
				return list(users)
		pharmasicts = User.objects.filter(id__in=UserType.objects.filter(user_type_id=1).values('user_id'))
		all_instance = [i.id for i in pharmasicts]

		# print(all_instance)
		# print(pharmasicts.__dict__)
		# print('jpt')
		return pharmasicts

		# users = User.objects.raw('select DISTINCT sender_id as id FROM inquiry_message WHERE receiver_id=%s', [user.id])
		# print(users)
		# print('jpt')
		# all_instance = [i for i in users]
		# print(all_instance)
		return list(users)


class UserInquiryForPharmacist1(generics.ListAPIView):
	serializer_class = InquiryUsersListForPharmacistSerializer

	def get_queryset(self):
		user =  self.request.user
		users = Message.objects.filter(receiver_id=user.id)[:1]
		return users


class UserInquiryForPharmacist(generics.ListAPIView):
	serializer_class = InquiryUsersListForPharmacistSerializer

	def get_queryset(self):
		user =  self.request.user
		users = User.objects.raw('select DISTINCT sender_id as id FROM inquiry_message WHERE receiver_id=%s', [user.id])
		return list(users)

class DeliveryUsersByStore(generics.ListAPIView):
	serializer_class = DeliveryUserSerializer
	def get_queryset(self):
		store  = getUserStoreService(self.request.user.id)
		if store:
			store_users = StoreUser.objects.filter(fk_store_id=store.id).filter(fk_store_usertypes_id=2).values('fk_user_id')
			delivery_boys = User.objects.filter(pk__in=store_users)
			return delivery_boys