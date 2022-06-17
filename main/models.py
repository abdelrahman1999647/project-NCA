from random import choices
from unicodedata import name
from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from matplotlib import image
# Banner
class Banner(models.Model):
    img=models.ImageField(upload_to="banner_imgs/",verbose_name = "صورة")
    alt_text=models.CharField(max_length=300,verbose_name = "نص")

    class Meta:
        verbose_name_plural='1. اعلان'

    def image_tag(self):
        return mark_safe('<img src="%s" width="100" />' % (self.img.url))

    def __str__(self):
        return self.alt_text

# Category
class Category(models.Model):
    title=models.CharField(max_length=100,verbose_name = "اسم الفئة")
    image=models.ImageField(upload_to="cat_imgs/",verbose_name = "صورة الفئة" ,null=True, blank=True)

    class Meta:
        verbose_name_plural='2. الفئات'

    # def image_tag(self):
    #     return mark_safe('<img src="%s" width="50" height="50" />' % ())

    def __str__(self):
        return self.title

# Brand
class Brand(models.Model):
    title=models.CharField(max_length=100,verbose_name = "اسم الماركة")
    image=models.ImageField(upload_to="brand_imgs/",verbose_name = "صورة الماركة", null=True, blank=True)

    class Meta:
        verbose_name_plural='3. الماركات'

    def __str__(self):
        return self.title

# Color
class Color(models.Model):
    title=models.CharField(max_length=100,verbose_name = "اللون")
    color_code=models.CharField(max_length=100,verbose_name = "رمز اللون")

    class Meta:
        verbose_name_plural='4. الالوان'

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
        return self.title

# Size
class Size(models.Model):
    title=models.CharField(max_length=100,verbose_name = "المساحة التخزينية")

    class Meta:
        verbose_name_plural='5. المساحة التخزينية'

    def __str__(self):
        return self.title


# Product Model
class Product(models.Model):
    title=models.CharField(max_length=200,verbose_name = "اسم المنتج")
    quantity = models.PositiveIntegerField(null=True, blank=True,verbose_name = "العدد")
    slug=models.CharField(max_length=400)
    specs=models.CharField(max_length=200,verbose_name = "المواصفات",null=True, blank=True)
    specs2=models.CharField(max_length=200,verbose_name = "2المواصفات",null=True, blank=True)
    specs3=models.CharField(max_length=200,verbose_name = "3المواصفات",null=True, blank=True)
    specs4=models.CharField(max_length=200,verbose_name = "4المواصفات",null=True, blank=True)
    specs5=models.CharField(max_length=200,verbose_name = "5المواصفات",null=True, blank=True)
    specs6=models.CharField(max_length=200,verbose_name = "6المواصفات",null=True, blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,verbose_name = "الفئة" ,null=True, blank=True)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,verbose_name = "الماركة" ,null=True, blank=True)
    status=models.BooleanField(default=True,verbose_name = "الحالة")
    is_featured=models.BooleanField(default=False, verbose_name="افضل تمييز")

    class Meta:
        verbose_name_plural='6. المنتج'

    def __str__(self):
        return self.title

# Product Attribute
class ProductAttribute(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name = "المنتج")
    color=models.ForeignKey(Color,on_delete=models.CASCADE,verbose_name = "اللون" ,null=True, blank=True)
    size=models.ForeignKey(Size,on_delete=models.CASCADE,verbose_name = "المساحة التخزينية" ,null=True, blank=True)
    price=models.PositiveIntegerField(default=0,verbose_name = "السعر")
    image=models.ImageField(upload_to="product_imgs/",null=True,verbose_name = "الصورة")

    class Meta:
        verbose_name_plural='7. سمات المنتج'

    def __str__(self):
        return self.product.title

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

# Order
status_choice=(
        ('في الانتظار','في الانتظار'),
        ('شحنها','شحنها'),
        ('تم التوصيل','تم التوصيل'),
    )
class CartOrder(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name = "العميل")
    total_amt=models.FloatField(verbose_name = "اجمالي السعر")
    paid_status=models.BooleanField(default=False,verbose_name = "تم الدفع")
    order_dt=models.DateTimeField(auto_now_add=True,verbose_name = "التاريخ")
    order_status=models.CharField(choices=status_choice,default='في الانتظار',max_length=150, verbose_name="حالة الاوردر")
    name = models.TextField( verbose_name="اسم العميل")
    number = models.IntegerField( verbose_name="رقم الهاتف")
    address = models.TextField(null=True, verbose_name="العنوان")
    pay = models.CharField(max_length=100, blank=True , null=True , verbose_name="الدفع")

    class Meta:
        verbose_name_plural='8. الاوردر'

# OrderItems
class CartOrderItems(models.Model):
    order=models.ForeignKey(CartOrder,on_delete=models.CASCADE,verbose_name = "الاوردر")
    invoice_no=models.CharField(max_length=150,verbose_name = "رقم الفاتورة")
    item=models.CharField(max_length=150,verbose_name = "اسم المنتج")
    image=models.CharField(max_length=200,verbose_name = "صورة المنتج")
    qty=models.IntegerField(verbose_name = "العدد")
    price=models.FloatField(verbose_name = "السعر")
    total=models.FloatField(verbose_name = "اجمالي السعر")
    
    

    class Meta:
        verbose_name_plural='9. قائمة الطلبات'

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image))

# Product Review
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name = "العميل")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name = "المنتج")
    review_text=models.TextField(verbose_name = "تعليق")
    review_rating=models.CharField(choices=RATING,max_length=150,verbose_name = "التقييم")

    class Meta:
        verbose_name_plural='تقييم المنتج'

    def get_review_rating(self):
        return self.review_rating

# WishList
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name = "العميل")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name = "المنتج")

    class Meta:
        verbose_name_plural='المفضلة'



class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    number = models.IntegerField()
    message = models.TextField(blank=True , null=True)

    class Meta:
        verbose_name_plural='تواصل معنا'













