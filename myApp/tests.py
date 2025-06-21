from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Quote, Like, Comment
from django.contrib.auth import get_user_model


User = get_user_model()


class QuoteViewSetTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')

        self.client = APIClient()
        self.client.force_authenticate(self.user1)

        self.quote1 = Quote.objects.create(body='First quote', author='Author1', publisher=self.user1)
        self.quote2 = Quote.objects.create(body='Second quote', author='Author2', publisher=self.user2)

        self.like = Like.objects.create(user=self.user1, quote=self.quote1)
        self.comment = Comment.objects.create(publisher=self.user1, body='First comment', quote=self.quote1)

    def test_list_quotes(self):
        url = reverse('api:quotes-list')
        rs = self.client.get(url)
        self.assertEqual(rs.status_code, status.HTTP_200_OK)
        self.assertIn('results', rs.data)
        self.assertGreaterEqual(len(rs.data['results']), 1)

    def test_retrieve_quote(self):
        url = reverse('api:quotes-detail', args=[self.quote1.id])
        rs = self.client.get(url)
        self.assertEqual(rs.status_code, status.HTTP_200_OK)
        self.assertEqual(rs.data['id'], self.quote1.id)

    def test_create_quote(self):
        url = reverse('api:quotes-list')
        data = {
            'body': 'New test quote',
            'author': 'TestAuthor',
            'publisher': self.user1.id
        }
        rs = self.client.post(url, data)
        self.assertEqual(rs.status_code, status.HTTP_201_CREATED)

    def test_update_quote(self):
        url = reverse('api:quotes-detail', args=[self.quote1.id])
        data = {'body': 'updated', 'author': 'updated', 'publisher': self.user1.id}
        rs = self.client.put(url, data)
        self.assertEqual(rs.status_code, status.HTTP_200_OK)
        self.quote1.refresh_from_db()
        self.assertEqual(self.quote1.body, 'updated')

    def test_delete_quote(self):
        url = reverse('api:quotes-detail', args=[self.quote1.id])
        rs = self.client.delete(url)
        self.assertEqual(rs.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Quote.objects.filter(id=self.quote1.id).exists())

    def test_like_action(self):
        url = reverse('api:quotes-like', args=[self.quote1.id])
        rs = self.client.get(url)
        self.assertEqual(rs.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rs.data['likes']), 1)
        self.assertEqual(rs.data['likes'][0]['user'], self.user1.id)

    def test_like_action_no_likes(self):
        url = reverse('api:quotes-like', args=[self.quote2.id])
        rs = self.client.get(url)
        self.assertEqual(rs.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rs.data['likes']), 0)

    def test_comments_action(self):
        url = reverse('api:quotes-comments', args=[self.quote1.id])
        rs = self.client.get(url)
        self.assertEqual(rs.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rs.data['comments']), 1)
        self.assertEqual(rs.data['comments'][0]['publisher'], self.user1.id)

    def test_comments_action_no_comments(self):
        url = reverse('api:quotes-comments', args=[self.quote2.id])
        rs = self.client.get(url)
        self.assertEqual(rs.status_code, status.HTTP_200_OK)
        self.assertEqual(len(rs.data['comments']), 0)

    def test_authenticated_create_forbidden(self):
        self.client.logout()
        url = reverse('api:quotes-list')
        data = {'body': 'Unauthorized quote', 'author': 'NoAuth', 'publisher': self.user1.id}
        rs = self.client.post(url, data)
        self.assertEqual(rs.status_code, status.HTTP_403_FORBIDDEN)

