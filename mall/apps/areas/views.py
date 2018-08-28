# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from areas.models import Areas
from areas.serializer import AreasSerializer, SubsSerializer


# noinspection PyUnresolvedReferences
class AreasViewSet(ReadOnlyModelViewSet):
    """序列化市区县"""
    # permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        if self.action == "list":
            return Areas.objects.filter(parent=None)
        return Areas.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AreasSerializer
        return SubsSerializer
