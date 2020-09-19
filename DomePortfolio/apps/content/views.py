from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .models import AboutSection
from .models.serializers import AboutSectionSerializer


@api_view(["GET"])
def about_view(request: Request) -> Response:
    about = AboutSection.objects.get(pk=1)
    serializer = AboutSectionSerializer(about)
    return Response(serializer.data)
