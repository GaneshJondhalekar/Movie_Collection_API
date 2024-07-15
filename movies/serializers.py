
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Collection, Movie

class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def create(self, validated_data):
        if User.objects.filter(username=validated_data.get('username')).exists():
            #print("Already user exist")
            return validated_data
        user=User.objects.create(username=validated_data['username'].lower())
        user.set_password(validated_data['password'])
        user.save()
        #print("created..................")
        return validated_data

    def get_jwt_token(self,data):
        #print("Token.............")
        user=authenticate(username=data['username'],password=data['password'])
        if user is None:
            return {'data':{},'message':"Invalid credentials"}
        
        refresh=RefreshToken.for_user(user)
        access=refresh.access_token
        #print('No isuue........')
        return {'access_token':str(access)}

    

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'genres', 'uuid')

class CollectionCreateSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ('title', 'description', 'movies','user')

    def create(self, validated_data):
        movies_data = validated_data.pop('movies')
        #print("################..",movies_data)
        collection = Collection.objects.create(**validated_data)
        #print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        for movie_data in movies_data:
            movie, _ = Movie.objects.get_or_create(**movie_data)
            collection.movies.add(movie)
        return collection    

class RetriveCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=('title','uuid','description')



class UpdateCollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description', 'movies']

    def update(self, instance, validated_data):
        movies_data = validated_data.pop('movies', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if movies_data:
            instance.movies.clear()
            for movie_data in movies_data:
                uuid = movie_data.get('uuid')
                if uuid:
                    movie, created = Movie.objects.get_or_create(uuid=uuid, defaults=movie_data)
                else:
                    movie = Movie.objects.create(**movie_data)
                instance.movies.add(movie)

        return instance

class GetCollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ['title', 'description', 'movies']
