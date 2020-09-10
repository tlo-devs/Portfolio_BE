from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
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
def category(request, root_key: str):
    root = get_object_or_404(
        CategoryTree.objects.all().filter(parent_id__isnull=True),
        key=root_key
    )
    res = recursive_node_to_dict(root)
    return Response(res)
