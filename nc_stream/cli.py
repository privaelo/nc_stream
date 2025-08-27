import argparse
from . import stream_netcdf


def main():
    parser = argparse.ArgumentParser(description="Stream NetCDF from S3")
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--key", required=True)
    parser.add_argument("--group", default=None)
    parser.add_argument("--engine")
    parser.add_argument(
        "--storage-option",
        action="append",
        default=[],
        metavar="key=value",
        help="Storage option for the stream (can repeat)",
    )
    args = parser.parse_args()

    storage_options = {}
    for item in args.storage_option:
        if "=" not in item:
            parser.error("--storage-option must be in key=value format")
        key, value = item.split("=", 1)
        storage_options[key] = value

    call_args = {"bucket": args.bucket, "key": args.key}
    if args.group is not None:
        call_args["group"] = args.group
    if args.engine is not None:
        call_args["engine"] = args.engine
    if storage_options:
        call_args["storage_options"] = storage_options

    ds = stream_netcdf(**call_args)
    print(ds)


if __name__ == "__main__":
    main()
