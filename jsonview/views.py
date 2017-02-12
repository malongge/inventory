"""
Generic View classes for JSON in  Django
"""

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseNotAllowed, HttpResponse
from django.utils.six import iteritems
from django.views.generic import View
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import BaseFormView
from django.views.generic.list import BaseListView

from .encoder import dumps

try:
    import json
except ImportError:
    from django.utils import simplejson as json


class JSONResponse(HttpResponse):
    def __init__(self, content, json_opts=None,
                 mimetype="application/json",
                 encoding="utf-8", *args, **kwargs):
        json_opts = json_opts or {}
        serialize_opts = kwargs.pop('serialize_opts', {})
        if content:
            content = dumps(content, **json_opts, **serialize_opts)
        else:
            content = dumps([], **json_opts, **serialize_opts)

        content_type = "%s; charset=%s" % (mimetype, encoding)
        super(JSONResponse, self).__init__(content, content_type,
                                           *args, **kwargs)

        self['Cache-Control'] = 'max-age=0,no-cache,no-store'

    @property
    def json(self):
        return json.loads(self.content)


class JSONResponseMixin(object):
    mimetype = "application/json"
    format = "json"
    encoding = "utf-8"
    serialize_fields = None
    serialize_use_natural_foreign_keys = False
    serialize_mtm = False
    serialize_mto = False
    serialize_alias_filed = None

    def render_to_response(self, context, *args, **kwargs):

        opts = {
            'mimetype': self.mimetype,
            'encoding': self.encoding,
        }
        opts.update(kwargs)
        serialize_opts = {
            'fields': self.serialize_fields,
            'use_natural_foreign_keys': self.serialize_use_natural_foreign_keys,
            'mtm': self.serialize_mtm,
            'mto': self.serialize_mto,
            'alias': self.serialize_alias_filed,

        }
        opts['serialize_opts'] = serialize_opts

        return JSONResponse(context, *args, **opts)

    def remove_duplicate_obj(self, context, duplicate="object", **kwargs):
        # Check if the duplicate key is in the context
        if duplicate in context:
            # Search to ensure that this key is in fact duplicated
            for key, val in context.items():
                if key == duplicate:  # Skip the duplicate object
                    continue
                if val == context[duplicate]:
                    del context[duplicate]
                    break

        # Django 1.5 also adds the View...
        context.pop('view')
        return context


##########################################################################
## Views
##########################################################################


