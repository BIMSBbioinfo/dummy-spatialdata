# dummy-spatialdata

Allows generating dummy spatialdata objects, which can be useful for testing purposes.

## Installation

```bash
pip install dummy-spatialdata
```

## Example usage
```{python}
from dummy_spatialdata import generate_dataset
import dummy_anndata
import spatialdata_plot as sdp 
import spatialdata as sd
import matplotlib.pyplot as plt
import anndata as ad

# generate dummy anndata
adata = dummy_anndata.generate_dataset(n_obs=12, n_vars=20)

# generate dummy spatialdata
sdata = generate_dataset(
    images = [
        {"type": "rgb", "n_layers": 4, "shape": {"x": 1000, "y": 1000}, "transformations": {"trans_0": ["affine"]}},
        {"type": "grayscale", "n_layers": 1, "shape": {"x": 1000, "y": 1000}, "transformations": {"trans_0": ["affine"]}},
    ],
    labels = [
        {"n_labels": 12, "n_layers": 4, "shape": {"x": 1000, "y": 1000}},
        {"n_labels": 12, "n_layers": 0, "shape": {"x": 100, "y": 100}},
    ], 
    shapes = [
        {"n_shapes": 12, "shape": {"x": 1000, "y": 1000}},
        {"n_shapes": 20, "shape": {"x": 1000, "y": 1000}},
    ],
    tables = [
        {"table": adata, "element": "shape", "element_index": 0}
    ],
    SEED=13
)
sdata
```

```
SpatialData object
├── Images
│     ├── 'image_0': DataTree[cyx] (3, 1000, 1000), (3, 500, 500), (3, 250, 250), (3, 125, 125)
│     └── 'image_1': DataTree[cyx] (1, 1000, 1000)
├── Labels
│     ├── 'label_0': DataTree[yx] (1000, 1000), (500, 500), (250, 250), (125, 125)
│     └── 'label_1': DataTree[yx] (100, 100)
├── Shapes
│     ├── 'shape_0': GeoDataFrame shape: (12, 1) (2D shapes)
│     └── 'shape_1': GeoDataFrame shape: (20, 1) (2D shapes)
└── Tables
      └── 'table_0': AnnData (12, 20)
with coordinate systems:
    ▸ 'global', with elements:
        image_0 (Images), image_1 (Images), label_0 (Labels), label_1 (Labels), shape_0 (Shapes), shape_1 (Shapes)
    ▸ 'trans_0', with elements:
        image_0 (Images), image_1 (Images)
```

```{python}
fig, axs = plt.subplots(1, 2, figsize=(12, 5))
sdata.pl.render_images("image_0").pl.render_shapes("shape_0", color="Gene001", table_name = "table_0", table_layer = "float_matrix").pl.show(ax=axs[0], coordinate_systems = "global")
```