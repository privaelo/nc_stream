import argparse
import json
from . import stream_netcdf


def main():
    parser = argparse.ArgumentParser(description="Stream NetCDF from S3")
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--key", required=True)
    parser.add_argument("--group", default=None)
    parser.add_argument("--engine", default=None)
    parser.add_argument("--chunks", default=None)
    parser.add_argument(
        "--storage-option", action="append", default=[], metavar="key=value"
    )
    args = parser.parse_args()

    kwargs = vars(args).copy()
    storage_list = kwargs.pop("storage_option", [])
    storage_options = {}
    for item in storage_list:
        if "=" in item:
            key, value = item.split("=", 1)
            storage_options[key] = value
    chunks = kwargs.get("chunks")
    if chunks is not None:
        kwargs["chunks"] = json.loads(chunks)
    kwargs["storage_options"] = storage_options

    ds = stream_netcdf(**kwargs)
    print(ds)

if __name__ == "__main__":
    main()
