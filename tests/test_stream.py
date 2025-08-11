import os
import pytest
import xarray as xr
from nc_stream.stream import stream_netcdf

@pytest.mark.integration
def test_stream_netcdf_integration():
    bucket = "meeo-s5p"
    key = "NRTI/L2__CO____/2023/08/01/S5P_NRTI_L2__CO_____20230801T230402_20230801T230902_30057_03_020500_20230802T000504.nc"

    ds = stream_netcdf(bucket, key)
    assert isinstance(ds, xr.Dataset)
    # Keep assertions resilient across minor product changes
    assert len(ds.data_vars) > 0
    assert len(ds.coords) >= 1
    assert "latitude" in ds
    assert "longitude" in ds
    assert "carbonmonoxide_total_column" in ds

def test_stream_netcdf_param_validation():
    with pytest.raises(ValueError):
        stream_netcdf("", "file.nc")
    with pytest.raises(ValueError):
        stream_netcdf("bucket", "")
    with pytest.raises(ValueError):
        stream_netcdf("bucket", "not_netcdf.txt")