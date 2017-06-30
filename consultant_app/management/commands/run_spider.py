from django.core.management.base import BaseCommand, CommandError
from scrapy.commands import crawl

# from scrapy_for_events.spiders import goeventz,eventshigh_spider
# import scrapy

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print("managememmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")
            # try:
            #     spider = 'scrapy crawl goeventz'
            # except spider.DoesNotExist:
            #     raise CommandError('Spider "%s" does not exist' )
            #
            #
            #
            # self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))