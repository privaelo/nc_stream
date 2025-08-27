import io
import socket

import boto3
import pytest
import xarray as xr
from botocore.response import StreamingBody
from botocore.stub import Stubber

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from nc_stream.stream import stream_netcdf


@pytest.fixture
def s3_netcdf(monkeypatch):
    ds = xr.Dataset({"data": ("x", [1, 2, 3])})
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".nc") as tmp:
        ds.to_netcdf(tmp.name, engine="h5netcdf")
        tmp.seek(0)
        data = tmp.read()

    client = boto3.client("s3", region_name="us-east-1")
    stubber = Stubber(client)
    response = {"Body": StreamingBody(io.BytesIO(data), len(data))}
    params = {"Bucket": "test-bucket", "Key": "test.nc"}
    stubber.add_response("get_object", response, params)
    stubber.activate()
    monkeypatch.setattr(boto3, "client", lambda *a, **k: client)

    yield ds, "test-bucket", "test.nc"

    stubber.deactivate()


def test_open_without_group_or_engine(s3_netcdf):
    expected, bucket, key = s3_netcdf
    ds = stream_netcdf(bucket, key)
    xr.testing.assert_identical(ds, expected)


def test_custom_engine_group_chunks(s3_netcdf):
    pytest.importorskip("dask.array")
    _, bucket, key = s3_netcdf
    ds = stream_netcdf(bucket, key, engine="h5netcdf", group=None, chunks={"x": 1})
    assert ds["data"].data.chunks[0][0] == 1


def test_unsupported_extension():
    with pytest.raises(ValueError):
        stream_netcdf("bucket", "file.txt")


def _has_network() -> bool:
    try:
        socket.create_connection(("example.com", 80), timeout=1)
        return True
    except OSError:
        return False


@pytest.mark.integration
@pytest.mark.skipif(not _has_network(), reason="requires network access")
def test_stream_netcdf_integration():
    bucket = "meeo-s5p"
    key = (
        "NRTI/L2__CO____/2023/08/01/"
        "S5P_NRTI_L2__CO_____20230801T230402_20230801T230902_30057_03_020500_20230802T000504.nc"
    )

    ds = stream_netcdf(bucket, key, engine="h5netcdf", group="/PRODUCT")
    assert isinstance(ds, xr.Dataset)
    assert len(ds.data_vars) > 0
    assert len(ds.coords) >= 1
    assert "latitude" in ds
    assert "longitude" in ds
    assert "carbonmonoxide_total_column" in ds


def test_param_validation():
    with pytest.raises(ValueError):
        stream_netcdf("", "file.nc")
    with pytest.raises(ValueError):
        stream_netcdf("bucket", "")
