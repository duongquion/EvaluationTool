from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from ..models import(
    CriteriaVersion
)
from ..serializers.criteria_version_serializer import(
    CriteriaVersionSerializer,
)
from ..constants import(
    ResponseMessage,
    CriteriaVersionMessage,
    MESSAGE
)
from ..utils import(
    check_state
)

class CriteriaVersionView(APIView):
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        version_name=kwargs.get("version_name")
        
        if version_name:
            get_version=self.get_criteria_version(version_name)
            return(get_version)
            
        else:
            all_version=self.all_criteria_version(request)
            return (all_version)
        
    def get_criteria_version(self, version_name):
        try:
            criteria_version = CriteriaVersion.objects.get(version_name=version_name)
            serializer = CriteriaVersionSerializer(criteria_version)
            return Response(serializer.data, status=status.HTTP_200_OK) 
        
        except CriteriaVersion.DoesNotExist:
            return Response(
                {MESSAGE: CriteriaVersionMessage.INVALID_VERSION},
                status=status.HTTP_404_NOT_FOUND
            )
        
        except ValidationError as ve:
            return Response(
                {MESSAGE: ve.detail}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {MESSAGE: str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )  
    
    def all_criteria_version(self, request):
        try:
            criteria_versions = CriteriaVersion.objects.all()
            if len(criteria_versions) < 1:
                return Response(
                    {MESSAGE:CriteriaVersionMessage.OBJECT_HAS_NO_VALUE},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            role_name = request.query_params.get("role_name")
            state = request.query_params.get("state")
            if role_name and state:
                criteria_versions = criteria_versions.filter(
                    role_name__exact=role_name, state__exact=state  
                )
            elif role_name:
                criteria_versions = criteria_versions.filter(
                    role_name__exact=role_name
                )
            elif state:
                criteria_versions = criteria_versions.filter(state__exact=state)
                
            serializer = CriteriaVersionSerializer(criteria_versions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as ve:
            return Response(
                {MESSAGE: ve.detail}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {MESSAGE: str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 

    @transaction.atomic
    def post(self, request):
        try:
            serializer = CriteriaVersionSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                criteria_version = serializer.save()
                return Response(
                    CriteriaVersionSerializer(criteria_version).data,
                    status=status.HTTP_201_CREATED
                )

        except ValidationError as ve:
            return Response(
                {MESSAGE: ve.detail}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {MESSAGE: str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        try:
            criteria_version = kwargs.get("version_name")
            instance=CriteriaVersion.objects.get(version_name=criteria_version)
            serializer = CriteriaVersionSerializer(instance, data=request.data, context={"request": request}, partial=True)
            
            if serializer.is_valid(raise_exception=True):
                current_state = instance.state
                new_state = serializer.validated_data.get("state", current_state)
                is_valid = check_state(
                    state=current_state,
                    model_name="Criteria Version",
                    new_state=new_state,
                )
                if not is_valid:
                    return Response(
                        {MESSAGE: ResponseMessage.CANT_UPDATE_STATE},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        
        except CriteriaVersion.DoesNotExist:
            return Response(
                {MESSAGE: CriteriaVersionMessage.INVALID_VERSION},
                status=status.HTTP_404_NOT_FOUND
            )

        except ValidationError as ve:
            return Response(
                {MESSAGE: ve.detail}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {MESSAGE: str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )