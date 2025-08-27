from __future__ import annotations

import io
from typing import Any, Optional

import boto3
import xarray as xr
from botocore import UNSIGNED, exceptions as boto_exc
from botocore.config import Config


def stream_netcdf(
    bucket: str,
    key: str,
    *,
    group: Optional[str] = None,
    engine: Optional[str] = None,
    chunks: Any | None = None,
) -> xr.Dataset:
    """Stream a NetCDF file from a *public* S3 bucket and return an ``xarray.Dataset``.

    Parameters
    ----------
    bucket : str
        S3 bucket name (e.g., "meeo-s5p").
    key : str
        Object key path to the NetCDF file within the bucket.
    group : str, optional
        HDF5/NetCDF group to open. ``None`` opens the root group.
    engine : str, optional
        Backend engine passed to :func:`xarray.open_dataset`.
    chunks : Any, optional
        Chunking argument forwarded to :func:`xarray.open_dataset`.

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
        body = obj["Body"].read()
        buffer = io.BytesIO(body)
        buffer.seek(0)
        ds = xr.open_dataset(buffer, engine=engine, group=group, chunks=chunks)
        return ds
    except Exception as e:
        raise RuntimeError(
            f"Failed to open NetCDF (group='{group}', engine='{engine}'): {e}"
        ) from e
