from django.core.management import BaseCommand
from core.models import Order, OrderItems
from faker import Faker
from random import randrange, random
import random


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        for _ in range(3):
            order = Order.objects.create(
                user_id=66,
                code='code',
                ambassador_email="edem@fedelity.io",
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                complete=True
            )

            for _ in range(randrange(1, 5)):
                price = round(random.uniform(33.33, 66.66))
                quantity = random.randint(0, 9)

                OrderItems.objects.create(
                    order_id=order.id,
                    product_title=faker.name(),
                    price=price,
                    quantity=quantity,
                    admin_revenue=.9 * price * quantity,
                    ambassador_revenue=0.1 * price * quantity
                )


