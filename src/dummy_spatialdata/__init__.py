from importlib.metadata import version

from .generate_dataset import generate_dataset
from .generate_imagemodel import generate_imagemodel
from .generate_labelmodel import generate_labelmodel
from .generate_shapemodel import generate_shapemodel
from .generate_pointmodel import generate_pointmodel
from .generate_tablemodel import generate_tablemodel
from .generate_transformations import (
    generate_transformations,
    get_basetransformations,
    get_shape
)
from .utils import default_shape

__all__ = [
    "generate_dataset",
    "generate_imagemodel",
    "generate_labelmodel",
    "generate_shapemodel",
    "generate_pointmodel"
    "generate_tablemodel",
    "generate_transformations",
    "utils"
]

__version__ = version("dummy-spatialdata")