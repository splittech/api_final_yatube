from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from posts import models
from . import serializers
from . import permissions


class PostViewSet(ModelViewSet):

    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          permissions.AuthorOrReadOnly,)

    pagination_class = LimitOffsetPagination
    page_size = 10

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):

    serializer_class = serializers.CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          permissions.AuthorOrReadOnly,)

    def get_queryset(self):
        post = get_object_or_404(models.Post, pk=self.kwargs.get('post_id'))
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(models.Post, pk=self.kwargs.get('post_id'))
        if serializer.is_valid():
            serializer.save(author=self.request.user, post=post)
        return super().perform_create(serializer)


class GroupViewSet(ReadOnlyModelViewSet):

    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = (AllowAny,)


class FollowViewSet(ModelViewSet):

    serializer_class = serializers.FollowSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return models.Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
