# EchoVision 🎤📚

**Enhancing Accessibility for the Visually Impaired through Audio and Braille Summaries**

---

## 📖 Overview

The **EchoVision** project helps visually impaired individuals by converting text-based documents into concise, portable audio summaries. It also provides Braille PDFs of these summaries, which can be printed using Braille printers. This system uses a three-stage pipeline:

1. **Text Extraction** with **pdfplumber**
2. **Summarization** with **AWS Bedrock's LLaMA model**
3. **Audio Conversion and Braille PDF Generation** using **Amazon Polly**

The downloadable audio and Braille outputs offer a flexible and engaging way to consume content on the go, enhancing accessibility and independence.

---

## ⚙️ Methodology

### 1️⃣ Input and Parsing

The system accepts PDF documents and extracts text efficiently using **pdfplumber**.

- **Input Format Handling:** Supports various text-based PDF files.
- **Text Extraction:** Uses pdfplumber to accurately capture document content.
- **Preprocessing:** Involves text cleaning, normalization, and segmentation for effective summarization.

### 2️⃣ Summarization

The preprocessed text is fed into **AWS Bedrock’s LLaMA model** to generate clear and concise summaries.

- **Model Selection:** AWS LLaMA model optimized for text summarization.
- **Summarization Process:** Formats the text to generate precise summaries that retain key insights.

### 3️⃣ Audio Conversion and Braille PDF Generation

**Amazon Polly** is used to convert the summarized text into natural-sounding speech, while Braille PDFs are generated for printing with Braille printers.

- **Audio Generation:** Produces high-quality MP3 audio compatible across devices.
- **Audio Enhancement:** Includes volume normalization and trimming for improved listening.
- **Downloadable Outputs:** Users can download both the MP3 audio and Braille PDFs for offline use.

---

## 🗺️ Workflow

Below is a visual overview of the EchoVision pipeline, illustrating how the system processes PDF files into Braille and audio outputs:

![Flow Chart](/images/image-6.png)
_Flow chart depicting the conversion of an input PDF into text, summarizing it, then converting it either to Braille (and generating a Braille PDF) or audio._

---

## 🛠️ Services Used

- **[AWS Bedrock](https://aws.amazon.com/bedrock/)**: Provides powerful AI models like LLaMA for summarization.
- **[Amazon Polly](https://aws.amazon.com/polly/)**: Converts text to natural, human-like speech.
- **[Boto3](https://boto3.amazonaws.com/)**: AWS SDK for Python for seamless AWS service interaction.
- **[Azure Web App Services](https://azure.microsoft.com/en-us/services/app-service/web/)**: Hosts the Flask application.

---

## 🚀 Features

- **Custom Parsing Logic:** Tailored adjustments to pdfplumber for precise text extraction.
- **Error Handling:** Robust mechanisms to detect and handle issues during processing.
- **User-Friendly Interface:** Simple upload of PDF files, summary viewing, and access to downloadable outputs.
- **Configurable Summarization:** Customizable summary length and detail level.
- **Audio Playback:** Immediate playback functionality for quick listening.
- **Braille PDF Generation:** Creates Braille PDFs of the summaries for printing with Braille printers.

---

## 🏆 Results

EchoVision effectively generates both audio summaries and Braille PDFs, making textual content more accessible for visually impaired individuals. The system fosters greater independence and inclusivity by providing essential outputs that can be used on the go.

---

## 🔧 Installation

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aiyyappann/EchoVision.git
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

---

## 🖼️ Visual Walkthrough

1. **Landing Page**  
   ![Landing Page](/images/image.png)  
   _The landing page welcomes users._

2. **File Upload**  
   ![File Upload](/images/image-1.png)  
   _Uploading a file to be processed._

3. **Audio Summary**  
   ![Audio Summary](/images/image-2.png)  
   _Generated audio summary of the file._

4. **Braille Display**  
   ![Braille Display](/images/image-3.png)  
   _Preview of the Braille content._

5. **Braille PDF Download**  
   ![Braille PDF Download](/images/image-4.png)  
   _Downloaded Braille PDF ready for printing._
