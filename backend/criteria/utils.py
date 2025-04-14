from .constants import(
    INVALID_STATE
)
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