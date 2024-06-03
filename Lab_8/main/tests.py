from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Team, Player

class TeamViewSetTestCase(APITestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')

    def test_get_team_list(self):
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_team(self):
        url = reverse('team-list')
        data = {'name': 'New Team'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)

    def test_update_team(self):
        url = reverse('team-detail', args=[self.team.id])
        data = {'name': 'Updated Team'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, 'Updated Team')

    def test_delete_team(self):
        url = reverse('team-detail', args=[self.team.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.count(), 0)
