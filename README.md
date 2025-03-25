# EchoVision 🎤📚

**Enhancing Accessibility for the Visually Impaired through Audio and Braille Summaries**

---

## 📖 Overview

The **EchoVision** project helps visually impaired individuals by converting text-based documents into concise, portable audio summaries. It also provides Braille PDFs of these summaries, which can be printed using Braille printers. This system uses a three-stage pipeline:
1. **Text Extraction** with **pdfplumber**
2. **Summarization** with **AWS Bedrock's LLaMA model**
3. **Audio Conversion** using **Amazon Polly** (with Braille PDF generation)

The downloadable audio and Braille outputs provide a flexible and engaging way to consume content on the go, enhancing accessibility and independence.

---

## ⚙️ Methodology

### 1️⃣ **Input and Parsing**  
The system accepts PDF documents, extracting text efficiently using **pdfplumber**.

- **Input Format Handling**: Supports various text-based PDF files.
- **Text Extraction**: Uses pdfplumber to accurately capture document content.
- **Preprocessing**: Text cleaning, normalization, and segmentation for effective summarization.

### 2️⃣ **Summarization**  
The preprocessed text is fed into **AWS Bedrock’s LLaMA model** to generate clear and concise summaries.

- **Model Selection**: AWS LLaMA model optimized for text summarization.
- **Summarization Process**: The text is formatted to generate a precise summary, retaining key insights.

### 3️⃣ **Audio Conversion and Braille PDF Generation**  
**Amazon Polly** is used to convert the summarized text into natural-sounding speech, while Braille PDFs of the summaries are also generated for printing with Braille printers.

- **Audio Generation**: High-quality MP3 audio compatible across devices.
- **Audio Enhancement**: Volume normalization and trimming for improved listening experience.
- **Downloadable Outputs**: Users can download both the MP3 audio and Braille PDFs for offline access.

---

## 🛠️ Services Used

- **[AWS Bedrock](https://aws.amazon.com/bedrock/)**: Powerful AI models like LLaMA for text summarization.
- **[Amazon Polly](https://aws.amazon.com/polly/)**: Converts text to natural, human-like speech.
- **[Boto3](https://boto3.amazonaws.com/)**: AWS SDK for Python, enabling seamless interaction with AWS services.
- **[Azure Web App Services](https://azure.microsoft.com/en-us/services/app-service/web/)**: Hosting the Flask application.

---

## 🚀 Features

- **Custom Parsing Logic**: Tailored adjustments to pdfplumber for precise text extraction.
- **Error Handling**: Robust mechanisms to detect and handle issues during processing.
- **User-Friendly Interface**: Easy upload of PDF files, summary viewing, and downloadable outputs.
- **Configurable Summarization**: Customizable summary length and detail level.
- **Audio Playback**: Immediate audio playback functionality for instant listening.
- **Braille PDF Generation**: Creates Braille PDFs of the summaries for printing with Braille printers.

---

## 🏆 Results

The system effectively generates both audio summaries and Braille PDFs, making textual content more accessible for visually impaired individuals. It allows users to consume important information on the go, fostering greater independence and inclusivity.

---

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/deepan484/Research_Echopedia.git
   ```
   
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your AWS and Azure credentials for integration.

4. Run the app:
   ```bash
   python app.py
   ```

