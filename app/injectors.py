from typing import Dict
from .config import Config

def inject_config_variables_into_templates() -> Dict:
    """
    Inject global variables into all templates.
    """
    return {"config": Config}