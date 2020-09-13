from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import products in BookTime'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=open)

    def handle(self, *args, **options):
        self.stdout.write('Importing products')
