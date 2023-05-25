# coding=utf-8
from fpdf import FPDF
from itertools import zip_longest
import csv
import sys
from collections import namedtuple
import re
from string import printable
import unicodedata

# C5 letter in millimeters
A4_X = 210
A4_Y = 294

#IMG_FILENAME = 'logo-mustavalkoinen-valkoiselle.png'
IMG_FILENAME = 'logo-varillinen.png'
FONT_FILENAME = 'fonts/Ubuntu-R.ttf'
TEXT = "Vaadimme kaikille kakkua."
PRINT_LOGO = True
FONT_SIZE = 7
DEBUG = 0

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


class PDF(FPDF):
    def header(self):
        self.image(
            IMG_FILENAME,
            0.03 * A4_X,  # X
            0.015 * A4_Y,  # Y
            0.20 * A4_X)  # W

        self.set_xy(0.40 * A4_X, 0.019 * A4_Y)

        self.set_font_size(8)
        self.multi_cell(
            0.52 * A4_X,  # X
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

        group1 = group[:85]
        group2 = group[85:170]
        group3 = group[170:]

        string1 = '\n'.join([
            (x.etunimi.title() + ' ' + x.sukunimi.title() +
             ((', ' + x.paikkakunta.title()) if x.paikkakunta else ''))
            for x in group1 if x
        ])
        string2 = '\n'.join([
            (x.etunimi.title() + ' ' + x.sukunimi.title() +
             ((', ' + x.paikkakunta.title()) if x.paikkakunta else ''))
            for x in group2 if x
        ])
        string3 = '\n'.join([
            (x.etunimi.title() + ' ' + x.sukunimi.title() +
             ((', ' + x.paikkakunta.title()) if x.paikkakunta else ''))
            for x in group3 if x
        ])

        pdf.set_font('ubuntu', '', FONT_SIZE)

        pdf.set_xy(0.04 * A4_X, 0.075 * A4_Y)
        pdf.multi_cell(
            0.30 * A4_X,  # Line width
            0.01 * A4_Y,  # Line height
            string1,
            DEBUG,
            'L')

        pdf.set_xy(0.34 * A4_X, 0.075 * A4_Y)
        pdf.multi_cell(
            0.30 * A4_X,  # Line width
            0.01 * A4_Y,  # Line height
            string2,
            DEBUG,
            'L')

        pdf.set_xy(0.64 * A4_X, 0.075 * A4_Y)
        pdf.multi_cell(
            0.30 * A4_X,  # Line width
            0.01 * A4_Y,  # Line height
            string3,
            DEBUG,
            'L')

    pdf.output(out, 'F')


def format_field_name(field_name):
    field_name = field_name.lower().strip()
    field_name = field_name.replace(' ', '_')
    field_name = field_name.replace('-', '_')
    field_name = field_name.replace('ä', 'a')
    field_name = field_name.replace('ö', 'o')
    field_name = field_name.replace(':', '')
    field_name = field_name.replace('.', '')

    return field_name.strip()


def load_csv(infile):
    """Return generator which outputs csv rows."""
    header = infile.readline()
    dialect = csv.Sniffer().sniff(header)
    reader = csv.reader((header, ), dialect)

    CSVRow = namedtuple("CSVRow", [format_field_name(x) for x in next(reader)])

    reader = csv.reader(infile, dialect)

    for data in map(CSVRow._make, reader):
        yield data

def normalize_row(row):
    for field, value in row._asdict().items():
        row = row._replace(**{field: unicodedata.normalize("NFC", value)})
    return row

if __name__ == '__main__':
    OUTFILE = 'Vetoomuksen_allekirjoittajat.pdf'

    data = []

    emailit = set()
    for row in load_csv(sys.stdin):
        row = normalize_row(row)
        if row.sahkoposti not in emailit:
            if len(row.etunimi) < 2 or len(row.sukunimi) < 2:
                continue
          
            # if not re.search(
            #         r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
            #         row.sahkoposti):
            #     print(row.etunimi, row.sukunimi, row.sahkoposti)
            #     continue
            data.append(row)
            emailit.add(row.sahkoposti)

    write_document(OUTFILE, data)
    print(f'wrote {OUTFILE} ({len(data)} rows).')
