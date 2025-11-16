from django.shortcuts import render
from rest_framework.decorators import api_view  
from rest_framework.response import Response
from rest_framework import status
from .geminiService import generate_response

# Create your views here.
@api_view(['POST'])
def chat(request):
    try:
        if request.method == 'POST':
            data = request.data
            if 'message' not in data:
                return Response({'error': 'No se envió ningun mensaje'}, status=status.HTTP_400_BAD_REQUEST)
            response = generate_response(data['message'])
            return Response({'message': response}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
