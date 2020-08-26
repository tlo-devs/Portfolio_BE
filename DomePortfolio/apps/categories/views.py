from drf_yasg.utils import swagger_auto_schema
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


@swagger_auto_schema(
    method="GET",
    operation_summary="Get Categories",
    security=[]
)
@api_view(["GET"])
def category(request):
    root_type = [p for p in request.path.split("/") if p][-1]
    res = [
        recursive_node_to_dict(n) for n in cache_tree_children(
            getattr(CategoryTree, root_type).all()
        )]
    return Response(res)
