from django.core.exceptions import PermissionDenied
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from ..models import (
    InputType
)

from ..serializers.input_type_serializer import (
    InputTypeSerializer
)

from ..constants import (
    ResponseMessage,
    CRUDResponseMessage,
    MESSAGE,
    DATA,
)

from ..utils import (
    check_permission
)

class InputTypeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if check_permission(
                username=request.user,
                action="can_read_criteria_setting",
                permission_is="criteria",
            ):
                input_types = InputType.objects.all()

                serializer = InputTypeSerializer(set(input_types), many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(
                {MESSAGE: ResponseMessage.DO_NOT_HAVE_PERMISSION},
                status=status.HTTP_403_FORBIDDEN,
            )

        except PermissionDenied as e:
            return Response(
                {MESSAGE: str(e)},
                status=status.HTTP_403_FORBIDDEN
            )

        except InputType.DoesNotExist:
            return Response(
                {MESSAGE: ResponseMessage.DATA_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response(
                {MESSAGE: str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def post(self, request):

        try:
            if check_permission(
                username=request.user,
                action="can_write_criteria_setting",
                permission_is="criteria",
            ):
                serializer = InputTypeSerializer(data=request.data)

                if serializer.is_valid(raise_exception=True):

                    input_type = InputType(
                        name=serializer.validated_data["name"],
                        min=serializer.validated_data["min"],
                        max=serializer.validated_data["max"],
                    )
                    input_type.save()
                    serializer_response = InputTypeSerializer(input_type).data

                    return Response(serializer_response, status=status.HTTP_201_CREATED)

            return Response(
                {MESSAGE: ResponseMessage.DO_NOT_HAVE_PERMISSION},
                status=status.HTTP_403_FORBIDDEN,
            )

        except PermissionDenied as e:
            return Response({MESSAGE: str(e)}, status=status.HTTP_403_FORBIDDEN)

        except ValidationError as ve:
            return Response({MESSAGE: ve.detail}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {MESSAGE: str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @transaction.atomic
    def put(self, request, *args, **kwargs):

        try:
            if check_permission(
                username=request.user,
                action="can_write_criteria_setting",
                permission_is="criteria",
            ):
                
                input_type = kwargs.get("id")
                instance = InputType.objects.get(id=input_type)
                serializer = InputTypeSerializer(
                    instance,
                    data=request.data,
                    partial=True
                )

                if serializer.is_valid(raise_exception=True):
                    serializer.save()

                    return Response({
                        MESSAGE: CRUDResponseMessage.UPDATE_SUCCESSFULLY,
                        DATA: serializer.data
                    }, status=status.HTTP_200_OK)

            return Response(
                {MESSAGE: ResponseMessage.DO_NOT_HAVE_PERMISSION},
                status=status.HTTP_403_FORBIDDEN,
            )

        except PermissionDenied as e:
            return Response({MESSAGE: str(e)}, status=status.HTTP_403_FORBIDDEN)

        except InputType.DoesNotExist:
            return Response(
                {MESSAGE: ResponseMessage.DATA_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND,
            )

        except ValidationError as ve:
            return Response({MESSAGE: ve.detail}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {MESSAGE: str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # Will be used when there is a Criteria table.
    
    # def delete(self, request, id):

    #     try:
    #         if check_permission(
    #             username=request.user,
    #             action="can_write_criteria_setting",
    #             permission_is="criteria",
    #         ):

    #             input_type = InputType.objects.get(id=id)
    #             input_type_being_used = Criteria.objects.filter(input_type=input_type)

    #             message = None

    #             if input_type_being_used.exists():
    #                 message = (
    #                     f"Warning: InputType is currently being used in "
    #                     f"{input_type_being_used.count()} Criteria entries."
    #                 )

    #             input_type.delete()
    #             response_message = {MESSAGE: InputTypeMessage.INPUT_TYPE_DELETED_SUCCESSFULLY}
                
    #             if message:
    #                 response_message["warning"] = message

    #             return Response(response_message, status=status.HTTP_200_OK)

    #         return Response(
    #             {MESSAGE: ResponseMessage.DO_NOT_HAVE_PERMISSION},
    #             status=status.HTTP_403_FORBIDDEN,
    #         )

    #     except PermissionDenied as e:
    #         return Response({MESSAGE: str(e)}, status=status.HTTP_403_FORBIDDEN)

    #     except InputType.DoesNotExist:
    #         return Response(
    #             {MESSAGE: ResponseMessage.DATA_NOT_FOUND},
    #             status=status.HTTP_404_NOT_FOUND,
    #         )

    #     except Exception as e:
    #         return Response(
    #             {MESSAGE: str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )