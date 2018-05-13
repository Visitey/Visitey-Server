from rest_framework import viewsets
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from rest_profile.models import Profile
from rest_profile.serializers import ProfileSerializer


# Create your views here.

class ProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update`, and `destroy` actions.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser,)

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        owner = self.request.query_params.get('owner', None)
        if owner is not None:
            return Profile.objects.filter(owner__username=owner)
        else:
            return Profile.objects.all()