from django.core.serializers.json import Serializer as BaseSerializer, Deserializer as BaseDeserializer
from django.utils.encoding import smart_unicode


class Serializer(BaseSerializer):
    use_natural_keys = True

    def end_object(self, obj):
        if BaseSerializer.get_dump_object:
            return super(Serializer, self).end_object(obj)
        else:
            self.objects.append({
                "model": smart_unicode(obj._meta),
                "natural_key": obj.natural_key(),
                "fields": self._current
            })
            self._current = None

    def get_dump_object(self, obj):
        original = super(Serializer, self).get_dump_object(obj)
        del original['pk']
        original["natural_key"] = obj.natural_key(),
        return original
