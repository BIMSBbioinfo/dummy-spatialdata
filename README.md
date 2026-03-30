# dummy-spatialdata

Allows generating dummy spatialdata objects, which can be useful for testing purposes.

## Installation

TODO

## Example usage
```{python}
import spatialdata as ad
import dummy_spatialdata as ds

sdata = ds.generate_dataset(
    images = [
        {"type": "rgb", "n_layers": 4},
        {"type": "grayscale", "n_layers": 0}
    ]
)
sdata
```

```
SpatialData object
└── Images
      ├── 'image_0': DataTree[cyx] (3, 512, 768), (3, 256, 384), (3, 128, 192), (3, 64, 96), (3, 32, 48)
      └── 'image_1': DataTree[cyx] (1, 510, 510)
with coordinate systems:
    ▸ 'global', with elements:
        image_0 (Images), image_1 (Images)
```