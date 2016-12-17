from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('admin:store_order_changelist'))

