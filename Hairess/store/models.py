from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True, blank=True)
    customer_name = models.CharField(max_length = 500, null=True, blank=True)
    device_id = models.CharField(max_length = 500, null=True, blank=True)
    
    
    def __str__(self):
        if self.user:
            return str(self.customer_name)
        else:
            return 'Guest user ' + self.device_id
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField()
    inches = models.CharField(max_length=10,null=True)
    image = models.ImageField(null=True,blank=True)
    description = models.CharField(max_length=600,null=True,blank=True)
    
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id =  models.CharField(max_length=200, null=True)
    shippingprice = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.product)
    
    @property
    def get_cart_subtotal(self):
        if self.customer.device_id:
            orderitems  = self.orderitem_set.filter(customer = Customer.objects.get(device_id = self.customer.device_id))
            total = sum([item.get_total for item in orderitems])
            print(total)
            return total
        else:
            orderitems  = self.orderitem_set.filter(customer = Customer.objects.get(customer_name = self.customer.customer_name))
            total = sum([item.get_total for item in orderitems])
            print(total)
            return total
    
    @property
    def get_cart_items(self):
        if self.customer.device_id:
            orderitems  = self.orderitem_set.filter(customer = Customer.objects.get(device_id = self.customer.device_id))
            total = sum([item.quantity for item in orderitems])
            return total
        else:
            orderitems  = self.orderitem_set.filter(customer = Customer.objects.get(customer_name = self.customer.customer_name))
            total = sum([item.quantity for item in orderitems])
            return total

    
    @property
    def get_cart_total(self):
        if self.customer.device_id:
            orderitems  = self.orderitem_set.filter(customer = Customer.objects.get(device_id = self.customer.device_id))
            total = sum([item.get_total + shippingprice for item in orderitems])
            print(total)
            return total
        else:
            orderitems  = self.orderitem_set.filter(customer = Customer.objects.get(customer_name = self.customer.customer_name))
            total = sum([item.get_total + shippingprice for item in orderitems])
            print(total)
            return total
    
    
class OrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    #id = models.IntegerField(primary_key=True)

    def __str__(self):
        if self.customer.device_id:
            return 'Guest user ' + self.customer.device_id
        else:
            return str(self.customer)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


    
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    
class Hair_bundles(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.IntegerField()
    inches = models.CharField(max_length=10,null=True)
    image = models.ImageField(null=True,blank=True)
    description = models.CharField(max_length=600,null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url