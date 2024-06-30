import json
import decimal

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert a DynamoDB number to JSON."""
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)