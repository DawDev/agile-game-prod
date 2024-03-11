from dataclasses import dataclass

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .config import Config
from .utils import Singleton


@dataclass
class Globals(metaclass=Singleton):
    DELTA_TIME: float = 0.0
    CONFIG: "Config" = None
    DEBUG: bool = False
    
