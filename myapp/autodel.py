from django.core.management.base import BaseCommand, CommandError
from models import tempUserVerification
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Delete objects older than 10 days'
    now = datetime.now()
    year = '{:02d}'.format(now.year)
    month = '{:02d}'.format(now.month)
    day = '{:02d}'.format(now.day)
    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)
    # second = '{:02d}'.format(now.second)
    day_month_year = '{}-{}-{}'.format(year, month, day)
    hour_minute_second = '{}:{}:00'.format(hour, minute)

    def handle(self, *args, **options):
        tempUserVerification.objects.filter(updated_date__lte=datetime.now()-timedelta(minutes=1)).delete()
        self.stdout.write('Deleted objects older than 10 days')