import logging

from rich.console import Console
from rich.logging import RichHandler

from . import paper, purpur, vanilla, velocity, waterfall


console = Console()
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(markup=True, rich_tracebacks=True)],
)
log = logging.getLogger(__name__)


pkgs = {
    "paper": paper,
    "purpur": purpur,
    "vanilla": vanilla,
    "velocity": velocity,
    "waterfall": waterfall,
}
