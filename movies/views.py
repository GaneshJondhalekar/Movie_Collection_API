
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from tenacity import retry, stop_after_attempt, wait_exponential
from .serializers import *
import os
import requests
from collections import Counter
import itertools
from .models import RequestCount

class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                response=serializer.get_jwt_token(serializer.validated_data)
                #print("get it......")
                return Response(
                    response
                , status=status.HTTP_201_CREATED)
            return Response({
                'data': serializer.errors,
                'message': "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            #print(e)
            return Response({
                'data': {},
                'message': "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=LoginSerializer(data=data)
            if serializer.is_valid():
                response=serializer.get_jwt_token(serializer.validated_data)
              
                return Response(response,status=status.HTTP_200_OK)
            
            return Response({
                'data':serializer.errors,
                'message':"something wents wrong"
            },status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print(e)
            return Response({
                'data':{},
                'message':"something wents wrong"
            },status=status.HTTP_400_BAD_REQUEST)


class MovieListView(APIView):
    permission_classes = [IsAuthenticated]
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=6))
    def fetch_movies(self):
        #print('..........................................')
        username = os.getenv('MOVIE_API_USERNAME')
        password = os.getenv('MOVIE_API_PASSWORD')
        #With username and password api is not working so i tried without username and password. It is working well
        response = requests.get('https://demo.credy.in/api/v1/maya/movies/',verify=False)
        #print(response.status_code)
        response.raise_for_status()
        return response.json()

    def get(self, request):
        try:
            data = self.fetch_movies()
            return Response(data)
        except requests.exceptions.HTTPError as e:
            return Response({'error':'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
        except requests.RequestException as e:
            return Response({'error': 'Temporary unavailable'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class CollectionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        data=request.data
        data['user']=request.user.id
        serializer = CollectionCreateSerializer(data=data)
        #print(request.data,'.......',data)
        if serializer.is_valid():
            collection=serializer.save()
            return Response({'collection_uuid':collection.uuid} , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request,*args,**kwargs):
        user=request.user
        my_collections=Collection.objects.prefetch_related('movies').filter(user=user)
        serializer=RetriveCollectionSerializer(my_collections,many=True)
       
        all_genres=[]
        for collection in my_collections:
            for movie in collection.movies.all():
                genres = movie.genres.split(',')
                all_genres.extend(genres)
        #print(all_genres,'........###')     
        genre_counter = Counter(all_genres)
        #print(genre_counter,'........###') 
        
        top_genres = [genre for genre, _ in genre_counter.most_common(3)]
        all_top_genres= ",".join(top_genres)

        data = {
            "is_success": True,
            "data": {
                "collections": serializer.data,
                "favourite_genres": all_top_genres
            }
        }
        
        return Response(data, status=status.HTTP_200_OK)


class DetailCollectionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, uuid, *args, **kwargs):
        collection = Collection.objects.prefetch_related('movies').filter(uuid=uuid).first()
        if not collection:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateCollectionSerializer(collection, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Successfully collection updated','data':serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, uuid, *args, **kwargs):
        collection = Collection.objects.filter(uuid=uuid).first()
        if not collection:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UpdateCollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, uuid, *args, **kwargs):
        collection = Collection.objects.filter(uuid=uuid).first()
        if not collection:
            return Response({'error': 'Collection not found'}, status=status.HTTP_404_NOT_FOUND)
        
        collection.delete()
        return Response({'message': 'Collection deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class RequestCountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            count = RequestCount.objects.get(id=1).count
        except RequestCount.DoesNotExist:
            count = 0
        return Response({"requests": count}, status=status.HTTP_200_OK)
    
class ResetRequestCountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        RequestCount.objects.update_or_create(id=1, defaults={'count': 0})
        return Response({"message": "request count reset successfully"}, status=status.HTTP_200_OK)