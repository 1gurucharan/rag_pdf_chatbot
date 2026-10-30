from django import forms
from .models import PDFDocument


class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ["title", "file"]

    def clean_file(self):
        file = self.cleaned_data["file"]

        if not file.name.lower().endswith(".pdf"):
            raise forms.ValidationError("Please upload a PDF file.")

        if file.size > 10 * 1024 * 1024:
            raise forms.ValidationError("PDF size must be under 10 MB.")

        return file