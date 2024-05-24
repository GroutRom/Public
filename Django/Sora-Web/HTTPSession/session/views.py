import json
import secrets
import random
import string
import logging
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
from .models import User, Device, Session
from datetime import datetime, timedelta
from django.views.decorators.http import require_GET
from django.utils import timezone


logger = logging.getLogger('mylogger')

@csrf_exempt
def create_session(request):
    if request.method == 'POST':
        
        logger.info("Début de la création de session")
        try :
            mode = request.GET.get('mode')
            if mode != "email" :
                return JsonResponse({'error': 'mode is not equal to email'}, status=400)

            # Récupére les données JSON de la requête
            data = json.loads(request.body)

            # Valider les informations de l'utilisateur
            if 'user' not in data or 'email' not in data['user']:
                return JsonResponse({'error': 'User email is required'}, status=400)

            # Valider email de l'utilisateur
            user_email = data['user']['email']
            validate_email(user_email)
        
            # Valider le type de l'appareil
            if 'device' not in data or 'type' not in data['device']:
                return JsonResponse({'error': 'Device type is required'}, status=400)
            device_type = data['device']['type']
            valid_device_types = ['mobi', 'othr']
            if device_type not in valid_device_types:
                return JsonResponse({'error': 'Invalid device type'}, status=400)

            device_vendor_uuid = data['device'].get('vendor_uuid')

            #Valider le vendor uuid
            if device_vendor_uuid is None and device_type == 'mobi':
                return JsonResponse({'error': 'Vendor UUID is required for mobi type'}, status=400)
        
            # Générer un token de session
            session_token = secrets.token_hex(16)

         
            # Créer ou récupérer l'utilisateur
            user, user_created = User.objects.get_or_create(email=user_email)

             # Vérifier si le device existe déjà pour cet utilisateur et ce type
            device = Device.objects.filter(user=user, type=device_type, vendor_uuid=device_vendor_uuid).first()

            # Si le device n'existe pas, le créer
            if not device:
                device = Device.objects.create(user=user, type=device_type, vendor_uuid=device_vendor_uuid)
                device_created = True
            else:
                device_created = False

            # Vérifier s'il existe des sessions pour ce device
            if device.session_set.exists():
                last_session = device.session_set.latest('created_at')
                last_session_created_at = last_session.created_at

                if last_session.status == 'expired':
                    last_session.save()
                elif timezone.now() >= last_session.created_at + timedelta(hours=2) and device_type == 'othr':
                    last_session.status = 'expired'
                    last_session.save()
                    return JsonResponse({'error': 'Token expired'}, status=401)

            else :
                last_session_created_at = None
                last_session_status = None

            # Si le device est créé ou si la dernière session pour ce device est expirée
            if device_created or (last_session_created_at and timezone.now() >= last_session_created_at + timedelta(hours=2) and device_type == 'othr'):

                # Générer un code OTP (ici, un code à 6 chiffres)
                otp_code = ''.join(random.choices(string.digits, k=6))


                # Créer une nouvelle instance de session
                session = Session.objects.create(
                    token=session_token,
                    user=user,
                    device=device,
                    otp_code=otp_code
                )
                logger.info(f"Fin de la création de session, otp_code = {otp_code}")
                
                # Retourner une réponse avec status 201 si le device est créé et 200 sinon
                status_code = 201 if device_created else 200

            else:
                # Si aucune session n'est créée, retourner simplement le dernier session existant avec status 200
                session = device.session_set.latest('created_at')
                status_code = 200
                logger.info("Session déjà existante")

            return JsonResponse({
                    'uuid': f'ses-{str(session.uuid)}',
                    'created_at': session.created_at,
                    'token': session.token,
                    'is_new_user': user_created,
                    'is_new_device': device_created,
                    'user': {
                        'uuid' : f'usr-{str(user.uuid)}',
                        'email': user.email
                    },
                    'device': {
                        'uuid': f'dev-{str(device.uuid)}',
                        'type': device.type,
                        'vendor_uuid': device.vendor_uuid
                    },
                    'status': session.status,
                }, status= status_code)
            
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def confirm_session(request, session_uuid):
    if request.method == 'PATCH' or request.method == 'PUT':
        
        try :

            # Récupérer le code de confirmation de la requête
            data = json.loads(request.body)


            logger.info(f"Début de la confirmation de session pour l'UUID : {session_uuid}")
            
            otp_code = data.get('otp_code')

            if not otp_code:
                return JsonResponse({'error': 'OTP code is required'}, status=400)

            # Récupérer la session correspondant à l'UUID fourni
            session = Session.objects.get(uuid=session_uuid)
            
            if not token_verification(request, session):
                return JsonResponse({'error':'Invalid token'}, status=401)

            # Vérifier si la session est expirée
            if session.is_expired():
                session.status = 'expired'
                session.save()
                return JsonResponse({'error': 'Session is expired'}, status=401)

            # Vérifier si le code de confirmation est correct
            if otp_code != session.otp_code:
                return JsonResponse({'error': 'Invalid OTP code'}, status=401)

            # Mettre à jour le statut de la session
            session.status = 'confirmed'
            session.save()
            logger.info(f"Session confirmée avec succès pour l'UUID : {session_uuid}")
            
            # Retourner la réponse appropriée
            return JsonResponse({
                'uuid': f'ses-{str(session.uuid)}',
                'created_at': session.created_at,
                'token': session.token,
                'is_new_user': session.is_new_user,
                'is_new_device': session.is_new_device,
                'user': {
                    'uuid' : f'usr-{str(session.user.uuid)}',
                    'email': session.user.email
                },
                'device': {
                    'uuid': f'dev-{str(session.device.uuid)}',
                    'type': session.device.type,
                    'vendor_uuid': session.device.vendor_uuid
                },
                'status': session.status
            }, status=200)
        
        except Session.DoesNotExist:
            return JsonResponse({'error': 'Session not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


def token_verification (request, session) :

    try :
        header = request.META.get('HTTP_AUTHORIZATION', "")
        logger.info({header})
        if not header:
            return False
        bearer, token = header.split(" ")
        if(bearer != "Bearer"):
            return False

        return (token == session.token)
        
    except :
        return False





