from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Account, CustomerRegisterSurvey, CallLog

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('mobile', 'password', 'email', 'username', 'firstname','lastname', 'nick_name')
		extra_kwargs = {'password': {'write_only': True}, }


	def create(self, validated_data):
		password = validated_data.pop('password', None)
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
			instance.save()
		return instance

	def update(self, instance, validated_data):
		for attr, value in validated_data.items():
			if attr == 'password':
				instance.set_password(value)
			else:
				setattr(instance, attr, value)
		instance.save()
		return instance
		# def create(self, validated_data):

class UpdateUserSerializer(serializers.ModelSerializer):
	class Meta:
		model =User
		fields = ['password']

	
	def update(self, instance, validated_data):
		
		for attr, value in validated_data.items():
			if attr == 'password':
				instance.set_password(value)
			else:
				setattr(instance, attr, value)

		instance.save()
		return instance


class SurveyRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerRegisterSurvey
		fields = ['firstname', 'lastname', 'email']


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['firstname','lastname']
		


			# password = serializers.CharField(write_only=True)

			# def create(self, validated_data):
			# 	user = User.objects.create_user(
			# 	username=validated_data['username'],
			# 	password=validated_data['password'],
			# 	mobile=validated_data['mobile'],
			# 	email=validated_data['email'],
			# 	)
			# 	return user

			# password = validated_data.pop('password')
			# user = super().create(validated_data)
			# user.set_password(make_password(validated_data['password']))
			# # user = Account.objects.create(**validated_data)
			# user.save()
			# return user
			# user = User(**validated_data)
			# # Hash the user's password.
			# user.set_password(validated_data['password'])
			# user.save()
			# return user
from store.models import StoreAccount
from products.serializers import UserVariationQuantityHistorySerializer
from products.models import UserVariationQuantityHistory
from carts.models import Comment
from carts.serializers import CommentSerializer
from store.service import getUserStoreService
from store.models import StoreUser
from users.serializers import DeliveryUserSerializer

class UserSerializer(serializers.ModelSerializer):
	credit = serializers.SerializerMethodField()
	jardetails = serializers.SerializerMethodField()
	# delivery_boys = serializers.SerializerMethodField()
	comments = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = ('firstname', 'lastname','mobile', 'nick_name', 'credit', 'jardetails',"comments")

	def get_credit(self, obj):
		user = StoreAccount.objects.filter(fk_user=obj).first()
		if user:
			return user.credit
		return ''
	def get_jardetails(self, obj):
		jardetails = UserVariationQuantityHistorySerializer(UserVariationQuantityHistory.objects.filter(user=obj), many=True)
		return jardetails.data
	
	def get_comments(self, obj):
		comments = CommentSerializer(Comment.objects.filter(user=obj), many=True)
		return comments.data
	
from products.models import Variation
from products.serializers import ProductVariationListSerializer		
from datetime import datetime
class CallLogSerializer(serializers.ModelSerializer):
	info_dhikka = serializers.SerializerMethodField()
	class Meta:
		model = CallLog
		fields = '__all__'
	def get_info_dhikka(self, obj):
		variation_id = CallLog.objects.filter(number=obj.number).first().fk_variation_id
		# print(variation_id)
		time = f'{obj.timestamp:%Y-%m-%d %H:%M}'
		data = {}
		if variation_id:
			variation = Variation.objects.filter(pk=variation_id).first()
			# serializer = 
			data = {
				"latitude" : obj.order_latitude,
				"longitude" : obj.order_longitude,
				"time" : time,
				"product" : variation.title#ProductVariationListSerializer(variation, many=True).data
			}
		return data
		
		# return 'Please, be very clear on your commit messages and pull requests, empty pull request messages may be rejected without reason.'

