# Getting Started 

The simplest (and recommended) way to install **carst** is by using the `pip` package manager. The command below installs **carst** along with all the required dependencies in your current Python environment:

```bash
pip install carst
```

Make sure your environment has Python version **3.0 or higher** before installation. If you're working in a clean environment (e.g., using `venv`, `conda`, or `mamba`), this ensures that all dependencies are managed properly.



## Required packages:

- `python >= 3.0`
- `scipy`
- `gdal`
- `shapely`
- `rasterio`
- `geopandas`
- `matplotlib`
- `scikit-image`

These packages will be installed automatically when using `pip`.



### Optional package:

- `ISCE >= 2.0.0` (must be built with your Python environment; required for feature tracking functionality)

If you intend to use **carst** for feature tracking, please ensure **ISCE** is installed and properly configured in your environment.



## Command-Line Interface (CLI) Usage

After installation, **carst** provides two command-line interface (CLI) tools that can be used directly from your terminal:

```bash
$ dhdt.py --help
$ featuretrack.py --help
```

Use the `--help` flag to view available options, required arguments, and usage examples for each tool. These scripts are designed to streamline your workflow for displacement and feature tracking tasks.
