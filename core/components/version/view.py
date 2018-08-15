from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from core.models import Version
from core.serializers import VersionDetailSerializer
from core.serializers import VersionListSerializer
from core.serializers import VersionCreateSerializer


class VersionCreateView(CreateAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionCreateSerializer


class VersionListView(ListAPIView):

    def get_queryset(self):
        return Version.objects.filter(company_id=self.kwargs["company_id"])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = VersionListSerializer(queryset, many=True)
        return Response(serializer.data)


class VersionDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Version.objects.all()
    serializer_class = VersionDetailSerializer
