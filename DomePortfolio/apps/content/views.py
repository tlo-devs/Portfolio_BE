from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .models import AboutSection, HomeSection
from .models.serializers import AboutSectionSerializer, HomeSectionSerializer


@api_view(["GET"])
def about_view(request: Request) -> Response:
    about = AboutSection.objects.get(pk=1)
    serializer = AboutSectionSerializer(about)
    return Response(serializer.data)


@api_view(["GET"])
def home_view(request: Request) -> Response:
    device = request.query_params.get("device")
    if device not in ("desktop", "mobile"):
        return Response(status=400)
    home = HomeSection.objects.get(pk=1)
    serializer = HomeSectionSerializer(home)
    video = serializer.data.get(f"video_{device}")
    return Response({"video": video})
