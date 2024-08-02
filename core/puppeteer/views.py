from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from weasyprint import HTML

from core.letters.models import Letter
from core.participants.models import Participant


def display_letter(request):
    letter_instance = Letter.objects.get(reference_number="EGD-2024-0002")
    primary_recipients = letter_instance.participants.filter(role=Participant.Roles.PRIMARY_RECIPIENT)
    cc_participants = letter_instance.participants.filter(role=Participant.Roles.CC)
    bcc_participants = letter_instance.participants.filter(role=Participant.Roles.BCC)

    context = {
        "letter": letter_instance,
        "primary_recipients": primary_recipients,
        "cc_participants": cc_participants,
        "bcc_participants": bcc_participants,
    }

    return render(request, "test_template.html", context)


def generate_pdf(request):
    letter_instance = Letter.objects.get(reference_number="IRS-2024-0004")
    context = {"letter": letter_instance}
    html_string = render_to_string("home.html", context)
    pdf_file = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="test_template.pdf"'
    return response
