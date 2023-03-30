# from constants import
# from django.core.management import BaseCommand
# from django.db import connections
# from django.db.utils import OperationalError
# import time
#
#
# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         self.stdout.write(f"{WAITING_FOR_DATABASE} ...")
#         conn = None
#         while not conn:
#             try:
#                 conn = connections['default']
#             except OperationalError:
#                 self.stdout.write(f"{DATABASE_NOT_AVAILABLE}, waiting for a second")
#                 time.sleep(1)
#         self.stdout.write(f"{DATABASE_CONNECTED} ...")

# from constants import DATABASE_NOT_AVAILABLE, DATABASE_CONNECTED, WAITING_FOR_DATABASE
from django.core.management import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Database is not available ")
        conn = None
        while not conn:
            try:
                conn = connections['default']
            except OperationalError:
                self.stdout.write("Waiting for the database")
                time.sleep(1)
        self.stdout.write("Database connected")
