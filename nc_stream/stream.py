from __future__ import annotations
import io
from typing import Optional, Dict

import boto3
import xarray as xr
from botocore import UNSIGNED, exceptions as boto_exc
from botocore.config import Config

def stream_netcdf(
    bucket: str,
    key: str,
    group: str = "/PRODUCT",
    *,
    engine: Optional[str] = None,
    storage_options: Optional[Dict[str, str]] = None,
) -> xr.Dataset:
    """
    Stream a NetCDF file from a *public* S3 bucket and return an xarray.Dataset.

    Parameters
    ----------
    bucket : str
        S3 bucket name (e.g., "meeo-s5p").
    key : str
        Object key path to the .nc file within the bucket.
    group : str, default "/PRODUCT"
        HDF5/NetCDF group to open.
    engine : str, optional
        xarray backend engine to use. Defaults to ``"h5netcdf"``.
    storage_options : dict[str, str], optional
        Additional storage options (currently unused).

    Returns
    -------
    xr.Dataset
        The opened dataset.

    Raises
    ------
    ValueError
        If parameters are invalid.
    FileNotFoundError
        If the object does not exist.
    RuntimeError
        For other streaming/opening errors.
    """
    if not bucket or not key:
        raise ValueError("Both 'bucket' and 'key' are required.")
    if not key.endswith(".nc"):
        raise ValueError("Expected an .nc key (NetCDF).")

    try:
        s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        obj = s3.get_object(Bucket=bucket, Key=key)  # works for public objects
    except boto_exc.ClientError as e:
        code = e.response.get("Error", {}).get("Code", "Unknown")
        if code in {"NoSuchKey", "404"}:
            raise FileNotFoundError(f"S3 object not found: s3://{bucket}/{key}") from e
        raise RuntimeError(f"S3 get_object failed ({code}) for s3://{bucket}/{key}") from e
    except Exception as e:
        raise RuntimeError(f"S3 access failed for s3://{bucket}/{key}: {e}") from e

    try:
        # Read into memory; do NOT write to disk
        body = obj["Body"].read()
        buffer = io.BytesIO(body)
        buffer.seek(0)
        # Important: specify engine and group
        ds = xr.open_dataset(buffer, engine=engine or "h5netcdf", group=group)
        # Eagerly load metadata/coords so underlying stream can GC safely
        return ds
    except Exception as e:
        raise RuntimeError(f"Failed to open NetCDF (group='{group}'): {e}") from e
