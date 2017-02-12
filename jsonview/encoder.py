try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.db.models.base import ModelBase
from django.utils.encoding import force_text, is_protected_type


def dumps(content, **json_opts):
    """
    Replaces json.dumps with our own custom encoder
    """

    opts = {
        'ensure_ascii': False,
        'cls': LazyJSONEncoder,
    }

    opts.update(json_opts)

    return json.dumps(content, **opts)


class LazyJSONEncoder(json.JSONEncoder):
    """
    A JSONEncoder subclass that handles querysets and model objects.
    If the model object has a "serialize" method that returns a dictionary,
    then this method is used, else, it attempts to serialize fields.
    """

    def __init__(self, **kwargs):
        self.selected_fields = kwargs.pop('fields', None)
        self.use_natural_foreign_keys = kwargs.pop('use_natural_foreign_keys', False)
        self.many_to_many_serialize = kwargs.pop('mtm', True)
        self.many_to_one_serialize = kwargs.pop('mto', True)
        self.alias_filed_name = kwargs.pop('alias', None)
        self.show_id = kwargs.pop('show_id', True)
        super(LazyJSONEncoder, self).__init__(**kwargs)

    def default(self, obj):
        # This handles querysets and other iterable types
        try:
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)

        # This handles Models
        if isinstance(obj.__class__, ModelBase):
            if hasattr(obj, 'serialize') and \
                    callable(getattr(obj, 'serialize')):
                return obj.serialize()
            return self.serialize_model(obj)

        # Other Python Types:
        try:
            return force_text(obj)
        except Exception:
            pass

        # Last resort:
        return super(LazyJSONEncoder, self).default(obj)

    def handle_field(self, obj, field):
        value = field.value_from_object(obj)
        # Protected types (i.e., primitives like None, numbers, dates,
        # and Decimals) are passed through as is. All other values are
        # converted to string first.
        if is_protected_type(value):
            return value
        else:
            return field.value_to_string(obj)

    def handle_fk_field(self, obj, field):
        if self.use_natural_foreign_keys and hasattr(field.remote_field.model, 'natural_key'):
            related = getattr(obj, field.name)
            if related:
                value = related.natural_key()
            else:
                value = None
        else:
            value = getattr(obj, field.get_attname())
            if not is_protected_type(value):
                value = field.value_to_string(obj)
            else:
                value = None

        if not value:
            field_obj = getattr(obj, field.name)
            if self.many_to_one_serialize:
                return field_obj
            elif field_obj:

                return getattr(obj, field.name)._get_pk_val()
        return value

    def handle_m2m_field(self, obj, field):
        if self.many_to_many_serialize:
            return getattr(obj, field.name).all()
        if field.remote_field.through._meta.auto_created:
            if self.use_natural_foreign_keys and hasattr(field.remote_field.model, 'natural_key'):
                def m2m_value(value):
                    return value.natural_key()
            else:
                def m2m_value(value):
                    return force_text(value._get_pk_val(), strings_only=True)
            return [
                m2m_value(related) for related in getattr(obj, field.name).iterator()
                ]

    def serialize_model(self, obj):
        ret = {}
        concrete_model = obj._meta.concrete_model
        show_id = self.show_id
        for field in concrete_model._meta.local_concrete_fields:

            name = self._use_name(field)
            if field.serialize:
                if field.remote_field is None:
                    if self.selected_fields is None or field.attname in self.selected_fields:
                        ret[name] = self.handle_field(obj, field)
                else:
                    if self.selected_fields is None or field.attname[:-3] in self.selected_fields:
                        ret[name] = self.handle_fk_field(obj, field)
            if show_id:
                if field.auto_created:
                    ret[name] = obj.pk

        for field in concrete_model._meta.many_to_many:
            name = self._use_name(field)
            if field.serialize:
                if self.selected_fields is None or field.attname in self.selected_fields:
                    ret[name] = self.handle_m2m_field(obj, field)
        return ret

    def _use_name(self, field):
        if self.alias_filed_name:
            name = self.alias_filed_name.get(field.name) or field.name
        else:
            name = field.name
        return name
