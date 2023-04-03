import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email: string, password: str = None):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")

        user: User = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_superuser = False
        user.is_ambassador = False
        user.is_staff = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email: string, password: str = None):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")

        user: User = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_ambassador = False
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_ambassador = models.BooleanField(default=True)
    username = None

    # overriding the username field which means we will log using the
    # email and password instead of the username and password
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def revenue(self):
        orders = Order.objects.filter(user_id=self.pk, complete=True)
        return sum(order.ambassador_revenue for order in orders)


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, null=True)
    image = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Link(models.Model):
    code = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)


class Order(models.Model):
    transaction_id = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=255)
    ambassador_email = models.CharField(max_length=255)
    # infor about customer
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    zip = models.CharField(max_length=255, null=True)
    complete = models.BooleanField(default=False)
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def ambassador_revenue(self):
        order_items = OrderItems.objects.filter(order_id=self.pk)
        return sum(item.ambassador_revenue for item in order_items)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product_title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    admin_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    ambassador_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.TimeField(auto_now_add=True)
    updated_at = models.TimeField(auto_now=True)
