import os
import socket
from contextlib import closing

import boto3
import pytest
import xarray as xr

pytest.importorskip("fsspec")
from nc_stream.stream import stream_netcdf

moto = pytest.importorskip("moto")
mock_s3 = moto.mock_s3


def _has_network() -> bool:
    """Return True if network access is available."""
    try:
        with closing(socket.create_connection(("meeo-s5p.s3.amazonaws.com", 443), timeout=1)):
            return True
    except OSError:
        return False


@pytest.fixture
def s3_netcdf(tmp_path):
    os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
    os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")
    bucket = "test-bucket"
    key = "data/test.nc"

    with mock_s3():
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=bucket)

        # Create a file with data in the root and a subgroup
        ds_root = xr.Dataset({"a": ("x", [1, 2])}, coords={"x": [0, 1]})
        path = tmp_path / "test.nc"
        ds_root.to_netcdf(path)

        ds_group = xr.Dataset({"b": ("y", [3, 4, 5])}, coords={"y": [0, 1, 2]})
        ds_group.to_netcdf(path, group="sub", mode="a")

        with open(path, "rb") as f:
            s3.upload_fileobj(f, bucket, key)

        yield bucket, key


@pytest.mark.integration
@pytest.mark.skipif(not _has_network(), reason="Network unavailable")
def test_stream_netcdf_integration():
    bucket = "meeo-s5p"
    key = (
        "NRTI/L2__CO____/2023/08/01/"
        "S5P_NRTI_L2__CO_____20230801T230402_20230801T230902_30057_03_020500_20230802T000504.nc"
    )

    ds = stream_netcdf(bucket, key, storage_options={"anon": True})
    assert isinstance(ds, xr.Dataset)
    assert len(ds.data_vars) > 0
    assert len(ds.coords) >= 1
    assert "latitude" in ds
    assert "longitude" in ds
    assert "carbonmonoxide_total_column" in ds


def test_stream_netcdf_default_params(s3_netcdf):
    bucket, key = s3_netcdf
    ds = stream_netcdf(bucket, key)
    assert list(ds.data_vars) == ["a"]
    assert ds["a"].data.tolist() == [1, 2]


def test_stream_netcdf_custom_options(s3_netcdf):
    bucket, key = s3_netcdf
    ds = stream_netcdf(
        bucket,
        key,
        engine="h5netcdf",
        group="sub",
        chunks={"y": 2},
    )
    assert list(ds.data_vars) == ["b"]
    assert ds.chunks["y"] == (2, 1)


def test_stream_netcdf_unsupported_extension():
    with pytest.raises(ValueError):
        stream_netcdf("bucket", "file.txt")


def test_stream_netcdf_param_validation():
    with pytest.raises(ValueError):
        stream_netcdf("", "file.nc")
    with pytest.raises(ValueError):
        stream_netcdf("bucket", "")

