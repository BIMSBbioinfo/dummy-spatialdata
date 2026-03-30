from importlib.metadata import version

from .generate_dataset import generate_dataset

__all__ = [
    "generate_dataset",
]

__version__ = version("dummy-spatialdata")