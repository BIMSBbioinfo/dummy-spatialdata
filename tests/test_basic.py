import dummy_spatialdata
import spatialdata as sd
import pytest
import tempfile as tf

def test_package_has_version():
    assert dummy_spatialdata.__version__ is not None

def test_generating_empty():
    dummy = dummy_spatialdata.generate_dataset()
    filename = tf.NamedTemporaryFile()
    dummy.write(filename.name + '.zarr')

    # read back
    sdata = sd.read_zarr(filename.name + '.zarr')

def test_generating_singleelement():
    dummy = dummy_spatialdata.generate_dataset(
        points = [
            {'n': 12}
        ],
        SEED=13
    )
    filename = tf.NamedTemporaryFile()
    dummy.write(filename.name + '.zarr')

    # read back
    sdata = sd.read_zarr(filename.name + '.zarr')