from django.core.serializers.json import Serializer as _JSONSerializer
from django.utils.encoding import smart_text


class Serializer(_JSONSerializer):
    def serialize(self, queryset, **options):
        self._alias = options.pop('alias', None)
        return super(Serializer, self).serialize(queryset, **options)

    def get_dump_object(self, obj):
        dump_object = self._current or {}
        dump_object.update({'id': smart_text(obj._get_pk_val(), strings_only=True)})
        if self._alias:
            for key, value in self._alias.items():
                if dump_object.get(key, None):
                    dump_object[value] = dump_object[key]
                    dump_object.pop(key)
        return dump_object

