# nc_stream

Stream `.nc` files directly from public S3 buckets without downloading them.

##  Features

- Stream NetCDF `.nc` files from **any public S3 bucket**
- Returns an **xarray.Dataset** without downloading data locally
- Optional parameters for `engine`, `group`, and `storage_options`
- Easily extensible for filtering, export, or transformation
- Powered by open-source tools like `xarray`, `fsspec`, and `s3fs`

##  Installation

```bash
  pip install -e .
  ```

##  Usage

```python
from nc_stream import stream_netcdf

bucket = "my-public-bucket"
key = "path/to/file.nc"

ds = stream_netcdf(
    bucket,
    key,
    engine="h5netcdf",   # optional: choose xarray backend
    group=None,          # optional: open a specific group within the file
    storage_options={"anon": True},  # optional: S3 filesystem options
)
print(ds)
```

### Example: Sentinel-5P NRTI CO dataset

This example streams a Sentinel-5P Near Real Time CO product hosted on AWS. It requires `numpy` and `xarray` and filters out pixels with a low quality assurance (QA) score.

```python
import numpy as np
import xarray as xr
from nc_stream import stream_netcdf

def fetch_filtered_co():
    bucket = "meeo-s5p"
    key = "NRTI/L2__CO____/2023/08/01/S5P_NRTI_L2__CO_____20230801T230402_20230801T230902_30057_03_020500_20230802T000504.nc"

    ds = stream_netcdf(
        bucket,
        key,
        group="/PRODUCT",
        engine="h5netcdf",
        storage_options={"anon": True},
    )

    co = ds["carbonmonoxide_total_column"]
    qa = ds["qa_value"]

    filtered = co.where(qa > 0.5)
    print(filtered.values)
    return filtered.values
```

The QA threshold of `0.5` discards retrievals flagged as low quality, retaining only the more reliable measurements.
# Acknowledgements
Thanks to the [AWS Open Data initiative](https://registry.opendata.aws/) and the open-source community behind `xarray`, `fsspec`, and `s3fs`.

## Sentinel-5P License
https://sentinel.esa.int/documents/247904/690755/Sentinel_Data_Legal_Notice

## Sentinel-5P Documentation
https://github.com/Sentinel-5P/data-on-s3/blob/master/DocsForAws/Sentinel5P_Description.md

---
