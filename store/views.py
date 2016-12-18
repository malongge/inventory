from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.http.response import JsonResponse

from .models import Goods


def goods_json(request, pk):
    var = {}
    try:
        g = Goods.objects.get(pk=pk)
        var = serialize('json', [g], ensure_ascii=False)[0]
    except ObjectDoesNotExist:
        pass

    return JsonResponse(var, safe=False)