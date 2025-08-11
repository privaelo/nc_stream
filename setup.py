from setuptools import setup, find_packages

setup(
    name="sentinel5pstream",
    version="0.1.0",
    description="Stream Sentinel-5P NetCDF files from public S3 into xarray, no local download",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Tagnon Okoumassoun",
    url="https://github.com/privaelo/nc_stream",
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.8",
    install_requires=[
        "boto3>=1.26",
        "xarray>=2023.1",
        "h5netcdf>=1.1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: GIS",
    ],
)
