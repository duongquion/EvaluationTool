from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import (
    CustomUser as User,
    Team,
    Employee,
)

from ..containts import (
    ErrorMessage,
)

from ..serializers import (
    TeamSerializer,
)

@csrf_exempt
@api_view(["GET"])
def list_team(request):
    try:
        user = request.user
        if not isinstance(user, User):
            return JsonResponse(
                {"message": ErrorMessage.AUTHENTICATION_REQUIRED},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            
        if user.is_default_password:
            return JsonResponse(
                {
                    "set_password": True,
                    "message": ErrorMessage.PASSWORD_HAS_NOT_BEEN_CHANGED
                },
                status=status.HTTP_403_FORBIDDEN,
            )
       
        employees = Employee.objects.filter(user__username = user, is_active = True)
        if not employees.exists():
            return JsonResponse({
                "message": ErrorMessage.NOT_PART_OF_ANY_TEAM
            }, status=status.HTTP_404_NOT_FOUND)
       
        teams = Team.objects.filter(id__in = [employee.team.id for employee in employees])
 
        serializer = TeamSerializer(teams, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return JsonResponse({
            'message' : str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)