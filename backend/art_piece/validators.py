import re
from rest_framework.exceptions import ValidationError as DrfError
from django.core.exceptions import ValidationError as DjangoError

YEAR_PATTERN = re.compile(r"^(ca\.\s)?\d{4}(\?|-\d{4})?$")

def validate_year(value, drf=False):
    if value and not YEAR_PATTERN.match(value):
        msg = f"Year has to be 'YYYY', 'YYYY-YYYY', 'ca. YYYY' or 'YYYY?', but given: {value}"
        raise (DrfError if drf else DjangoError)(msg)