from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api_v2.serializer import PostSerializer
from posts.models import Post
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return super().get_permissions()


class PostApiView(APIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        post = Post.objects.all()
        return post

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk=None,  *args, **kwargs):
        id = pk or request.query_params.get('id')
        if id:
            serializer = PostSerializer(self.get_object(id))
        else:
            serializer = PostSerializer(self.get_queryset(), many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def put(self, request, pk=None, *args, **kwargs):
        post_object = self.get_object(pk or request.query_params.get('id'))
        data = request.data

        post_object.title = data["title"]
        post_object.caption = data["caption"]
        post_object.slug = data["slug"]
        post_object.user = data["user"]

        post_object.save()

        serializer = PostSerializer(post_object)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        todo_object = self.get_object(pk or request.query_params.get('id'))
        todo_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
