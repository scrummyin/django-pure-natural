from django.core.serializers.json import Serializer as BaseSerializer, Deserializer as BaseDeserializer
from django.utils.encoding import smart_unicode

class Serializer(BaseSerializer):
    use_natural_keys = True
    def end_object(self, obj):
        self.objects.append({
            "model": smart_unicode(obj._meta),
            "natural_key": obj.natural_key(),
            "fields": self._current
        })
        self._current = None
