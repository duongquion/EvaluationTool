from .constants import(
    INVALID_STATE
)
from users.constants import(
    CheckPermissionMessage
)
from users.models import(
    CustomUser as User,
    Employee
)
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied

def check_state(
    state: str,
    model_name: str,
    new_state: str | None,
) -> bool:

    def check_state_for_criteria_verison():
        
        if state == "Unofficial" and new_state == "Outdated":
            return False
        elif state == "Official" and new_state == "Unofficial":
            return False
        elif state == "Outdated" and new_state in INVALID_STATE:
            return False
        return True

    if model_name == "Criteria Version":
        return check_state_for_criteria_verison()
    
def check_permission(
    username: str, 
    action: str, 
    permission_is: str
) -> bool:
    
    try:
        user = User.objects.get(username=username, is_active=True)
        
        if user.is_superuser:
            return True
        
        employee = Employee.objects.filter(user=user, is_active=True).first()
        
        if employee is None:   
            if user.is_staff:
                groups = user.groups.all()
                if not groups.exists():
                    raise PermissionDenied(_(CheckPermissionMessage.USER_NOT_PART_ANY_GROUP))
                for group in groups:
                    permissions = group.permissions.all()
                    for permission in permissions:
                        if permission_is in permission.name:
                            return True
                return False
            else:
                raise PermissionDenied(_(CheckPermissionMessage.EMPLOYEE_NOT_FOUND_OR_USER_NOT_PART_ANY_TEAM))
        
        if employee is not None:
            if action is not None:
                match action:
                    case "can_read_eval_data":
                        return employee.access_level.can_read_eval_data
                    case "can_write_eval_data":
                        return employee.access_level.can_write_eval_data
                    case "can_read_eval_setting":
                        return employee.access_level.can_read_eval_settings
                    case "can_write_eval_setting":
                        return employee.access_level.can_write_eval_settings
                    case "can_read_criteria_setting":
                        return employee.access_level.can_read_criteria_settings
                    case "can_write_criteria_setting":
                        return employee.access_level.can_write_criteria_settings
                    case "can_export":
                        return employee.access_level.can_export
                    case _:
                        raise Exception(_(CheckPermissionMessage.NO_ACTION_DEFINE))
            return False
      
    except User.DoesNotExist:
        raise PermissionDenied(_(CheckPermissionMessage.USER_NOT_FOUND))
       
    except Exception as e:
        raise PermissionDenied(str(e))