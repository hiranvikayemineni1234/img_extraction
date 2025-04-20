import streamlit as st
from PIL import Image, ImageOps
import pytesseract
import re
import io
from pdf2image import convert_from_bytes  # For handling PDF images

# Set Tesseract command path
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_text_from_image(image):
    gray = ImageOps.grayscale(image)
    text = pytesseract.image_to_string(gray)
    return text

def process_pdf_image(pdf_file):
    try:
        images = convert_from_bytes(pdf_file.read())
        if images:
            return images[0]  # Assuming the first page contains the image
        else:
            st.error("No images found in the PDF.")
            return None
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        return None

def analyze_confusion_matrix_knowledge():
    report = []
    report.append("**General Knowledge on Confusion Matrices:**")
    report.append("- A confusion matrix typically has dimensions corresponding to the number of classes.")
    report.append("- For binary: TP, FP, FN, TN represent counts of true/false positives/negatives.")
    report.append("- Axes represent predicted vs. actual classes.")
    report.append("- Issues: Missing cells, inconsistent labels, negative values.")
    return "\n".join(report)

def analyze_formulas_knowledge():
    report = []
    report.append("**General Knowledge on Formulas:**")
    report.append("- Formulas show relationships between variables using math symbols.")
    report.append("- Elements: variables, constants, operators, functions.")
    report.append("- Issues: Syntax errors, undefined variables, nonsensical operations.")
    return "\n".join(report)

def main():
    st.title("Image Analysis (PDF Support - Knowledge-Based)")

    uploaded_file = st.file_uploader("Upload an image or a PDF file containing an image", type=["png", "jpg", "jpeg", "pdf"])

    extracted_text = ""
    confusion_matrix_report = analyze_confusion_matrix_knowledge()
    formula_report = analyze_formulas_knowledge()

    if uploaded_file is not None:
        file_type = uploaded_file.type

        if file_type.startswith("image"):
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image.", use_container_width=True)
            extracted_text = extract_text_from_image(image)

        elif file_type == "application/pdf":
            image_from_pdf = process_pdf_image(uploaded_file)
            if image_from_pdf:
                st.image(image_from_pdf, caption="Image from PDF.", use_container_width=True)
                extracted_text = extract_text_from_image(image_from_pdf)
        else:
            st.error("Unsupported file type. Please upload a PNG, JPG, JPEG, or PDF file.")

    st.subheader("General Knowledge-Based Analysis:")
    st.markdown(confusion_matrix_report)
    st.markdown(formula_report)

    st.subheader("Ask a Question (Based on Image Expectation):")
    query = st.text_input("Enter your query about the expected confusion matrix or formulas in the image:")
    if st.button("Ask"):
        st.write(f"**Your Query:** {query}")
        knowledge_based_answer = "**Knowledge-Based Answer:** "

        if "f1 score" in query.lower():
            knowledge_based_answer += "The F1 score is a common metric derived from a confusion matrix, especially for binary classification. It is the harmonic mean of precision and recall. Precision is TP / (TP + FP), and recall is TP / (TP + FN). A potential issue would be an F1 score calculated incorrectly from the TP, FP, and FN values (if they were present)."
        elif "accuracy" in query.lower() and "confusion matrix" in query.lower():
            knowledge_based_answer += "Accuracy, in the context of a confusion matrix, is typically calculated as (TP + TN) / (TP + TN + FP + FN) for binary classification. An incorrect accuracy would arise from using the wrong formula or incorrect values from the matrix."
        elif "precision" in query.lower() and "confusion matrix" in query.lower():
            knowledge_based_answer += "Precision (also called positive predictive value) is calculated as TP / (TP + FP). It indicates how many of the positively predicted cases were actually positive. An incorrect precision would result from using the wrong TP or FP values."
        elif "recall" in query.lower() and "confusion matrix" in query.lower():
            knowledge_based_answer += "Recall (also called sensitivity or true positive rate) is calculated as TP / (TP + FN). It indicates how many of the actual positive cases were correctly identified. An incorrect recall would result from using the wrong TP or FN values."
        elif "formula" in query.lower() and "syntax" in query.lower():
            knowledge_based_answer += "A formula with incorrect syntax might have unbalanced parentheses, missing operators between variables or numbers, or misuse of mathematical symbols."
        elif "variable" in query.lower() and "defined" in query.lower() and "formula" in query.lower():
            knowledge_based_answer += "A formula using an undefined variable (a variable not introduced or explained within the context) would be considered potentially incorrect or incomplete."
        else:
            knowledge_based_answer += "Based on general knowledge, I don't see an immediately obvious issue related to your query."

        st.write(knowledge_based_answer)

        st.subheader("Extracted Text (for your context):")
        st.write(extracted_text if extracted_text else "No text extracted from the image.")

if __name__ == "__main__":
    main()
