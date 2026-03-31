import os
import sys
import numpy as np

from pathlib import Path
from importlib.resources import files, as_file
from PIL import Image
from typing import Optional
from spatialdata.models import TableModel

def generate_tablemodel(
    input: Optional[dict] = None,
) -> TableModel:

    if input is None:
        return None

    # link 
    print(input)
    region = input["instances_element"] + "_" + str(input["instance_element_index"])
    input["table"].obs['instance_id'] =  input["table"].obs.index
    input["table"].obs['region'] = region
    input["table"].uns["spatialdata_attrs"] = {
        "region": region,
        "region_key": "region",
        "instance_key": "instance_id",
    }

    return TableModel.parse(input["table"])