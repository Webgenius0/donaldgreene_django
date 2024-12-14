from .models import DayStory, DayStoryComment, DayStoryLike, DayStoryShare
from .serializers import (
    DayStorySerializer,
    DayStoryCommentSerializer,
    DayStoryLikeSerializer,
    DayStoryShareSerializer,
)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# for story
class DayStoryList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        dayStory = DayStory.objects.all()
        serializer = DayStorySerializer(dayStory, many=True)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Day story list get successful",
            "data": serializer.data,
        }
        return Response(response_data)

    def post(self, request, format=None):
        serializer = DayStorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            serializer.save()
            response_data = {
                "status": status.HTTP_201_CREATED,
                "success": True,
                "message": "Day story created successful",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DayStoryDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return DayStory.objects.get(pk=pk)
        except DayStory.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dayStory = self.get_object(pk)
        serializer = DayStorySerializer(dayStory)
        response_data = {
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Day story get successful",
            "data": serializer.data,
        }
        return Response(response_data)

    def put(self, request, pk, format=None):
        dayStory = self.get_object(pk)
        serializer = DayStorySerializer(dayStory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Day story updated successful",
                "data": serializer.data,
            }
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#  post like

class DayStoryLikeList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        dayStoryLike = DayStoryLike.objects.filter(user=request.user)
        serializer = DayStoryLike(dayStoryLike, many=True)
        return Response(serializer.data)

    def post(self, request,pk, format=None):
        day_story = DayStory.objects.get(pk=pk)
        serializer = DayStoryLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(day_story=day_story, user=request.user)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# post comments 
class DayStoryCommentList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        dayStoryComment = DayStoryComment.objects.filter(user=request.user)
        serializer = DayStoryCommentSerializer(dayStoryComment, many=True)
        return Response(serializer.data)

    def post(self, request,pk, format=None):
        day_story = DayStory.objects.get(pk=pk)
        serializer = DayStoryCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, day_story=day_story)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# shere story

class DayStoryShareList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        dayStoryShare = DayStoryShare.objects.filter(user=request.user)
        serializer = DayStoryShareSerializer(dayStoryShare, many=True)
        return Response(serializer.data)

    def post(self, request,pk, format=None):
        day_story = DayStory.objects.get(pk=pk)
        serializer = DayStoryShareSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, day_story=day_story)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)