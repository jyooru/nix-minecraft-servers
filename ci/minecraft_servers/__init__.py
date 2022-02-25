import logging

from rich.logging import RichHandler

from . import paper, purpur, vanilla, velocity, waterfall


__all__ = [
    "paper",
    "purpur",
    "vanilla",
    "velocity",
    "waterfall",
]


logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(markup=True, rich_tracebacks=True)],
)
log = logging.getLogger(__name__)


packages = {package: globals()[package] for package in __all__}
