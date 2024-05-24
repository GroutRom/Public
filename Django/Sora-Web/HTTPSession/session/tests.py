from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Session
import json
import logging
import time


class SessionViewsTest(TestCase):

    logger = logging.getLogger('mylogger')
    
    def setUp(self):
        self.client = Client()
        self.create_session_url = reverse('create_session')
        self.session_uuid = None

    def test_create_session(self):
        
        # Créer une session avec des données incorrectes
        data = {'user': {}, 'device': {}}
        response = self.client.post(self.create_session_url + '?mode=email', data=json.dumps(data), content_type='application/json', HTTP_MODE='email')
        self.assertEqual(response.status_code, 400)

        # Créer une session avec des données correctes
        data = {
            'user': {'email': 'emailtest@test.com'},
            'device': {'type': 'mobi', 'vendor_uuid': '4854bf18-9e11-4e98-9762-fba8be4f8187'}
        }
        response = self.client.post(self.create_session_url + '?mode=email', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        # Récupérer l'UUID de la session créée
        session_uuid = response.json()['uuid'][4:]
        self.logger.info({session_uuid})

        # Tentative de confirmation de session sans code OTP
        response = self.client.patch(reverse('confirm_session', kwargs={'session_uuid': session_uuid}), data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Tentative de confirmation de session avec un code OTP invalide
        response = self.client.patch(reverse('confirm_session', kwargs={'session_uuid': session_uuid}), data=json.dumps({'otp_code': 'invalid_code'}), content_type='application/json')
        self.assertEqual(response.status_code, 401)

        # Tentative de confirmation de session avec un code OTP valide
        # Nous ne pouvons pas vraiment tester cela car le code OTP est généré aléatoirement et enregistré dans les logs, mais nous pouvons simuler un comportement réussi
        # Créons une instance de session correspondant à la session créée
        from .models import Session
        session = Session.objects.get(uuid=session_uuid)
        session.otp_code = '123456'  # Simulation du code OTP valide
        session.token = '1bbdebf5b44bb7d87808a6d527515df9' # Simulation token valide
        session.save()

        self.logger.info({session.otp_code})
        response = self.client.patch(reverse('confirm_session', kwargs={'session_uuid': session_uuid}), data=json.dumps({'otp_code': '123456'}), content_type='application/json', HTTP_AUTHORIZATION="Bearer 1bbdebf5b44bb7d87808a6d527515df9")
        self.assertEqual(response.status_code, 200)

    def test_is_expired(self):
        # Tester si une session est expirée
        expired_session = Session(created_at=timezone.now() - timezone.timedelta(minutes=6))
        self.assertTrue(expired_session.is_expired())

        # Tester si une session n'est pas expirée
        valid_session = Session(created_at=timezone.now())
        self.assertFalse(valid_session.is_expired())

    def test_device_token_expiry(self):
        # Créer une session avec un type de device 'othr'
        data = {
            'user': {'email': 'test@tests.com'},
            'device': {'type': 'othr', 'vendor_uuid': 'a5fc879a-8042-4b3b-8cdc-fd89b6d5844d'}
        }
        response = self.client.post(self.create_session_url + '?mode=email', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        
        # Récupérer l'UUID de la session créée
        session_uuid = response.json()['uuid'][4:]

        # Récupérer le token de la session créée
        token = Session.objects.get(uuid=session_uuid).token

        # Simuler une session créée il y a moins de 2h
        session = Session.objects.get(uuid=session_uuid)
        session.created_at = timezone.now() - timezone.timedelta(hours=1, minutes=30)
        session.save()

        # Effectuer une requête avec le même token (cela devrait réussir car la session est toujours active)
        response = self.client.post(self.create_session_url + '?mode=email', data=json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, 200)

        # Simuler une session créée il y a plus de 2h
        expired_session = Session.objects.get(uuid=session_uuid)
        expired_session.created_at = timezone.now() - timezone.timedelta(hours=3)
        expired_session.save()

        # Effectuer une autre requête avec le même token (cela devrait échouer car la session est expirée)
        response = self.client.post(self.create_session_url + '?mode=email', data=json.dumps(data), content_type='application/json', HTTP_AUTHORIZATION='Bearer ' + token)
        self.assertEqual(response.status_code, 401)
