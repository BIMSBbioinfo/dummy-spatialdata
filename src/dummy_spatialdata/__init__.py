from importlib.metadata import version

from .generate_dataset import generate_dataset
from .generate_imagemodel import generate_imagemodel
from .generate_labelmodel import generate_labelmodel
from .generate_shapemodel import generate_shapemodel
from .generate_tablemodel import generate_tablemodel

__all__ = [
    "generate_dataset",
    "generate_imagemodel",
    "generate_labelmodel"
]

__version__ = version("dummy-spatialdata")