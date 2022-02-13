import logging

from rich.console import Console
from rich.logging import RichHandler

from .packages import packages


console = Console()
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(markup=True, rich_tracebacks=True)],
)
log = logging.getLogger(__name__)


__all__ = ["packages"]
