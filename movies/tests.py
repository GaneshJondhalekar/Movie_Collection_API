from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Collection

class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')
        self.valid_payload = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        self.invalid_payload = {
            'username': '', 
            'password': 'testpassword123'
        }

    def test_register_valid_payload(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.data)


    def test_register_invalid_payload(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], "Something went wrong")

    



class CollectionAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create_retieve_collection')
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {
            'title': 'Test Collection',
            'description': 'This is a test collection',
            'movies':[
       
                    {
                        "title": "Robin Hood",
                        "description": "Yet another version of the classic epic, with enough variation to make it interesting. The story is the same, but some of the characters are quite different from the usual, in particular Uma Thurman's very special maid Marian. The photography is also great, giving the story a somewhat darker tone.",
                        "genres": "Drama,Action,Romance",
                        "uuid": "73399935-2165-41f0-a6a4-1336ef5e5c20"
                    }
        
                ]
        }
       

    def test_create_collection_valid_payload(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('collection_uuid', response.data)

class CollectionAPIViewGetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('create_retieve_collection')
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.force_authenticate(user=self.user)
        
       
        self.collection1 = Collection.objects.create(title='Collection 1', user=self.user)
        self.collection2 = Collection.objects.create(title='Collection 2', user=self.user)

        
        self.valid_payload = {
            'title': 'Test Collection',
            'description': 'This is a test collection',
            'movies': [
                {
                    "title": "Robin Hood",
                    "description": "Yet another version of the classic epic, with enough variation to make it interesting. The story is the same, but some of the characters are quite different from the usual, in particular Uma Thurman's very special maid Marian. The photography is also great, giving the story a somewhat darker tone.",
                    "genres": "Drama,Action,Romance",
                    "uuid": "73399935-2165-41f0-a6a4-1336ef5e5c20"
                }
            ]
        }

    def test_get_collections(self):
        
        response_create = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response_create.status_code, status.HTTP_201_CREATED)

       
        response_get = self.client.get(self.url)

       
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertIn('collections', response_get.data['data'])
       

       
        self.assertEqual(len(response_get.data['data']['collections']), 3) 
        self.assertEqual(response_get.data['data']['collections'][0]['title'], 'Collection 1')
        self.assertEqual(response_get.data['data']['collections'][1]['title'], 'Collection 2')
        self.assertEqual(response_get.data['data']['collections'][2]['title'], 'Test Collection')

class DetailCollectionAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.client.force_authenticate(user=self.user)
        
        
        self.collection = Collection.objects.create(
            title='Test Collection',
            description='This is a test collection',
            user=self.user
        )
        self.url = reverse('collection_detail', kwargs={'uuid': self.collection.uuid})

    def test_get_collection(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Collection')
        
    def test_update_collection(self):
        updated_data = {
            'title': 'Updated Collection',
            'description': 'Updated description'
        }
        response = self.client.put(self.url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Successfully collection updated')
        self.assertEqual(response.data['data']['title'], 'Updated Collection')
       

    def test_delete_collection(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Collection.objects.filter(uuid=self.collection.uuid).exists())
        
if __name__ == '__main__':
    TestCase.main()

