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
    """
    API endpoint for managing Criteria Version data.

    This view supports the following operations:
    - Retrieve a single or all criteria versions (GET)
    - Create a new criteria version (POST)
    - Partially update an existing criteria version (PATCH)
    - Delete a criteria version (DELETE)

    Permissions are required for each action. All operations are performed 
    with proper error handling and transactional safety.
    """
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to retrieve a specific version or all versions of Criteria.

        Args:
            request (Request): The incoming HTTP request.
            version_name (str, optional): Name of the version to retrieve.

        Returns:
            Response: Serialized data or error message with HTTP status code.
        """
        
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
        """
        Retrieve a specific Criteria version by version name.

        Args:
            version_name (str): The version name to retrieve.

        Returns:
            Response: Serialized data or appropriate error response.
        """
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
        """
        Retrieve all Criteria versions, with optional filtering by role name and state.

        Args:
            request (Request): The incoming HTTP request with optional query parameters.

        Returns:
            Response: List of serialized data or appropriate error response.
        """
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
        """
        Handle POST request to create a new CriteriaVersion record.

        This method performs the following steps:
        - Checks user permission for writing criteria settings.
        - Validates the incoming data using the serializer.
        - Creates and saves a new CriteriaVersion instance.
        - Returns a success response with the created data.

        Args:
            request (Request): The incoming HTTP request with new version data.

        Returns:
            Response: 
                - 201 Created if creation is successful.
                - 400 Bad Request if validation fails.
                - 403 Forbidden if user lacks permission.
                - 500 Internal Server Error for unexpected issues.
        """
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
                        **serializer.data,
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
        """
        Handle PATCH request to partially update a CriteriaVersion instance.

        This method performs the following:
        - Checks user permission to update criteria settings.
        - Retrieves the existing CriteriaVersion instance by `version_name`.
        - Validates the update data using the serializer (partial update).
        - Checks if the state transition is valid using `check_state`.
        - Saves the updated instance with the current user as `updated_user`.

        Args:
            request (Request): The incoming HTTP request containing update data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments, expected to contain 'version_name'.

        Returns:
            Response:
                - 200 OK if update is successful.
                - 400 Bad Request if validation or state check fails.
                - 403 Forbidden if user lacks permission.
                - 404 Not Found if the CriteriaVersion does not exist.
                - 500 Internal Server Error for unexpected exceptions.
        """
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
                {MESSAGE: str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    @transaction.atomic   
    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE request to remove a CriteriaVersion instance.

        This method performs the following:
        - Checks if the user has permission to delete criteria settings.
        - Retrieves the CriteriaVersion object based on `version_name`.
        - Deletes the instance from the database.

        Args:
            request (Request): The incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Expected to contain 'version_name' to identify the object.

        Returns:
            Response:
                - 200 OK if the object is successfully deleted.
                - 403 Forbidden if the user lacks proper permissions.
                - 404 Not Found if the specified CriteriaVersion does not exist.
                - 500 Internal Server Error for unexpected exceptions.
        """
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
                {MESSAGE: str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )