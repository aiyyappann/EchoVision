# # from flask import Flask, render_template, request, send_from_directory, url_for
# # import os
# # import boto3
# # import pdfplumber
# # import json
# # import logging
# # from dotenv import load_dotenv
# # import requests  # For Google API calls

# # # Load environment variables from .env file
# # load_dotenv()

# # app = Flask(__name__)  

# # # Configuration
# # UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
# # AUDIO_FOLDER = os.getenv("AUDIO_FOLDER", "static/audio")
# # AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
# # AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# # AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# # GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # New Google API key

# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
# # app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit

# # # Set up logging
# # logging.basicConfig(level=logging.INFO)

# # # Ensure directories exist
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# # os.makedirs(AUDIO_FOLDER, exist_ok=True)

# # # Allowed extensions
# # ALLOWED_EXTENSIONS = {'pdf'}

# # def allowed_file(filename):
# #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # def convert_text_to_braille(text, api_key):
# #     """Convert text to Braille using Google's Text-to-Speech API"""
# #     try:
# #         url = "https://texttospeech.googleapis.com/v1/text:synthesize"
# #         headers = {
# #             "Content-Type": "application/json",
# #             "X-Goog-Api-Key": api_key
# #         }
        
# #         payload = {
# #             "input": {
# #                 "text": text
# #             },
# #             "voice": {
# #                 "languageCode": "en-US"
# #             },
# #             "audioConfig": {
# #                 "audioEncoding": "LINEAR16",
# #                 "speakingRate": 1.0
# #             },
# #             "enableBraille": True  # Request Braille output
# #         }
        
# #         response = requests.post(url, headers=headers, json=payload)
# #         response.raise_for_status()
        
# #         data = response.json()
# #         braille_text = data.get("braille", {}).get("braille", "Braille conversion failed")
# #         return braille_text
        
# #     except Exception as e:
# #         logging.error(f"Error converting text to Braille: {e}")
# #         return "Braille conversion unavailable"

# # # Extract text from PDF
# # def extract_text_from_pdf(pdf_path):
# #     extracted_text = ""
# #     try:
# #         with pdfplumber.open(pdf_path) as pdf:
# #             for page in pdf.pages:
# #                 width, height = page.width, page.height
# #                 left_bbox = (0, 0, width / 2, height)
# #                 right_bbox = (width / 2, 0, width, height)
# #                 left_text = page.within_bbox(left_bbox).extract_text() or ""
# #                 right_text = page.within_bbox(right_bbox).extract_text() or ""
# #                 extracted_text += left_text.strip() + "\n" + right_text.strip() + "\n\n"
# #         return extracted_text
# #     except Exception as e:
# #         logging.error(f"Error extracting text from PDF: {e}")
# #         raise

# # # Summarize text using AWS Bedrock
# # def summarize_text_with_bedrock(text):
# #     model_id = "us.meta.llama3-2-1b-instruct-v1:0"
# #     try:
# #         bedrock_client = boto3.client(
# #             "bedrock-runtime",
# #             region_name='us-east-1',
# #             aws_access_key_id=AWS_ACCESS_KEY_ID,
# #             aws_secret_access_key=AWS_SECRET_ACCESS_KEY
# #         )
# #         text += " Summarize the above in 7 to 8 lines."
# #         prompt = (
# #             "You are a content summarization expert. Summarize the given content meaningfully without omitting important details."
# #             f"\n\nHuman:{text}\n\nAssistant:"
# #         )
# #         request_payload = {"prompt": prompt, "temperature": 0.5}
# #         response = bedrock_client.invoke_model(modelId=model_id, body=json.dumps(request_payload))
# #         model_response = json.loads(response["body"].read())
# #         return model_response.get("generation", "No summary generated.")
# #     except Exception as e:
# #         logging.error(f"Error summarizing text with Bedrock: {e}")
# #         raise

# # # Convert text to audio using Polly
# # def convert_text_to_audio_with_polly(text, output_path):
# #     try:
# #         polly_client = boto3.client(
# #             "polly",
# #             region_name=AWS_REGION,
# #             aws_access_key_id=AWS_ACCESS_KEY_ID,
# #             aws_secret_access_key=AWS_SECRET_ACCESS_KEY
# #         )
# #         response = polly_client.synthesize_speech(
# #             Text=text,
# #             OutputFormat="mp3",
# #             VoiceId="Joanna"
# #         )
# #         with open(output_path, "wb") as file:
# #             file.write(response["AudioStream"].read())
# #     except Exception as e:
# #         logging.error(f"Error converting text to audio with Polly: {e}")
# #         raise

# # @app.route("/", methods=["GET", "POST"])
# # def index():
# #     if request.method == "POST":
# #         pdf = request.files.get("pdf")
# #         if not pdf or not allowed_file(pdf.filename):
# #             logging.warning("Invalid file upload attempt.")
# #             return "Invalid file type. Only PDF files are allowed.", 400
        
# #         try:
# #             pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
# #             pdf.save(pdf_path)
# #             logging.info(f"Saved PDF to {pdf_path}")
            
# #             # Extract text and summarize
# #             extracted_text = extract_text_from_pdf(pdf_path)
# #             logging.info("Extracted text from PDF.")
# #             summary = summarize_text_with_bedrock(extracted_text)
# #             logging.info("Summarized text with Bedrock.")
            
# #             # Generate audio
# #             audio_filename = f"{os.path.splitext(pdf.filename)[0]}.mp3"
# #             audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
# #             convert_text_to_audio_with_polly(summary, audio_path)
# #             logging.info(f"Generated audio at {audio_path}")
            
# #             # Convert to Braille
# #             braille_text = convert_text_to_braille(summary, GOOGLE_API_KEY)
# #             logging.info("Converted summary to Braille.")
            
# #             # Return page with audio and braille
# #             audio_url = url_for("static", filename=f"audio/{audio_filename}")
# #             return render_template(
# #                 "index.html", 
# #                 audio_url=audio_url,
# #                 braille_text=braille_text,
# #                 summary_text=summary
# #             )
        
# #         except Exception as e:
# #             logging.error(f"An error occurred during processing: {e}")
# #             return "An error occurred while processing your request.", 500
    
# #     return render_template("index.html")

# # if __name__ == "__main__":
# #     app.run(debug=False, host='0.0.0.0', port=8000)
































# from flask import Flask, render_template, request, send_from_directory, url_for
# import os
# import boto3
# import pdfplumber
# import json
# import logging
# from dotenv import load_dotenv
# import requests  # For Google API calls

# # NEW: Import FPDF for PDF generation
# from fpdf import FPDF

# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__)

# # Configuration
# UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
# AUDIO_FOLDER = os.getenv("AUDIO_FOLDER", "static/audio")
# AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # New Google API key

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit

# # Set up logging
# logging.basicConfig(level=logging.INFO)

# # Ensure directories exist
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(AUDIO_FOLDER, exist_ok=True)

# # Allowed extensions
# ALLOWED_EXTENSIONS = {'pdf'}

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def convert_text_to_braille(text, api_key):
#     """Convert text to Braille using Google's Text-to-Speech API."""
#     try:
#         url = "https://texttospeech.googleapis.com/v1/text:synthesize"
#         headers = {
#             "Content-Type": "application/json",
#             "X-Goog-Api-Key": api_key
#         }
        
#         payload = {
#             "input": {
#                 "text": text
#             },
#             "voice": {
#                 "languageCode": "en-US"
#             },
#             "audioConfig": {
#                 "audioEncoding": "LINEAR16",
#                 "speakingRate": 1.0
#             },
#             "enableBraille": True  # Request Braille output
#         }
        
#         response = requests.post(url, headers=headers, json=payload)
#         response.raise_for_status()
        
#         data = response.json()
#         braille_text = data.get("braille", {}).get("braille", "Braille conversion failed")
#         return braille_text
        
#     except Exception as e:
#         logging.error(f"Error converting text to Braille: {e}")
#         return "Braille conversion unavailable"

# def extract_text_from_pdf(pdf_path):
#     """Extract text from a PDF file, splitting each page into left and right columns if needed."""
#     extracted_text = ""
#     try:
#         with pdfplumber.open(pdf_path) as pdf:
#             for page in pdf.pages:
#                 width, height = page.width, page.height
#                 left_bbox = (0, 0, width / 2, height)
#                 right_bbox = (width / 2, 0, width, height)
#                 left_text = page.within_bbox(left_bbox).extract_text() or ""
#                 right_text = page.within_bbox(right_bbox).extract_text() or ""
#                 extracted_text += left_text.strip() + "\n" + right_text.strip() + "\n\n"
#         return extracted_text
#     except Exception as e:
#         logging.error(f"Error extracting text from PDF: {e}")
#         raise

# def summarize_text_with_bedrock(text):
#     """Use AWS Bedrock to summarize the text."""
#     model_id = "us.meta.llama3-2-1b-instruct-v1:0"
#     try:
#         bedrock_client = boto3.client(
#             "bedrock-runtime",
#             region_name='us-east-1',
#             aws_access_key_id=AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=AWS_SECRET_ACCESS_KEY
#         )
#         # Append instructions for summarization
#         text += " Summarize the above in 7 to 8 lines."
#         prompt = (
#             "You are a content summarization expert. Summarize the given content meaningfully without omitting important details."
#             f"\n\nHuman:{text}\n\nAssistant:"
#         )
#         request_payload = {"prompt": prompt, "temperature": 0.5}
#         response = bedrock_client.invoke_model(modelId=model_id, body=json.dumps(request_payload))
#         model_response = json.loads(response["body"].read())
#         return model_response.get("generation", "No summary generated.")
#     except Exception as e:
#         logging.error(f"Error summarizing text with Bedrock: {e}")
#         raise

# def convert_text_to_audio_with_polly(text, output_path):
#     """Convert text to audio (MP3) using Amazon Polly."""
#     try:
#         polly_client = boto3.client(
#             "polly",
#             region_name=AWS_REGION,
#             aws_access_key_id=AWS_ACCESS_KEY_ID,
#             aws_secret_access_key=AWS_SECRET_ACCESS_KEY
#         )
#         response = polly_client.synthesize_speech(
#             Text=text,
#             OutputFormat="mp3",
#             VoiceId="Joanna"
#         )
#         with open(output_path, "wb") as file:
#             file.write(response["AudioStream"].read())
#     except Exception as e:
#         logging.error(f"Error converting text to audio with Polly: {e}")
#         raise

# @app.route("/", methods=["GET", "POST"])
# def index():
#     """Main route to handle PDF upload, summarization, audio generation, and short Braille display."""
#     if request.method == "POST":
#         pdf = request.files.get("pdf")
#         if not pdf or not allowed_file(pdf.filename):
#             logging.warning("Invalid file upload attempt.")
#             return "Invalid file type. Only PDF files are allowed.", 400
        
#         try:
#             pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
#             pdf.save(pdf_path)
#             logging.info(f"Saved PDF to {pdf_path}")
            
#             # Extract text and summarize
#             extracted_text = extract_text_from_pdf(pdf_path)
#             logging.info("Extracted text from PDF.")
#             summary = summarize_text_with_bedrock(extracted_text)
#             logging.info("Summarized text with Bedrock.")
            
#             # Generate audio for the summary
#             audio_filename = f"{os.path.splitext(pdf.filename)[0]}.mp3"
#             audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
#             convert_text_to_audio_with_polly(summary, audio_path)
#             logging.info(f"Generated audio at {audio_path}")
            
#             # Convert summary to Braille (for on-screen display)
#             braille_text = convert_text_to_braille(summary, GOOGLE_API_KEY)
#             logging.info("Converted summary to Braille.")
            
#             # Return page with audio, Braille summary, plus the original PDF filename
#             audio_url = url_for("static", filename=f"audio/{audio_filename}")
#             return render_template(
#                 "index.html", 
#                 audio_url=audio_url,
#                 braille_text=braille_text,
#                 summary_text=summary,
#                 pdf_filename=pdf.filename  # pass original PDF name for the download route
#             )
        
#         except Exception as e:
#             logging.error(f"An error occurred during processing: {e}")
#             return "An error occurred while processing your request.", 500
    
#     # GET request: just render the page with no results
#     return render_template("index.html")

# @app.route("/download_braille/<pdf_filename>", methods=["GET"])
# def download_braille(pdf_filename):
#     """
#     Route to convert the *entire* PDF to Braille and download as a PDF.
#     This is triggered by the "Download Braille" button in the template.
#     """
#     try:
#         # 1. Find the original PDF in the uploads folder
#         pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
#         if not os.path.exists(pdf_path):
#             return "File not found.", 404
        
#         # 2. Extract full text from the PDF
#         full_text = extract_text_from_pdf(pdf_path)
        
#         # 3. Convert the full text to Braille
#         braille_full_text = convert_text_to_braille(full_text, GOOGLE_API_KEY)
        
#         # 4. Generate a PDF file with the Braille text
#         braille_pdf_filename = f"{os.path.splitext(pdf_filename)[0]}_braille.pdf"
#         braille_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], braille_pdf_filename)
        
#         pdf = FPDF()
#         pdf.add_page()
#         pdf.set_font("Courier", size=12)
        
#         # multi_cell automatically wraps text; 
#         # we replace any \r to avoid extra spacing issues
#         pdf.multi_cell(0, 10, braille_full_text.replace('\r', ''))
        
#         pdf.output(braille_pdf_path)
        
#         # 5. Send it to the user as an attachment
#         return send_from_directory(app.config['UPLOAD_FOLDER'], braille_pdf_filename, as_attachment=True)
    
#     except Exception as e:
#         logging.error(f"Error in download_braille route: {e}")
#         return "Failed to generate Braille PDF.", 500

# if __name__ == "__main__":
#     app.run(debug=False, host='0.0.0.0', port=8000)



















from flask import Flask, render_template, request, send_from_directory, url_for
import os
import boto3
import pdfplumber
import json
import logging
from dotenv import load_dotenv
from fpdf import FPDF

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
AUDIO_FOLDER = os.getenv("AUDIO_FOLDER", "static/audio")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit

# Set up logging
logging.basicConfig(level=logging.INFO)

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Allowed extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

########################################################################
# Braille Conversion Dictionaries and Function
########################################################################

# Basic letter mapping (Grade‑1)
BRAILLE_MAP = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
    'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
    'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
    'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
    'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
    'z': '⠵'
}

# Punctuation mapping (a few common punctuation marks)
PUNCTUATION_MAP = {
    ',': '⠠⠂',
    '.': '⠲',
    '!': '⠖',
    '?': '⠦',
    ';': '⠆',
    ':': '⠒',
    '-': '⠤',
    "'": '⠄',
    '"': '⠐⠦',
    '(': '⠷',
    ')': '⠾'
}

# Digit mapping (using letters a-j with a number indicator)
DIGIT_MAP = {
    '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
    '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚'
}
NUMBER_INDICATOR = '⠼'

# Common Grade‑2 contractions
CONTRACTIONS = {
    "and": "⠯",   # contraction for "and"
    "for": "⠿",   # contraction for "for"
    "of": "⠷",    # contraction for "of"
    "the": "⠮",   # contraction for "the"
    "with": "⠾"   # contraction for "with"
}

def convert_text_to_braille(text):
    """
    Convert text to Braille with extended mappings:
      - Lowercase letters using BRAILLE_MAP.
      - Uppercase letters are prefixed with the capital indicator (⠠).
      - Punctuation uses PUNCTUATION_MAP.
      - Digits are prefixed with NUMBER_INDICATOR and then mapped via DIGIT_MAP.
      - Basic Grade‑2 contractions for common words.
    """
    # Split text into words so we can check for contractions
    words = text.split()
    converted_words = []
    for word in words:
        lower_word = word.lower()
        if lower_word in CONTRACTIONS:
            # Add capital indicator if the original word starts with uppercase
            if word[0].isupper():
                converted_words.append("⠠" + CONTRACTIONS[lower_word])
            else:
                converted_words.append(CONTRACTIONS[lower_word])
        else:
            converted_chars = []
            # We use a flag to check if the previous character was a digit
            prev_digit = False
            for ch in word:
                if ch.isalpha():
                    # Reset digit flag
                    prev_digit = False
                    if ch.isupper():
                        converted_chars.append("⠠" + BRAILLE_MAP.get(ch.lower(), ch))
                    else:
                        converted_chars.append(BRAILLE_MAP.get(ch, ch))
                elif ch.isdigit():
                    # If previous char was not a digit, add number indicator
                    if not prev_digit:
                        converted_chars.append(NUMBER_INDICATOR)
                    prev_digit = True
                    converted_chars.append(DIGIT_MAP.get(ch, ch))
                elif ch in PUNCTUATION_MAP:
                    converted_chars.append(PUNCTUATION_MAP[ch])
                    prev_digit = False
                else:
                    # For spaces or unknown characters, leave unchanged
                    converted_chars.append(ch)
                    prev_digit = False
            converted_words.append(''.join(converted_chars))
    return ' '.join(converted_words)

########################################################################
# PDF Extraction, Summarization, and Audio Generation Functions
########################################################################
def extract_text_from_pdf(pdf_path):
    extracted_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                width, height = page.width, page.height
                left_bbox = (0, 0, width / 2, height)
                right_bbox = (width / 2, 0, width, height)
                left_text = page.within_bbox(left_bbox).extract_text() or ""
                right_text = page.within_bbox(right_bbox).extract_text() or ""
                extracted_text += left_text.strip() + "\n" + right_text.strip() + "\n\n"
        return extracted_text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise

def summarize_text_with_bedrock(text):
    model_id = "us.meta.llama3-2-1b-instruct-v1:0"
    try:
        bedrock_client = boto3.client(
            "bedrock-runtime",
            region_name='us-east-1',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        text += " Summarize the above in 7 to 8 lines."
        prompt = (
            "You are a content summarization expert. Summarize the given content meaningfully without omitting important details."
            f"\n\nHuman:{text}\n\nAssistant:"
        )
        request_payload = {"prompt": prompt, "temperature": 0.5}
        response = bedrock_client.invoke_model(modelId=model_id, body=json.dumps(request_payload))
        model_response = json.loads(response["body"].read())
        return model_response.get("generation", "No summary generated.")
    except Exception as e:
        logging.error(f"Error summarizing text with Bedrock: {e}")
        raise

def convert_text_to_audio_with_polly(text, output_path):
    try:
        polly_client = boto3.client(
            "polly",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Joanna"
        )
        with open(output_path, "wb") as file:
            file.write(response["AudioStream"].read())
    except Exception as e:
        logging.error(f"Error converting text to audio with Polly: {e}")
        raise

########################################################################
# Flask Routes
########################################################################
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pdf = request.files.get("pdf")
        if not pdf or not allowed_file(pdf.filename):
            logging.warning("Invalid file upload attempt.")
            return "Invalid file type. Only PDF files are allowed.", 400
        
        try:
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
            pdf.save(pdf_path)
            logging.info(f"Saved PDF to {pdf_path}")
            
            # Extract text and summarize
            extracted_text = extract_text_from_pdf(pdf_path)
            logging.info("Extracted text from PDF.")
            summary = summarize_text_with_bedrock(extracted_text)
            logging.info("Summarized text with Bedrock.")
            
            # Generate audio for the summary
            audio_filename = f"{os.path.splitext(pdf.filename)[0]}.mp3"
            audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
            convert_text_to_audio_with_polly(summary, audio_path)
            logging.info(f"Generated audio at {audio_path}")
            
            # Convert summary to Braille using the enhanced conversion
            braille_text = convert_text_to_braille(summary)
            logging.info("Converted summary to Braille (with expanded mapping).")
            
            # Return the main page with results
            audio_url = url_for("static", filename=f"audio/{audio_filename}")
            return render_template(
                "index.html", 
                audio_url=audio_url,
                braille_text=braille_text,
                summary_text=summary,
                pdf_filename=pdf.filename  # pass original PDF name for the download route
            )
        
        except Exception as e:
            logging.error(f"An error occurred during processing: {e}")
            return "An error occurred while processing your request.", 500
    
    return render_template("index.html")

@app.route("/download_braille/<pdf_filename>", methods=["GET"])
# def download_braille(pdf_filename):
#     """
#     Convert the entire PDF text to Braille (using the enhanced map)
#     and generate a downloadable PDF file.
#     """
#     try:
#         pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
#         if not os.path.exists(pdf_path):
#             return "File not found.", 404
        
#         # Extract full text from the PDF
#         full_text = extract_text_from_pdf(pdf_path)
        
#         # Convert full text to Braille using the enhanced conversion
#         braille_full_text = convert_text_to_braille(full_text)
        
#         # Generate a PDF file with the Braille text
#         braille_pdf_filename = f"{os.path.splitext(pdf_filename)[0]}_braille.pdf"
#         braille_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], braille_pdf_filename)
        
#         pdf_doc = FPDF()
#         pdf_doc.add_page()
#         pdf_doc.set_font("Courier", size=12)
#         pdf_doc.multi_cell(0, 10, braille_full_text.replace('\r', ''))
#         pdf_doc.output(braille_pdf_path)
        
#         # Send the PDF as a downloadable file
#         return send_from_directory(app.config['UPLOAD_FOLDER'], braille_pdf_filename, as_attachment=True)
    
#     except Exception as e:
#         logging.error(f"Error in download_braille route: {e}")
#         return "Failed to generate Braille PDF.", 500






def download_braille(pdf_filename):
    try:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        if not os.path.exists(pdf_path):
            return "File not found.", 404

        full_text = extract_text_from_pdf(pdf_path)
        braille_full_text = convert_text_to_braille(full_text)

        braille_pdf_filename = f"{os.path.splitext(pdf_filename)[0]}_braille.pdf"
        braille_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], braille_pdf_filename)

        pdf_doc = FPDF()
        pdf_doc.add_page()

        # Use a font that supports Braille glyphs, e.g., NotoSansSymbols2
        font_path = os.path.join(app.root_path, "fonts", "NotoSansSymbols2-Regular.ttf")
        pdf_doc.add_font(fname=font_path, family="NotoSansSymbols2", uni=True)
        pdf_doc.set_font("NotoSansSymbols2", size=12)

        pdf_doc.multi_cell(0, 10, braille_full_text)
        pdf_doc.output(braille_pdf_path)

        return send_from_directory(app.config['UPLOAD_FOLDER'], braille_pdf_filename, as_attachment=True)

    except Exception as e:
        logging.error(f"Error in download_braille route: {e}", exc_info=True)
        return "Failed to generate Braille PDF.", 500
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8000)
