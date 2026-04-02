import os
import sys
import numpy as np

from importlib.resources import files, as_file
from typing import Optional
from spatialdata.models import ShapesModel
from spatialdata.transformations import set_transformation, Identity
import geopandas as gpd
from shapely.geometry import Polygon
from .generate_transformations import generate_transformations

def generate_shapemodel(
    input: Optional[dict] = None,
    key: Optional[str] = None,
    transformations: Optional[dict] = None,
    SEED: Optional[int] = 42
) -> ShapesModel:

    if input is None:
        return None

    # generate polygons
    RADIUS = 0.08 * min(input["shape"]["x"], input["shape"]["y"])
    MIN_GAP = 0.01 * min(input["shape"]["x"], input["shape"]["y"])

    centers = generate_non_overlapping_centers(input["shape"]["x"], input["shape"]["y"], RADIUS, input["n_shapes"], MIN_GAP, SEED)
    polygon_seeds = [SEED + i for i in range(input["n_shapes"])]
    polygons = [Polygon(border_polygon_points(c, RADIUS, 10, SEED = seed)) for c, seed in zip(centers, polygon_seeds)]
    gdf = gpd.GeoDataFrame(geometry=polygons)

    # get transformations
    if "transformations" in input:
        if input["transformations"] in transformations:
            trans = {input["transformations"]: transformations[input["transformations"]]}
        else: 
            trans = {key: Identity()}
    else:
        trans = {key: Identity()}

    # shape model
    shapemodel = ShapesModel.parse(gdf, 
                                   transformations = trans)
    
    return shapemodel

def circles_overlap(c1, c2, radius, min_gap=0.0):
    x1, y1 = c1
    x2, y2 = c2
    return np.hypot(x2 - x1, y2 - y1) < (2 * radius + min_gap)

def generate_non_overlapping_centers(width, height, radius, n_circles, min_gap=0.15, SEED=1, max_tries=10000):
    centers = []
    tries = 0
    rng = np.random.default_rng(SEED)

    while len(centers) < n_circles and tries < max_tries:
        tries += 1
        x = rng.uniform(radius, width - radius)
        y = rng.uniform(radius, height - radius)
        candidate = (x, y)

        if all(not circles_overlap(candidate, c, radius, min_gap=min_gap) for c in centers):
            centers.append(candidate)

    if len(centers) < n_circles:
        raise RuntimeError(f"Could only place {len(centers)} circles after {max_tries} attempts.")

    return np.array(centers)

def border_polygon_points(center, radius, n_points, SEED=1):
    cx, cy = center
    rng = np.random.default_rng(SEED)

    # Random angles around the border
    angles = np.sort(rng.uniform(0, 2 * np.pi, n_points))

    # Points exactly on the circle border
    xs = cx + radius * np.cos(angles)
    ys = cy + radius * np.sin(angles)

    return np.column_stack([xs, ys])