from .models import SocialPost
from .serializers import SocialPostSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SocialPostList(APIView):

    def get(self, request, format=None):
        socialPost = SocialPost.objects.filter(user=request.user)
        serializer = SocialPostSerializer(socialPost, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SocialPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class SocialPostDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return SocialPost.objects.get(pk=pk)
        except SocialPost.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        socialPost = self.get_object(pk)
        serializer = SocialPostSerializer(socialPost)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        socialPost = self.get_object(pk)
        serializer = SocialPostSerializer(socialPost, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)