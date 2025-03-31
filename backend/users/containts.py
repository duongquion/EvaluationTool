class SuccessMessage():
    LOGIN_SUCCESSFULLY = 'Login successfully'
    CHANGE_PASSWORD_SUCCESSFULLY = 'Change password successfully'
    RESET_PASSWORD_SUCCESSFULLY = 'Reset password successfully'

class ErrorMessage():
    USER_NOT_ALLOWED = 'User not allowed to do it'
    INCORRECT_USERNAME_PASSWORD = 'Username or password is incorrect'
    THE_ANSWER_DOES_NOT_MATCH = 'The answer does not match'
    PASSWORD_HAS_BEEN_CHANGED = 'Password has been changed'
    PASSWORD_HAS_NOT_BEEN_CHANGED = 'Password has not been changed'
    NOT_PART_OF_ANY_TEAM = 'User is not part of any team'
    TEAM_NOT_FOUND = 'Team not found'
    AUTHENTICATION_REQUIRED='Authentication required'
    
class AlertMessage():
    UNSUCCESS_FOR_ADD_NEW_EMPLOYEE="Employees must be away from their old team for at least 90 days before joining a new team"