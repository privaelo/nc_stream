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

The library can stream any public NetCDF file. One possible dataset is the Sentinel-5P Near Real Time CO product hosted on AWS.

```python
from nc_stream import stream_netcdf

bucket = "meeo-s5p"
key = "NRTI/L2__CO____/2023/08/01/S5P_NRTI_L2__CO_____20230801T230402_20230801T230902_30057_03_020500_20230802T000504.nc"
#group = "/PRODUCT"
#engine="h5netcdf"

ds = stream_netcdf(bucket, key)
print(ds)
```
# Acknowledgements
Thanks to the [AWS Open Data initiative](https://registry.opendata.aws/) and the open-source community behind `xarray`, `fsspec`, and `s3fs`.

## Sentinel-5P License
https://sentinel.esa.int/documents/247904/690755/Sentinel_Data_Legal_Notice

## Sentinel-5P Documentation
https://github.com/Sentinel-5P/data-on-s3/blob/master/DocsForAws/Sentinel5P_Description.md

---
