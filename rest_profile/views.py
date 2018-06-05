from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from rest_profile.models import Profile
from rest_profile.serializers import ProfileSerializer


# Create your views here.

class ProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions.

      parameters:
        - name: owner
        in: query
        type: int
        description: Profile owner username
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser,)

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Profile.objects.filter(owner=self.request.user)
