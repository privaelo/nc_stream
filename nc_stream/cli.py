import argparse
from . import stream_netcdf

def main():
    parser = argparse.ArgumentParser(description="Stream Sentinel-5P NetCDF from S3")
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--key", required=True)
    parser.add_argument("--group", default="/PRODUCT")
    args = parser.parse_args()

    ds = stream_netcdf(args.bucket, args.key, group=args.group)
    print(ds)

if __name__ == "__main__":
    main()
