# nc_stream

Stream `.nc` files directly from public S3 storage without downloading them.

## Features

- Stream **any** NetCDF `.nc` object from public S3 buckets
- Customize `engine`, `group`, and `storage_options`
- Returns **xarray.Dataset** for easy geospatial processing
- Built-in support for **Sentinel-5P NRTI CO** (Near Real time) datasets
- Easily extensible for filtering, export, or transformation

##  Installation

```bash
  pip install -e .
  ```

## Example Usage

### Generic S3 NetCDF object

```python
from nc_stream import stream_netcdf

ds = stream_netcdf(
    bucket="my-public-bucket",
    key="path/to/data.nc",
    engine="netcdf4",
    group="/subgroup",
    storage_options={"region_name": "us-west-2"},
)
print(ds)
```

### Streaming Sentinel-5P data

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
