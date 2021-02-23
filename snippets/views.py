"""
Views for the Snippets API
"""

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetViewSet(viewsets.ModelViewSet):
    """
    The viewset provides `list`, `create`, `retrieve`, `update` and
    `destroy` actions.

    We also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly]
    
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        """
        Custom view to present a highlighted snippet.
        """
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        """
        Associate snippet with user creating it.
        """
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
