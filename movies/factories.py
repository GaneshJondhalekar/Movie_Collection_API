import factory
from django.contrib.auth.models import User
from .models import Movie, Collection, RequestCount
import uuid

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall('set_password', 'password')

class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    uuid = factory.LazyFunction(uuid.uuid4)
    name = factory.Faker('name')
    description = factory.Faker('text')
    genres = factory.Faker('word')

class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    uuid = factory.LazyFunction(uuid.uuid4)
    title = factory.Faker('sentence')
    description = factory.Faker('text')
    user = factory.SubFactory(UserFactory)

class RequestCountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RequestCount

    id = 1
    count = 0
