from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

# Create your views here.
from SyntaxTreeApplication.syntax_tree import tree_to_string, paraphrase as phr


def paraphrase(request):
    tree = request.GET.get('tree', '')
    limit = request.GET.get('limit', 20)

    if not tree:
        return HttpResponseBadRequest('Tree parameter is required')
    if type(limit) != int and not limit.isnumeric():
        limit = 20

    try:
        res = phr(tree, int(limit))
    except ValueError:
        return HttpResponseBadRequest('Bad request, invalid string')

    data = {
        'paraphrase': [{'tree': tree_to_string(tr)} for tr in res],
    }

    return JsonResponse(data, json_dumps_params={'indent': 4})
