import json
import re

from rest_framework.exceptions import ValidationError


def parse_form_data(request):
    letter_data_str = request.data.get("letter", "{}")
    otp = request.data.get("otp", "")
    # print(otp)
    # print(request.data.item())

    try:
        letter_data = json.loads(letter_data_str)
    except json.JSONDecodeError:
        raise ValidationError("Invalid JSON data")

    attachment_pattern = re.compile(r"attachments\[(\d+)]\.(\w+)")

    attachments = []
    for key, value in request.data.items():
        match = attachment_pattern.match(key)
        if match:
            index = int(match.group(1))
            field_name = match.group(2)

            if len(attachments) <= index:
                attachments.extend({"file": None, "description": None} for _ in range(len(attachments), index + 1))

            if field_name == "file":
                attachments[index]["file"] = request.FILES.get(key)
            elif field_name == "description":
                attachments[index]["description"] = value if value and value != "undefined" else ""

    return letter_data, attachments
