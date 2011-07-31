from django.core.management.base import BaseCommand, CommandError
from secdef.keyserver.models import Key
from datetime import datetime
class Command(BaseCommand):
    args = ''
    help = 'Determines if there are any expired keys. If so, it deletes them.'

    def handle(self, *args, **options):
        keys = Key.objects.filter(expires__lte=datetime.utcnow())
        self.stdout.write('Number of keys: %d\n' % (len(keys)))
        for key in keys:
            self.stdout.write('Deleting Key: %s\nMin: %d\nExpires: %s\n' % (key.key, key.min_to_expire, key.expires))
            key.delete()

