
import fitz
import logging
import time

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import PDFUploadForm
from .models import PDFDocument, Conversation, ChatMessage

from .services.rag_service import process_pdf_pages
from .services.search_service import search_chunks
from .services.gemini_service import generate_answer


logger = logging.getLogger(__name__)


# --------------------------------------------------
# 1. UPLOAD PDF
# --------------------------------------------------

def upload_pdf(request):

    if request.method == "POST":

        form = PDFUploadForm(request.POST, request.FILES)

        if form.is_valid():

            document = form.save()

            messages.success(
                request,
                "PDF uploaded successfully!"
            )

            return redirect("extract_pdf", pk=document.pk)

    else:

        form = PDFUploadForm()

    return render(
        request,
        "chatbot/upload.html",
        {
            "form": form
        }
    )


# --------------------------------------------------
# 2. EXTRACT PDF AND CREATE EMBEDDINGS
# --------------------------------------------------

def extract_pdf(request, pk):

    document = get_object_or_404(
        PDFDocument,
        pk=pk
    )

    try:

        with fitz.open(document.file.path) as pdf:

            if len(pdf) == 0:

                messages.error(
                    request,
                    "The PDF contains no pages."
                )

                return redirect("upload_pdf")

            pages = []

            for index, page in enumerate(pdf):

                text = page.get_text("text").strip()

                pages.append({
                    "page_number": index + 1,
                    "text": text
                })

    except (fitz.FileDataError, RuntimeError, OSError):

        logger.exception("PDF extraction failed")

        messages.error(
            request,
            "Unable to read this PDF file."
        )

        return redirect("upload_pdf")

    try:

        chunk_count = process_pdf_pages(
            document.pk,
            pages
        )

    except Exception:

        logger.exception("RAG processing failed")

        messages.error(
            request,
            "Unable to process PDF for RAG."
        )

        return redirect("upload_pdf")

    return render(
        request,
        "chatbot/extracted_text.html",
        {
            "document": document,
            "pages": pages,
            "chunk_count": chunk_count
        }
    )


# --------------------------------------------------
# 3. CHAT WITH PDF
# --------------------------------------------------

def search_pdf(request):

    request_start = time.perf_counter()

    documents = PDFDocument.objects.all().order_by("-uploaded_at")

    retrieved_chunks = []

    selected_document_id = None
    selected_document_title = None
    conversation_id = None

    question = ""
    answer = None
    source_pages = []
    chat_history = []

    if request.method == "POST":

        question = request.POST.get(
            "question", ""
        ).strip()

        document_id = request.POST.get(
            "document_id", ""
        )

        submitted_conversation_id = request.POST.get(
            "conversation_id", ""
        )

        if not question:

            messages.error(
                request,
                "Please enter a question."
            )

        elif not document_id.isdigit():

            messages.error(
                request,
                "Please select a valid PDF."
            )

        else:

            document = get_object_or_404(
                documents,
                pk=int(document_id)
            )

            selected_document_id = document.pk
            selected_document_title = document.title

            # --------------------------------------
            # GET OR CREATE CONVERSATION
            # --------------------------------------

            conversation = None

            if submitted_conversation_id.isdigit():

                conversation = Conversation.objects.filter(
                    pk=int(submitted_conversation_id),
                    document=document
                ).first()

            if conversation is None:

                conversation = Conversation.objects.create(
                    document=document,
                    title=question[:200]
                )

            conversation_id = conversation.pk

            try:

                # ----------------------------------
                # LOAD PREVIOUS CHAT HISTORY
                # ----------------------------------

                previous_messages = list(
                    conversation.messages.order_by(
                        "-created_at"
                    )[:10]
                )

                previous_messages.reverse()

                chat_history = [
                    {
                        "role": message.role,
                        "content": message.content
                    }
                    for message in previous_messages
                ]

                # ----------------------------------
                # SAVE USER QUESTION
                # ----------------------------------

                ChatMessage.objects.create(
                    conversation=conversation,
                    role="user",
                    content=question
                )

                # ----------------------------------
                # VECTOR SEARCH
                # No separate Gemini rewriting call
                # ----------------------------------

                start = time.perf_counter()

                search_query = question

                retrieved_chunks = search_chunks(
                    question=search_query,
                    document_id=document.pk,
                    top_k=3
                )

                print(
                    "Vector search:",
                    round(
                        time.perf_counter() - start,
                        2
                    ),
                    "seconds"
                )

                # ----------------------------------
                # FILTER IRRELEVANT CHUNKS
                # ----------------------------------

                MAX_DISTANCE = 1.5

                retrieved_chunks = [
                    chunk
                    for chunk in retrieved_chunks
                    if chunk["distance"] <= MAX_DISTANCE
                ]

                # ----------------------------------
                # GENERATE ANSWER
                # ----------------------------------

                start = time.perf_counter()

                if not retrieved_chunks:

                    answer = (
                        "I could not find sufficiently relevant "
                        "information in this PDF to answer "
                        "your question."
                    )

                else:

                    answer = generate_answer(
                        question=question,
                        retrieved_chunks=retrieved_chunks,
                        conversation_history=chat_history
                    )

                    source_pages = sorted({
                        chunk["page_number"]
                        for chunk in retrieved_chunks
                    })

                print(
                    "Gemini answer generation:",
                    round(
                        time.perf_counter() - start,
                        2
                    ),
                    "seconds"
                )

                # ----------------------------------
                # SAVE AI RESPONSE
                # ----------------------------------

                ChatMessage.objects.create(
                    conversation=conversation,
                    role="assistant",
                    content=answer
                )

                # ----------------------------------
                # LOAD UPDATED CONVERSATION
                # ----------------------------------

                chat_history = list(
                    conversation.messages.order_by(
                        "created_at"
                    )
                )

            except Exception:

                logger.exception(
                    "AI PDF question answering failed"
                )

                answer = (
                    "Sorry, something went wrong while "
                    "generating your answer. Please try again."
                )

                ChatMessage.objects.create(
                    conversation=conversation,
                    role="assistant",
                    content=answer
                )

                chat_history = list(
                    conversation.messages.order_by(
                        "created_at"
                    )
                )

    print(
        "Total request processing:",
        round(
            time.perf_counter() - request_start,
            2
        ),
        "seconds"
    )

    return render(
        request,
        "chatbot/search.html",
        {
            "documents": documents,
            "retrieved_chunks": retrieved_chunks,
            "selected_document_id": selected_document_id,
            "selected_document_title": selected_document_title,
            "conversation_id": conversation_id,
            "question": question,
            "answer": answer,
            "source_pages": source_pages,
            "chat_history": chat_history,
        }
    )
