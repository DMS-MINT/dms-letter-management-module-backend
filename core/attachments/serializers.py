import io

import filetype
from drf_extra_fields.fields import Base64FileField
from rest_framework import serializers


# class FileField(Base64FileField):
#     ALLOWED_TYPES = ["pdf", "txt", "png", "jpg", "jpeg", "docx"]

#     def validate_file(self, decoded_file, file_extension):
#         print(file_extension)
#         if file_extension not in self.ALLOWED_TYPES:
#             raise serializers.ValidationError("Unsupported file type.")

#     def get_file_extension(self, filename, decoded_file):
#         kind = filetype.guess(io.BytesIO(decoded_file))
#         if kind is None:
#             raise serializers.ValidationError("Cannot determine file type.")

#         file_extension = kind.extension
#         self.validate_file(decoded_file, file_extension)
#         return file_extension


# class PDFBase64File(Base64FileField):
#     ALLOWED_TYPES = ["pdf"]

#     def get_file_extension(self, filename, decoded_file):
#         try:
#             # Try to read the file as a PDF
#             PyPDF2.PdfFileReader(io.BytesIO(decoded_file))
#         except PyPDF2.utils.PdfReadError as e:
#             raise serializers.ValidationError("Invalid PDF file.")
#         else:
#             # Return the file extension if validation is successful
#             return "pdf"


# class AttachmentSerializer(serializers.Serializer):
#     id = serializers.UUIDField()
#     name = serializers.CharField()
#     file_type = serializers.CharField()
#     size = serializers.IntegerField()
#     remote_file_url = serializers.CharField(allow_blank=True)
#     uploaded_file = PDFBase64File()
#     description = serializers.CharField(allow_blank=True)