class JSONDataView(JSONResponseMixin, View):
    def get_context_data(self, **kwargs):
        return kwargs

    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class JSONDetailView(JSONResponseMixin, BaseDetailView):
    """
    Override get method to allow access from querystrings for AJAX calls.
    """

    def get(self, request, **kwargs):
        """
        This method does not allow multiple parameters in the query string,
        so a normal dictionary rather than a QueryDict is necessary.

        The development version has a QuerySet.dict method-- but not 1.3, so
        we have to do this manually until the new version comes out.
        """
        querydict = dict([(k, v) for k, v in iteritems(request.GET)])
        self.kwargs.update(querydict)
        kwargs.update(querydict)
        return super(JSONDetailView, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(JSONDetailView, self).get_context_data(**kwargs)
        return self.remove_duplicate_obj(context)


class JSONListView(JSONResponseMixin, BaseListView):
    def get_context_data(self, **kwargs):
        context = super(JSONListView, self).get_context_data(**kwargs)
        return self.remove_duplicate_obj(context, duplicate="object_list")
        # pass


class PaginatedJSONListView(JSONListView):
    """
    Provides some helper view methods and a default pagination for the
    ListView -- including removal of pagination data from the json and a
    json return of the total number of results and pages that will be
    returned on the submission of a get request.
    """

    paginate_by = 10
    count_query = 'count'
    count_only = False

    def get_count_query(self):
        return self.count_query

    def get_count_only(self):
        return self.count_only

    def get(self, request, *args, **kwargs):
        """
        On GET if the parameter defined by ``count_query`` is in the
        request, then set the count only parameter to True. Note that the
        method ``get_count_only`` can override or use this value as
        required -- but the interface is to set the value on the instance.
        """
        if self.get_count_query() in self.request.GET:
            self.count_only = True
        return super(PaginatedJSONListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Removes paginator objects and instead supplies the pages and the
        count data as part of the paginated framework. Leaves in the
        ``is_paginated`` boolean value.

        Also tests to see if get_count_only is True -- if so, it returns
        only the pages and the count rather than the entire context.
        """
        context = super(PaginatedJSONListView, self).get_context_data(**kwargs)

        # Replace paginatior data with JSON friendly data
        page = context.pop('page_obj')
        paginator = context.pop('paginator')
        count_only = self.get_count_only()

        if paginator:
            pages = paginator.num_pages
            count = paginator.count
            ispag = page.has_other_pages()
            perpage = paginator.per_page
            ppage = page.previous_page_number() if page.has_previous() else None
            npage = page.next_page_number() if page.has_next() else None
            cpage = page.number
        else:
            pages = 1
            count = self.get_queryset().count()  # Should be the object_list
            ispag = False
            perpage = count
            cpage = 1
            npage = None
            ppage = None

        _data = {'pages': pages,
                 'count': count,
                 'per_page': perpage,
                 'is_paginated': ispag,
                 'current': cpage,
                 'pre': ppage,
                 'next': npage}
        if count_only:
            return _data
        else:
            context.update(_data)

        return context


class SearchVieWMixin(object):
    search_text = None

    def get(self, request, **kwargs):
        querydict = dict([(k, v) for k, v in iteritems(request.GET)])
        self.kwargs.update(querydict)
        kwargs.update(querydict)
        self.search_value = kwargs.get('search_value', None)
        return super(SearchVieWMixin, self).get(request, **kwargs)

    def get_queryset(self):
        if self.search_text and self.search_value:
            self.queryset = self.model._default_manager.filter(**{self.search_text + '__icontains': self.search_value})
        return super(SearchVieWMixin, self).get_queryset()


class JSONListSearchView(SearchVieWMixin, JSONListView):
    pass


class PaginatedJSONListSearchView(SearchVieWMixin, PaginatedJSONListView):
    pass


class JSONFormView(JSONResponseMixin, BaseFormView):
    """
    An attempt to integrate a JSONView with a FormView.

    Basically, the idea is this- JSON views will not require a GET method.
    Since POST is the only concern, we need to pass the post data into
    the form, then respond with JSON data instead of Form data.

    Several Overrides are the attempt to manipulate the BaseFormView to
    respond with JSON data, rather than starting from scratch.
    """

    def get_form_class(self):
        """
        There will be issues if form_class is None, so override this
        method to check and see if we have one or not.
        """
        form_class = super(JSONFormView, self).get_form_class()
        if form_class is None:
            raise ImproperlyConfigured(
                "No form class to validate. Please set form_class on"
                " the view or override 'get_form_class()'.")
        return form_class

    def get_success_url(self):
        """
        Overridden to ensure that JSON data gets returned, rather
        than HttpResponseRedirect, which is bad.
        """
        return None

    def form_valid(self, form):
        """
        Overridden to ensure that an HttpResponseRedirect does not get
        called with a success_url -- instead render_to_response some
        JSON data. DO NOT CALL SUPER!

        @note: We return a JSON flag - { success: true }. Because this
        is a common paradigm in Ben programming. However, it seems that
        the flag should be { valid: true }. Discuss amongst yourselves.
        """
        return self.render_to_response(self.get_context_data(success=True))

    def form_invalid(self, form):
        """
        Overridden to ensure that a form object isn't returned, since
        that has some weird serialization issues. Instead pass back
        the errors from the form, and a JSON flag - { success: false }.

        @note: See form_valid for more discussion on the JSON flag.
        """
        context = self.get_context_data(success=False)
        context['errors'] = form.errors
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        """
        Overridden so that on a GET request the response isn't allowed.

        JSON Forms are intrinsinctly POST driven things, a GET makes
        no sense in the context of a form. (What would you get?). For
        Normal HTTP, you would pass back an empty form, but that's
        pretty usesless for JSON. So we pwn this entire method right
        off the bat to ensure no screwiness or excessive net traffic.
        """
        return HttpResponseNotAllowed(['GET', ])
