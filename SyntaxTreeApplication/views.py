from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

# Create your views here.
from SyntaxTreeApplication.models import TreeParaphrase, tree_to_string


def paraphrase(request):
    tree_str = request.GET.get('tree', '')
    limit = request.GET.get('limit', 20)

    if not tree_str:
        return HttpResponseBadRequest('Tree parameter is required')
    if type(limit) != int and not limit.isnumeric():
        limit = 20

    try:
        tree = TreeParaphrase(tree_str, int(limit))
        res = tree.paraphrase()
    except ValueError:
        return HttpResponseBadRequest('Bad request, invalid string')

    data = {
        'paraphrase': [{'tree': tree_to_string(tr)} for tr in res],
    }

    return JsonResponse(data, json_dumps_params={'indent': 4})
