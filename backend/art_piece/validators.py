import re
from rest_framework.exceptions import ValidationError as DrfError
from django.core.exceptions import ValidationError as DjangoError

YEAR_PATTERN = re.compile(r"^(ca\.\s)?\d{4}(\?|-\d{4})?$")

def validate_year(value, drf=False):
    if value and not YEAR_PATTERN.match(value):
        msg = f"Year has to be 'YYYY', 'YYYY-YYYY', 'ca. YYYY', 'ca. YYYY-YYYY' or 'YYYY?', but given: {value}"
        raise (DrfError if drf else DjangoError)(msg)

MEASUREMENTS_PATTERN = re.compile(r"^\d+\s(cm|m)\sx\s\d+\s(cm|m)$")

def validate_measurements(value, drf=False):
    if value and not MEASUREMENTS_PATTERN.match(value):
        msg = f"Measurements has to be 'h cm x w cm' or 'h m x w m', but given: {value}"
        raise (DrfError if drf else DjangoError)(msg)