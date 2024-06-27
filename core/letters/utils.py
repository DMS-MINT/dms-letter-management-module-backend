import json


def process_request_data(request):
    participants_json = request.POST.get("participants", "[]")
    participants = json.loads(participants_json)

    request_data = {
        "subject": request.POST.get("subject", ""),
        "content": request.POST.get("content", ""),
        "letter_type": request.POST.get("letter_type", ""),
        "participants": participants,
    }

    if "signature" in request.FILES:
        request_data["signature"] = request.FILES.get("signature")

    if "attachments" in request.FILES:
        request_data["attachments"] = request.FILES.getlist("attachments")

    return request_data
