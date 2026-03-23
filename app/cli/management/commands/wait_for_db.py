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

        for _ in range(0, 5):
            try:
                connection.ensure_connection()
                self.stdout.write(
                    self.style.SUCCESS(f"Database is active.")
                )
                return
            except OperationalError:
                self.stdout.write(f"Waiting for Database....")
                time.sleep(2)

        self.stdout.write(
                    self.style.WARNING(f"Database is not Available")
                )


