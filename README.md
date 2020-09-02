# Petition template

Edit petition text in print.py

```bash
cat "vetoomus.csv" | python print.py
open out.pdf
```

## Installing

```bash
python3 -m venv ./venv
. venv/bin/activate
pip install -r requirements.txt
```
## Data format

Accepts csv files downloaded directly from drupal. Needs columns sahkoposti, etunimi, sukunimi, paikkakunta. Other fields discarded.

