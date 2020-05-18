""" Events Tests """
import datetime
import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.factories import AccountFactory
from events.factories import EventFactory


class EventTestCase(APITestCase):
    """
    Events tests
    """
    def setUp(self):
        self.account = AccountFactory()
        self.event = EventFactory()
        self.event_stub = EventFactory.stub().__dict__
        self.event_stub['date'] = self.event_stub['date'].isoformat()
        del self.event_stub['created_by']

    def test_unauthenticated_list_events(self):
        """
        GIVEN An unauthenticated user
        WHEN tries to list all the events
        THEN should see a list of events sorted
        """
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        EventFactory.create_batch(10, **{'date': yesterday})
        EventFactory.create_batch(2, **{'date': tomorrow})
        response = self.client.get(reverse('events-list'))
        stored_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'response does not has 200 OK.')
        # Check first elements are upcoming
        for event in stored_data.get('results')[:2]:
            self.assertEqual(event['date'], tomorrow.isoformat(), 'Event is not upcoming')

    def test_unauthenticated_get_events(self):
        """
        GIVEN An unauthenticated user
        WHEN fetch for a single event
        THEN should see it's details
        """
        response = self.client.get(reverse('events-detail', kwargs={'pk': self.event.pk}))
        stored_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK, 'response does not has 200 OK.')
        self.assertEqual(stored_data['id'], self.event.pk, 'PK field does not match')
        self.assertEqual(stored_data['title'], self.event.title, 'title field does not match')
        self.assertEqual(stored_data['description'], self.event.description, 'description field does not match')
        self.assertEqual(stored_data['date'], self.event.date.isoformat(), 'date field does not match')
        self.assertEqual(stored_data['created_by'], self.event.created_by.username,
                         'username of user is not displayed')
        self.assertIn('count_participants', stored_data, 'count_participants field is not displayed')
        self.assertIn('attends', stored_data, 'count_participants field is not displayed')

    def test_unauthenticated_delete_events(self):
        """
        GIVEN An unauthenticated user
        WHEN tries to delete an event
        THEN should not be able to delete it
        """
        response = self.client.delete(reverse('events-detail', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'response does not has 401 status')

    def test_unauthenticated_create_events(self):
        """
        GIVEN An unauthenticated user
        WHEN tries to create an event
        THEN should not be able to create it
        """
        response = self.client.post(
            reverse('events-list'),
            json.dumps(self.event_stub),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'response does not has 401 status')

    def test_authenticated_create_events(self):
        """
        GIVEN An authenticated user
        WHEN tries to create an event
        THEN should be able to create it
        """
        self.client.force_login(self.account)
        response = self.client.post(
            reverse('events-list'),
            json.dumps(self.event_stub),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, 'response does not has 201 status')

    def test_authenticated_another_user_update_events(self):
        """
        GIVEN An authenticated user
        WHEN tries to update another's user event
        THEN should not be able to update it
        """
        self.client.force_login(self.account)
        response = self.client.put(
            reverse('events-detail', kwargs={'pk': self.event.pk}),
            json.dumps(self.event_stub),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, 'response does not has 403 status')

    def test_authenticated_update_events(self):
        """
        GIVEN An authenticated user
        WHEN tries to update his event
        THEN should be able to update it
        """
        self.client.force_login(self.account)
        event = EventFactory(created_by=self.account)
        response = self.client.put(
            reverse('events-detail', kwargs={'pk': event.pk}),
            json.dumps(self.event_stub),
            content_type='application/json'
        )
        stored_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'response does not has 200 status')
        self.assertEqual(stored_data['title'], self.event_stub['title'], 'title field does not match')
        self.assertEqual(stored_data['description'], self.event_stub['description'], 'description field does not match')
        self.assertEqual(stored_data['date'], self.event_stub['date'], 'date field does not match')

    def test_unauthenticated_attend_event(self):
        """
        GIVEN An unauthenticated user
        WHEN tries to attend an event
        THEN should be not able to do it
        """
        response = self.client.post(
            reverse('events-attend', kwargs={'pk': self.event.pk}),
            json.dumps({'attend': True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 'response does not has 401 status')

    def test_authenticated_attend_event(self):
        """
        GIVEN An authenticated user
        WHEN tries to attend an event
        THEN should not be able to do it
        """
        self.client.force_login(self.account)
        response = self.client.post(
            reverse('events-attend', kwargs={'pk': self.event.pk}),
            json.dumps({'attend': True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'response does not has 204 status')

    def test_authenticated_withdraw_event(self):
        """
        GIVEN An authenticated user
        WHEN tries to withdraw from an event
        THEN should be able to do it
        """
        self.event.participants.add(self.account)
        self.client.force_login(self.account)
        response = self.client.post(
            reverse('events-attend', kwargs={'pk': self.event.pk}),
            json.dumps({'attend': False}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, 'response does not has 204 status')

    def test_authenticated_attend_event_again(self):
        """
        GIVEN An authenticated user
        WHEN tries to attend an event two times
        THEN should not be able to do it
        """
        self.event.participants.add(self.account)
        self.client.force_login(self.account)
        response = self.client.post(
            reverse('events-attend', kwargs={'pk': self.event.pk}),
            json.dumps({'attend': True}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'response does not has 400 status')

    def test_authenticated_withdraw_event_again(self):
        """
        GIVEN An authenticated user
        WHEN tries to withdraw from an event two times
        THEN should not be able to do it
        """
        self.client.force_login(self.account)
        response = self.client.post(
            reverse('events-attend', kwargs={'pk': self.event.pk}),
            json.dumps({'attend': False}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'response does not has 400 status')
