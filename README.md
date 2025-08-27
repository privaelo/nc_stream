# nc_stream

Stream `.nc` files directly from public S3 buckets without downloading them.

##  Features

- Stream NetCDF `.nc` files from **any public S3 bucket**
- Returns an **xarray.Dataset** without downloading data locally
- Optional parameters for `engine`, `group`, and `storage_options`
- Built-in support for **Sentinel-5P NRTI CO** (Near Real time) datasets
- Easily extensible for filtering, export, or transformation

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
    engine="netcdf4",   # optional: choose xarray backend
    group=None,          # optional: open a specific group within the file
    storage_options={"anon": True},  # optional: S3 filesystem options
)
print(ds)
```

### Real-world Example: Sentinel-5P NRTI CO

```python
from nc_stream import stream_netcdf

bucket = "meeo-s5p"
key = "NRTI/L2__CO____/2023/08/01/S5P_NRTI_L2__CO_____20230801T230402_20230801T230902_30057_03_020500_20230802T000504.nc"

ds = stream_netcdf(bucket, key)
print(ds)
```
# Acknowledgements
This package streams Sentinel-5P data hosted by MEEO via the AWS Open Data Registry, in support of the European Space Agency's Copernicus Programme.
## License
https://sentinel.esa.int/documents/247904/690755/Sentinel_Data_Legal_Notice
## Documentation
https://github.com/Sentinel-5P/data-on-s3/blob/master/DocsForAws/Sentinel5P_Description.md

---
