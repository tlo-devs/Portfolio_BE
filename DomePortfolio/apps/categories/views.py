from mptt.templatetags.mptt_tags import cache_tree_children
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import CategoryTree


def recursive_node_to_dict(node):
    result = {
        'name': node.name,
        'key': node.key,
    }
    children = [recursive_node_to_dict(c) for c in node.get_children()]
    if children:
        result['children'] = children
    return result


@api_view(["GET"])
def portfolio(request):
    obj = [c for c in CategoryTree.objects.all() if c.get_root().key != "shop"]
    objs = CategoryTree.objects.all().filter(id__in=[node.id for node in obj])
    res = [
        recursive_node_to_dict(n) for n in cache_tree_children(
            objs
        )]
    return Response(res)


@api_view(["GET"])
def shop(request):
    obj = [c for c in CategoryTree.objects.all() if c.get_root().key != "portfolio"]
    objs = CategoryTree.objects.all().filter(id__in=[node.id for node in obj])
    res = [
        recursive_node_to_dict(n) for n in cache_tree_children(
            objs
        )]
    return Response(res)
