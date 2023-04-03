from django.core.management import BaseCommand
from django_redis import get_redis_connection
from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        con = get_redis_connection()
        ambassadors = User.objects.filter(is_ambassador=True)

        for ambassador in ambassadors:
            con.zadd('rankings', {ambassador.name: float(ambassador.revenue)})

        # sorted_numbers = con.zrevrange('sorted_numbers', 0, -1)
        #
        # print(sorted_numbers)

# from django_redis import get_redis_connection

# # get a Redis connection
# redis_conn = get_redis_connection()
#
# # create a list of numbers
# numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
#
# # add the numbers to a Redis sorted set with their values as the score in reverse order
# for i, number in enumerate(reversed(numbers)):
#     redis_conn.zadd('sorted_numbers', {number: i})
#
# # retrieve the sorted elements from the sorted set in descending order
# sorted_numbers = redis_conn.zrevrange('sorted_numbers', 0, -1)
#
# print(sorted_numbers)  # [b'9', b'6', b'5', b'4', b'3', b'2', b'1']