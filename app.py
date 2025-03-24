from flask import Flask, render_template, request, send_from_directory, url_for
import os
import boto3
import pdfplumber
import json
import logging
from dotenv import load_dotenv
import requests  # For Google API calls

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)  

# Configuration
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
AUDIO_FOLDER = os.getenv("AUDIO_FOLDER", "static/audio")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # New Google API key

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

def convert_text_to_braille(text, api_key):
    """Convert text to Braille using Google's Text-to-Speech API"""
    try:
        url = "https://texttospeech.googleapis.com/v1/text:synthesize"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key
        }
        
        payload = {
            "input": {
                "text": text
            },
            "voice": {
                "languageCode": "en-US"
            },
            "audioConfig": {
                "audioEncoding": "LINEAR16",
                "speakingRate": 1.0
            },
            "enableBraille": True  # Request Braille output
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        braille_text = data.get("braille", {}).get("braille", "Braille conversion failed")
        return braille_text
        
    except Exception as e:
        logging.error(f"Error converting text to Braille: {e}")
        return "Braille conversion unavailable"

# Extract text from PDF
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

# Summarize text using AWS Bedrock
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

# Convert text to audio using Polly
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
            
            # Generate audio
            audio_filename = f"{os.path.splitext(pdf.filename)[0]}.mp3"
            audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
            convert_text_to_audio_with_polly(summary, audio_path)
            logging.info(f"Generated audio at {audio_path}")
            
            # Convert to Braille
            braille_text = convert_text_to_braille(summary, GOOGLE_API_KEY)
            logging.info("Converted summary to Braille.")
            
            # Return page with audio and braille
            audio_url = url_for("static", filename=f"audio/{audio_filename}")
            return render_template(
                "index.html", 
                audio_url=audio_url,
                braille_text=braille_text,
                summary_text=summary
            )
        
        except Exception as e:
            logging.error(f"An error occurred during processing: {e}")
            return "An error occurred while processing your request.", 500
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8000)