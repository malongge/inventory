from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse


def index(request):
    return HttpResponseRedirect('/admin/sells')

