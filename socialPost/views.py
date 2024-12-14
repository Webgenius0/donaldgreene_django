from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment, Like, Share
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, ShareSerializer
from rest_framework.permissions import IsAuthenticated

# Post List and Detail View
class PostList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Post list get successful",
            "data": serializer.data,
        }
        return Response(response_data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            serializer.save()
            response_data = {
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Post created successful",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Post detail get successful",
            "data": serializer.data,
        }
        return Response(response_data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Post updated successful",
                "data": serializer.data,
            }
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Like a Post
class PostLike(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if created:
            return Response({"status": "liked"}, status=status.HTTP_201_CREATED)
        return Response({"status": "already liked"}, status=status.HTTP_200_OK)


# Comment on a Post
class PostComment(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        content = request.data.get('content')
        if content:
            comment = Comment.objects.create(post=post, user=request.user, content=content)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response({"error": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)


# Share a Post
class PostShare(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        share = Share.objects.create(post=post, user=request.user)
        return Response({"status": "shared"}, status=status.HTTP_201_CREATED)


# Comment List for a specific Post
class CommentList(APIView):

    def get(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Comment list get successful",
            "data": serializer.data,
        }
        return Response(response_data)


# List of Likes for a specific Post
class LikeList(APIView):

    def get(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        likes = post.likes.all()
        serializer = LikeSerializer(likes, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Like list get successful",
            "data": serializer.data,
        }
        return Response(response_data)


# List of Shares for a specific Post
class ShareList(APIView):

    def get(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        shares = post.shares.all()
        serializer = ShareSerializer(shares, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Share list get successful",
            "data": serializer.data,
        }
        return Response(response_data)