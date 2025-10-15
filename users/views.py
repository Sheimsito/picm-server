from rest_framework.decorators import api_view  
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


@csrf_exempt
@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Inicio de sesión exitoso"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "El usuario o la contraseña no son válidos. Verifica e inténtalo de nuevo."}, status=status.HTTP_401_UNAUTHORIZED) 
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@csrf_exempt
@api_view(['POST'])
def user_logout(request):
    try:
        logout(request)
        return Response({"message": "Cierre de sesión exitoso"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@csrf_exempt
@api_view(['POST'])
def password_reset(request): 
    data = request.data.get('email')
    email = data['email']
    if not email:
        return Response({"error": "El correo electrónico es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
    try: 
        user = User.objects.get(email=email)
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"http://localhost:5173/#/reset-password/{uid}/{token}"  # Genera un enlace real en producción
       
        send_mail(
            'Restablecimiento de contraseña',
            f'Hola {user.username}.\n\nVimos que solicistaste la recuperación de tu contraseña para llevar eso a cabo haz clic en el siguiente enlace para restablecer tu contraseña:\n{reset_link}\n\nSi no solicitaste este cambio, ignora este correo.',
            'kealgri@gmail.com',
            [email],
            fail_silently=False,
        )
        return Response({"message": "Se ha enviado un enlace de restablecimiento de contraseña a tu correo electrónico."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "No se encontró ningún usuario con ese correo electrónico."}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['POST'])
def confirm_password_reset(request):
    new_password = request.data.get('new_password')
    user_id = request.data.get('uid')
    token = request.data.get('token')
    if not new_password:
        return Response({"error": "La nueva contraseña es obligatoria."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        uid = force_str(urlsafe_base64_decode(user_id))
        user = User.objects.get(pk=uid)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "El token de restablecimiento de contraseña no es válido o ha expirado."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Contraseña restablecida exitosamente."}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)