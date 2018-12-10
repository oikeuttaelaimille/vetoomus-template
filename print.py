from fpdf import FPDF
from itertools import zip_longest
import csv
import sys

# C5 letter in millimeters
A4_X = 210
A4_Y = 294

IMG_FILENAME = 'logo-mustavalkoinen-valkoiselle.png'
FONT_FILENAME = 'fonts/Ubuntu-R.ttf'
TEXT = 'Eläinten asia on nyt otettava vakavasti. Eläinsuojelun edistäminen on otettava hallitusohjelmaan. Olemassaolevia säädöksiä on alettava oikeasti valvoa. Eläinsuojelulaki on uudistettava niin, että eläinten näkökulma on etusijalla.'
PRINT_LOGO = True
FONT_SIZE = 7
DEBUG = 0

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

class PDF(FPDF):
  def header(self):
    self.image(IMG_FILENAME,
              0.03 * A4_X,  # X
              0.015 * A4_Y,  # Y
              0.20 * A4_X)   # W

    self.set_xy(0.40 * A4_X,
               0.019 * A4_Y)

    self.set_font_size(8)
    self.multi_cell(0.52 * A4_X,  # X
                    0.01 * A4_Y,  # Y
                    TEXT)

  def footer(self):
    self.set_y(-15)
    self.cell(0, 10, '%s / {nb}' % self.page_no(), 0, 0, 'C')

def write_document(out, rows):
    """Create pdf from addresses and write it to output file."""
    pdf = PDF('P', 'mm', 'A4')
    pdf.alias_nb_pages()
    pdf.add_font('ubuntu', '', FONT_FILENAME, uni=True)
    pdf.set_font('ubuntu', '', FONT_SIZE)

    # TODO Make offsets % - based
    for group in grouper(255, rows):
        pdf.add_page()

        string1 = '\n'.join([(x[0].title() + ' ' + x[1].title() + ((', ' + x[2].title()) if x[2] else '')) for x in group[0:85] if x])
        string2 = '\n'.join([(x[0].title() + ' ' + x[1].title() + ((', ' + x[2].title()) if x[2] else '')) for x in group[85:170] if x])
        string3 = '\n'.join([(x[0].title() + ' ' + x[1].title() + ((', ' + x[2].title()) if x[2] else '')) for x in group[170:255] if x])

        pdf.set_font('ubuntu', '', FONT_SIZE)

        pdf.set_xy(0.04 * A4_X,
                   0.075 * A4_Y)
        pdf.multi_cell(0.30 * A4_X,  # Line width
                       0.01 * A4_Y,  # Line height
                       string1, DEBUG, 'L')

        pdf.set_xy(0.34 * A4_X,
                   0.075 * A4_Y)
        pdf.multi_cell(0.30 * A4_X,  # Line width
                       0.01 * A4_Y,  # Line height
                       string2, DEBUG, 'L')

        pdf.set_xy(0.64 * A4_X,
                   0.075 * A4_Y)
        pdf.multi_cell(0.30 * A4_X,  # Line width
                       0.01 * A4_Y,  # Line height
                       string3, DEBUG, 'L')


    pdf.output(out, 'F')


def load_csv():
    """Return generator which outputs csv rows."""
    for i, row in enumerate(csv.reader(sys.stdin, delimiter='\t', quotechar='"')):
        if i == 0:
            continue

        yield list(map(str.strip, row[0:2] + row[3:4]))


if __name__ == '__main__':
    OUTFILE = 'out.pdf'

    write_document(OUTFILE, list(load_csv()))
    print('wrote %s.' % OUTFILE)
