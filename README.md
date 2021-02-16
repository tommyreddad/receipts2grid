# receipts2grid

This script can be used to extract addresses from a PDF file containing pages of etsy receipts, and arrange these addresses in a customizable grid.

## Prerequisites

- [Python 3](https://www.python.org/downloads/)
- [PyMuPDF](https://pypi.org/project/PyMuPDF/)

## Usage

The simplest usage is as follows:

```shell
python receipts2grid.py input.pdf
```

This extracts the addresses and saves them to the file `output.pdf` in the working directory. The following optional arguments can be supplied:

- **`--rows, -r` (default=14)**: number of grid rows per output page.
- **`--columns, -c` (default=6)**: number of grid columns per output page.
- **`--font, -f` (default=helv)**: font for the output address labels.
- **`--fontsize, -s` (default=6)**: font size for the output address labels.
- **`--page-margin, -P` (default=20)**: border margin for the output pages.
- **`--cell-margin, -C` (default=5)**: border margin for each grid cell of the output.
- **`--paper-size, -p` (default=A4)**: papersize format for the output pages.
- **`--landscape, -l`**: toggle to output in landscape mode.
- **`--output, -o` (default=output.pdf)**: target path to the output file.
