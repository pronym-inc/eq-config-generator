from typing import Dict

from roles import Role


class AssistHealerRole(Role):
    def get_bureau_config(self) -> Dict[str, str]:
        return {
            'AssistAndHealOn': "Yes"
        }
