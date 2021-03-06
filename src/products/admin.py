from django.contrib import admin

# Register your models here.


from .models import Product, Variation, ProductImage,\
	 Category, ProductFeatured, Company, Brand, GenericName, ProductUnit, ProductCommon, VariationBatch,VariationBatchPrice

class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 0
	max_num = 10

class VariationInline(admin.TabularInline):
	model = Variation
	extra = 0
	max_num = 10


class ProductAdmin(admin.ModelAdmin):
	# list_display = ['title', 'price']
	inlines = [
		ProductImageInline,
		VariationInline,
	]
	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)



#admin.site.register(Variation)

admin.site.register(ProductImage)

admin.site.register(Category)

admin.site.register(ProductFeatured)

admin.site.register(Company)

admin.site.register(Brand)

admin.site.register(GenericName)

admin.site.register(ProductUnit)

admin.site.register(ProductCommon)
admin.site.register(VariationBatch)
admin.site.register(VariationBatchPrice)



