from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import CurrentUserDefault


from posts import models


class PostSerializer(serializers.ModelSerializer):

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = models.Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = models.Comment
        fields = '__all__'
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):

    user = SlugRelatedField(
        default=CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=models.User.objects.all()
    )

    class Meta:
        model = models.Follow
        fields = '__all__'
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=models.Follow.objects.all(),
                fields=('user', 'following'),
            ),
            serializers.UniqueTogetherValidator(
                queryset=models.Follow.objects.all(),
                fields=('user', 'user'),
            )
        )
