# -*- coding: utf-8 -*-

from decimal import Decimal as D
from datetime import datetime as d

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ImproperlyConfigured
from openexchangerates import OpenExchangeRatesClient

from ...models import Currency as C

APP_ID = getattr(settings, "OPENEXCHANGERATES_APP_ID", None)
if APP_ID is None:
    raise ImproperlyConfigured(
        "You need to set the 'OPENEXCHANGERATES_APP_ID' setting to your openexchangerates.org api key")


class Command(BaseCommand):
    help = "Update the currencies against the current exchange rates"

    def handle(self, *args, **options):
        self.verbose = int(options.get('verbosity', 0))
        self.options = options

        client = OpenExchangeRatesClient(APP_ID)
        if self.verbose >= 1:
            self.stdout.write("Querying database at %s" % (client.ENDPOINT_CURRENCIES))

        try:
            code = C._default_manager.get(is_base=True).code
        except C.DoesNotExist:
            code = 'USD'  # fallback to default

        l = client.latest(base=code)

        if self.verbose >= 1 and "timestamp" in l:
            self.stdout.write("Rates last updated on %s" % (
                d.fromtimestamp(l["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")))

        if "base" in l:
            if self.verbose >= 1:
                self.stdout.write("All currencies based against %s" % (l["base"]))

            if not C._default_manager.filter(code=l["base"]):
                self.stderr.write(
                    "Base currency %r does not exist! Rates will be erroneous without it." % l["base"])
            else:
                base = C._default_manager.get(code=l["base"])
                base.is_base = True
                base.last_updated = d.fromtimestamp(l["timestamp"])
                base.save()

        exception_currencies = {
            # eg: NMP will be mapped to MXN
            'NMP': 'MXN',
            'BYR': 'BYN',
            'RMB': 'CNY'
        }

        for c in C._default_manager.all():
            if c.code in exception_currencies:
                mapped_currency = exception_currencies[c.code]
                factor = D(l["rates"][mapped_currency]).quantize(D(".000001"))

            elif c.code not in l["rates"] and c.code not in exception_currencies:
                self.stderr.write("Could not find rates for %s (%s)" % (c, c.code))
                continue
            else:
              factor = D(l["rates"][c.code]).quantize(D(".000001"))

            if self.verbose >= 1:
                self.stdout.write("Updating %s rate to %f" % (c, factor))

            C._default_manager.filter(pk=c.pk).update(factor=factor, last_updated=d.fromtimestamp(l["timestamp"]))
