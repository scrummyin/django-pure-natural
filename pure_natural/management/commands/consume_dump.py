from django.utils import six
from django.conf import settings
from django.utils.encoding import smart_text
from django.db import models
from django.db.models.loading import get_model
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import ManyToManyField
import os
import json


class Command(BaseCommand):
    help = 'Loads data from a pure_natural dump file'
    args = "dump [dump...]"

    def handle(self, *dumps, **options):
        dump_paths = [os.path.relpath(path) for path in dumps]
        self.verbosity = int(options.get('verbosity'))

        if not len(dump_paths):
            raise CommandError(
                "No dump specified. Please provide the path of at least one dump in the command line."
            )

        for dump_path in dump_paths:
            data = open(dump_path).read()
            json_data = json.loads(data)
            for item in json_data:
                app_name, model_name = item['model'].split('.')
                model = get_model(app_name, model_name)
                self.print_out(item)
                try:
                    instance = model.objects.get_by_natural_key(*item['natural_key'])
                except ObjectDoesNotExist as ex:
                    instance = model()
                model_fields = instance._meta.get_all_field_names()
                manager_fields = []
                fk_fields = []
                for (field_name, field_value) in six.iteritems(item["fields"]):

                    if field_name not in model_fields:
                        # skip fields no longer on model
                        continue

                    if isinstance(field_value, str):
                        field_value = smart_text(field_value, options.get("encoding", settings.DEFAULT_CHARSET), strings_only=True)

                    field = model._meta.get_field(field_name)
                    if not isinstance(field, ManyToManyField):
                        # Handle FK fields
                        field_instance = model._meta.get_field_by_name(field_name)[0]
                        if field_instance.rel:
                            related_model_manager = field_instance.rel.to.objects
                            if field_value:
                                field_value = related_model_manager.get_by_natural_key(*field_value)

                        setattr(instance, field_name, field_value)
                    else:
                        manager_fields.append((field_name, field_value))

                    # Handle M2M relations
                instance.save()
                for field_name, field_value in manager_fields:
                    field = getattr(instance, field_name)
                    field.clear()
                    for nat_key in field_value:
                        field.add(field.model.objects.get_by_natural_key(*nat_key))


    def print_out(self, *args):
        if self.verbosity > 1:
            print(args)
