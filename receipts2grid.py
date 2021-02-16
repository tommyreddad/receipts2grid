import argparse
import fitz  # PyMuPDF
import sys


def get_addresses_from_receipt(doc):
    """Get the list of addresses from a doc of etsy receipts."""
    addresses = []
    # this assumes each page has exactly one address written in the following format:
    #   Ship to
    #   <address>
    #   Scheduled to ship by
    for i, page in enumerate(doc):
        words = page.getText()
        try:
            start = words.index("Ship to\n") + len("Ship to\n")
            end = words.index("\nScheduled to ship by")
        except ValueError as e:
            print("Failed to parse page {}: {}".format(i + 1, e))
            continue
        addresses.append(words[start:end])
    return addresses


def parse_args():
    """Setup the command-line argument parser and parse them."""
    parser = argparse.ArgumentParser(
        description="This script can be used to extract addresses from a PDF file containing pages of etsy receipts, and arrange these addresses in a customizable grid.")
    parser.add_argument(
        'filepath', help="target path to the input receipt PDF file")
    parser.add_argument('--rows', "-r", type=int, default=14,
                        help="number of grid rows per output page")
    parser.add_argument('--columns', "-c", type=int, default=6,
                        help="number of grid columns per output page")
    parser.add_argument('--font', "-f", type=str, default="helv",
                        help="font for the output address labels")
    parser.add_argument('--fontsize', "-s", type=int, default=6,
                        help="font size for the output address labels")
    parser.add_argument('--page-margin', "-P", type=int,
                        default=20, help="border margin for the output pages")
    parser.add_argument('--cell-margin', "-C", type=int, default=5,
                        help="border margin for each grid cell of the output")
    parser.add_argument('--paper-size', "-p", type=str, default="A4",
                        help="papersize format for the output pages")
    parser.add_argument('--landscape', "-l", action="store_true",
                        help="toggle to output in landscape mode")
    parser.add_argument('--output', "-o", type=str,
                        default="output.pdf", help="target path to the output file")
    return parser.parse_args()


def write_addresses_to_doc(doc, addresses, rows, columns, font, fontsize, page_margin, cell_margin, width, height):
    """Write list of addresses to a grid in a given PDF document."""
    for i, address in enumerate(addresses):
        if i % (rows*columns) == 0:
            # start a new page if all cells are filled
            page = doc.newPage(width=width, height=height)
            table_rect = page.rect + \
                (page_margin, page_margin, -page_margin, -page_margin)
            cells = fitz.make_table(rect=table_rect, cols=columns, rows=rows)
            wr = fitz.TextWriter(page.rect)

            def draw_grid_line(origin, target):
                shape = page.newShape()
                shape.drawLine(origin, target)
                shape.finish(dashes="[3] 0")
                shape.commit()
            # draw the row grid lines
            for r in range(rows+1):
                row_height = int(float(page_margin) +
                                 float(height - 2*page_margin)*float(r)/float(rows))
                draw_grid_line((0, row_height), (width, row_height))
            # draw the column grid lines
            for c in range(columns+1):
                column_width = int(
                    float(page_margin) + float(width - 2*page_margin)*float(c)/float(columns))
                draw_grid_line((column_width, 0), (column_width, height))
        # write the addresses from left-to-right, and top-down.
        # extract the row and column coordinates from the address index.
        row = (i // columns) % rows
        col = i % columns
        cell_rect = cells[row][col] + \
            (cell_margin, cell_margin, -cell_margin, -cell_margin)
        wr.fillTextbox(cell_rect, text=address,
                       fontsize=fontsize, font=font)
        if ((i == len(addresses) - 1) or (i % (rows*columns) == rows*columns - 1)):
            # write the page if we've reached the end of the address list, or if we've filled all grid cells
            wr.writeText(page)


def main():
    args = parse_args()
    font = fitz.Font(args.font)
    width, height = fitz.PaperSize(args.paper_size)
    if args.landscape:
        # just flip the width and height in landscape mode
        width, height = height, width

    # extract addresses from the input file
    # addresses = []
    with fitz.open(args.filepath) as receipt_doc:
        addresses = get_addresses_from_receipt(doc=receipt_doc)

    # write the addresses to the output document
    with fitz.open() as output_doc:
        write_addresses_to_doc(doc=output_doc, addresses=addresses, rows=args.rows, columns=args.columns, font=font, fontsize=args.fontsize, page_margin=args.page_margin,
                               cell_margin=args.cell_margin, width=width, height=height)
        output_doc.save(args.output)


if __name__ == "__main__":
    main()
