from django.core.management.base import BaseCommand, CommandError
from pull_requests.models import PullRequest

class Command(BaseCommand):
    help = 'Merges new requests waiting in the database'

    def handle(self, *args, **options):
        self.stdout.write('Starting...')
        PullRequest.merge_pull_requests()
        self.stdout.write('Stopped.')