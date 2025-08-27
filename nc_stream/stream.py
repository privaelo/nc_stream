from __future__ import annotations

from typing import Any, Optional

import fsspec
import xarray as xr


def stream_netcdf(
    bucket: str,
    key: str,
    *,
    engine: str = "h5netcdf",
    group: str = "/PRODUCT",
    storage_options: Optional[dict[str, Any]] = None,
    chunks: Optional[Any] = None,
    **open_dataset_kwargs: Any,
) -> xr.Dataset:
    """
    Stream a NetCDF file from a *public* S3 bucket and return an ``xarray.Dataset``.

    Parameters
    ----------
    bucket : str
        S3 bucket name (e.g., ``"meeo-s5p"``).
    key : str
        Object key path to the NetCDF file (``.nc``, ``.nc4``, or ``.cdf``).
    engine : str, default "h5netcdf"
        Backend engine to pass to :func:`xarray.open_dataset`.
    group : str, default "/PRODUCT"
        HDF5/NetCDF group to open.
    storage_options : dict, optional
        ``fsspec`` storage options for S3 access.
    chunks : dict or int, optional
        Dask chunking passed to :func:`xarray.open_dataset`.
    **open_dataset_kwargs
        Additional keyword arguments forwarded to :func:`xarray.open_dataset`.

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
    if not key.endswith((".nc", ".nc4", ".cdf")):
        raise ValueError("Expected a NetCDF key ending with .nc, .nc4, or .cdf.")

    url = f"s3://{bucket}/{key}"

    try:
        with fsspec.open(url, mode="rb", **(storage_options or {})) as f:
            ds = xr.open_dataset(
                f,
                engine=engine,
                group=group,
                chunks=chunks,
                **open_dataset_kwargs,
            )
            return ds
    except FileNotFoundError as e:
        raise FileNotFoundError(f"S3 object not found: {url}") from e
    except Exception as e:
        raise RuntimeError(
            f"Failed to open NetCDF from {url} (group='{group}'): {e}"
        ) from e
