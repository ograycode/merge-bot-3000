from django.core.management.base import BaseCommand, CommandError
from pull_requests.models import PullRequest

class Command(BaseCommand):
    help = 'Obtains all new pull requests and stores them in the database'

    def handle(self, *args, **options):
        self.stdout.write('Starting...')
        PullRequest.save_new_merge_requests()
        number_of_new_requests = PullRequest.objects.filter(already_merged = False).count()
        self.stdout.write('Stopped with ' + str(number_of_new_requests) + ' new requests')