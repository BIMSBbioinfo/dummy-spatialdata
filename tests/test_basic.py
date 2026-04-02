import dummy_spatialdata
import pytest

def test_package_has_version():
    assert dummy_spatialdata.__version__ is not None

# This test test whether or not all the functions in the package
# work.
def test_generating_dataset(tmp_path):
    dummy = dummy_spatialdata.generate_dataset()
    # filename = tmp_path / "dummy.h5ad"
    # dummy.write_h5ad(filename)

