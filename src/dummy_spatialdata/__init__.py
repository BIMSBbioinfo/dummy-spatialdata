from importlib.metadata import version

from .generate_dataset import generate_dataset
from .generage_imagemodel import generate_imagemodel

__all__ = [
    "generate_dataset",
    "generate_imagemodel"
]

__version__ = version("dummy-spatialdata")