from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from ..serializers import (
    ChangePasswordSerializer,
    SetPasswordSerializer,
)
from ..models import (
    CustomUser as User,
)
from ..containts import (
    SuccessMessage,
    ErrorMessage,
)

@csrf_exempt
@api_view(['POST'])
def change_password(request):
    try:
        serializer = ChangePasswordSerializer(data=request.data)
 
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
       
        user = User.objects.get(username= serializer.validated_data['username'])
        if not user.is_active:
            return JsonResponse({
                "id": "username",
                "message": ErrorMessage.USER_NOT_ALLOWED
            }, status = status.HTTP_403_FORBIDDEN)
       
        if user.is_default_password:
            return JsonResponse({
                "id" : "password",
                "message" : ErrorMessage.USER_NOT_ALLOWED
            }, status = status.HTTP_403_FORBIDDEN)
       
        if not user.check_password(serializer.validated_data['password']):
            return JsonResponse({
                "id": "oldpassword",
                "message": ErrorMessage.INCORRECT_USERNAME_PASSWORD
                }, status=status.HTTP_404_NOT_FOUND)
       
        user.set_password(serializer.validated_data['new_password'])
        user.save()
 
        return JsonResponse({
            "message": SuccessMessage.CHANGE_PASSWORD_SUCCESSFULLY
        }, status=status.HTTP_200_OK)
           
    except User.DoesNotExist:
        return JsonResponse({
            "id": "username",
            "message": ErrorMessage.INCORRECT_USERNAME_PASSWORD
            }, status=status.HTTP_404_NOT_FOUND)
   
    except Exception as e:
        return JsonResponse({'message': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@csrf_exempt
@api_view(['POST'])
def set_password(request):
    try:
        serializer = SetPasswordSerializer(data=request.data)
       
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
        user = User.objects.get(username=serializer.validated_data['username'])    
        if not user.is_active:
            return JsonResponse({
                "id": "username",
                "message": ErrorMessage.USER_NOT_ALLOWED
            }, status = status.HTTP_403_FORBIDDEN)
           
        if not user.check_password(serializer.validated_data['password']):
            return JsonResponse({
                "id": "password",
                "message": ErrorMessage.INCORRECT_USERNAME_PASSWORD
                }, status=status.HTTP_404_NOT_FOUND)
       
        if not user.is_default_password:
            return JsonResponse({
                "message": ErrorMessage.PASSWORD_HAS_BEEN_CHANGED
            },status = status.HTTP_301_MOVED_PERMANENTLY)
           
        user.set_password(serializer.validated_data['new_password'])
        user.is_default_password = False
        user.question = serializer.validated_data['question']
        user.answer = serializer.validated_data['answer']
        user.init_password = None
        user.save()
        return JsonResponse({
            "message": SuccessMessage.CHANGE_PASSWORD_SUCCESSFULLY
        }, status=status.HTTP_200_OK)
   
    except User.DoesNotExist:
        return JsonResponse({
            "id": "username",
            "message": ErrorMessage.INCORRECT_USERNAME_PASSWORD
            }, status=status.HTTP_404_NOT_FOUND)
   
    except Exception as e:
        return JsonResponse({'message': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)