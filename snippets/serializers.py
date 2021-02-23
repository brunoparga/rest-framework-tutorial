"""
JSON serializers for the Snippets app.
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(
        view_name='snippet-highlight',
        format='html'
    )

    class Meta(object):
        model = Snippet
        fields = ['url', 'id', 'owner', 'title', 'code', 'linenos',
            'highlight', 'language', 'style']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='snippet-detail',
        read_only=True
    )

    class Meta(object):
        model = User
        fields = ['url', 'id', 'username', 'snippets']