"""
    Command to Sure that db is active before web_app starts
"""
from django.core.management import BaseCommand
from django.db import connection
from django.db.utils import OperationalError
import time

class Command(BaseCommand):
    help = "Waits for database to be active"

    def handle(self, *args, **options):

        while True:
            try:
                connection.ensure_connection()
                self.stdout.write(
                    self.style.SUCCESS(f"Database is active.")
                )
                return
            except OperationalError:
                self.stdout.write(f"2 second, Waiting for Database....")
                time.sleep(2)


