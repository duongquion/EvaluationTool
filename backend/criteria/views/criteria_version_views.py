from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from ..models import(
    CriteriaVersion
)
from users.models import(
    CustomUser as User, 
)
from ..serializers.criteria_version_serializer import(
    CriteriaVersionSerializer,
)
from ..constants import(
    ResponseMessage,
    CriteriaVersionMessage,
    CRUDResponseMessage,
    MESSAGE,
    DATA,
)
from ..utils import(
    check_state,
    check_permission,
)

class CriteriaVersionView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        if not check_permission(
            username=request.user,
            action="can_read_criteria_settings",
            permission_is="Criteria",
    ):
            return Response(
                {MESSAGE: ResponseMessage.DO_NOT_HAVE_PERMISSION},
                status=status.HTTP_403_FORBIDDEN,
        ) 
            
        version_name=kwargs.get("version_name")
        
        if version_name:
            get_version=self.get_criteria_version(version_name)
            return(get_version)
            
        else:
            all_version=self.all_criteria_version(request)
            return (all_version)
        
    def get_criteria_version(self, version_name):
        try:
            criteria_version=CriteriaVersion.objects.get(version_name=version_name)
            serializer=CriteriaVersionSerializer(criteria_version)
            return Response(serializer.data, status=status.HTTP_200_OK) 
        
        except PermissionDenied as p:
            return Response(
                {MESSAGE: str(p)}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
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
            criteria_versions=CriteriaVersion.objects.all()
            if len(criteria_versions)<1:
                return Response(
                    {MESSAGE:CriteriaVersionMessage.OBJECT_HAS_NO_VALUE},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            role_name=request.query_params.get("role_name")
            state=request.query_params.get("state")
            
            if role_name and state:
                criteria_versions=criteria_versions.filter(
                    role_name__exact=role_name, state__exact=state  
                )
                
            elif role_name:
                criteria_versions=criteria_versions.filter(
                    role_name__exact=role_name
                )
                
            elif state:
                criteria_versions=criteria_versions.filter(state__exact=state)
                
            serializer=CriteriaVersionSerializer(criteria_versions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except PermissionDenied as p:
            return Response(
                {MESSAGE: str(p)}, 
                status=status.HTTP_403_FORBIDDEN
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
    def post(self, request):
        try:
            if not check_permission(
            username=request.user,
            action="can_write_criteria_setting",
            permission_is="Criteria",
        ):
                return Response(
                {MESSAGE: ResponseMessage.DO_NOT_HAVE_PERMISSION},
                status=status.HTTP_403_FORBIDDEN,
            ) 
            
            serializer = CriteriaVersionSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                criteria_version = CriteriaVersion(
                        version_name=serializer.validated_data["version_name"],
                        role_name=serializer.validated_data["role_name"],
                        created_user=request.user,
                        updated_user=None,
                    )
                criteria_version.save()
                response=CriteriaVersionSerializer(criteria_version).data
                
                return Response({
                        MESSAGE:CRUDResponseMessage.CREATE_SUCCESSFULLY, 
                        DATA:response,
                    },
                    status=status.HTTP_201_CREATED
                )
                
        except PermissionDenied as p:
            return Response(
                {MESSAGE: str(p)}, 
                status=status.HTTP_403_FORBIDDEN
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
            if not check_permission(
            username=request.user,
            action="can_write_criteria_setting",
            permission_is="Criteria",
        ):
                return Response(
                {MESSAGE: ResponseMessage.DO_NOT_HAVE_PERMISSION},
                status=status.HTTP_403_FORBIDDEN,
            )
            user=request.user
            version_name=kwargs.get("version_name")
            instance=CriteriaVersion.objects.get(version_name=version_name)
            
            serializer = CriteriaVersionSerializer(
                instance, 
                data=request.data, 
                context={"request": request}, 
                partial=True
            )
            
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
                
                serializer.save(updated_user=user)
                return Response({
                        MESSAGE:CRUDResponseMessage.UPDATE_SUCCESSFULLY,
                        DATA:serializer.data
                    }, 
                    status=status.HTTP_200_OK
                )
        
        except PermissionDenied as p:
            return Response(
                {MESSAGE: str(p)}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
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
            
    @transaction.atomic   
    def delete(self, request, *args, **kwargs):
        try: 
            if not check_permission(
            username=request.user,
            action="can_write_criteria_setting",
            permission_is="Criteria",
        ):
                return Response(
                {MESSAGE: ResponseMessage.DO_NOT_HAVE_PERMISSION},
                status=status.HTTP_403_FORBIDDEN,
            )
            version_name=kwargs.get("version_name")
            instance=CriteriaVersion.objects.get(version_name=version_name)
            instance.delete()
            
            return Response(
                {MESSAGE:CRUDResponseMessage.DELETE_SUCCESSFULLY}, 
                status=status.HTTP_200_OK
            )
        
        except PermissionDenied as p:
            return Response(
                {MESSAGE: str(p)}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        except CriteriaVersion.DoesNotExist:
            return Response(
                {MESSAGE: CriteriaVersionMessage.INVALID_VERSION},
                status=status.HTTP_404_NOT_FOUND
            )
            
        except Exception as e:
            return Response(
                {MESSAGE: str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )