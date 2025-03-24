# Research Echopedia 🎤📚

**Transforming IEEE-format Research Papers into Concise, Portable Audio Summaries**

---

## 📖 Overview

The **Research Echopedia** project enhances the accessibility of IEEE-format research papers by converting their dense technical content into concise, portable audio summaries. This system uses a three-stage pipeline:  
1. **Text Extraction** with **pdfplumber**
2. **Summarization** with **AWS Bedrock's LLaMA model**
3. **Audio Conversion** using **Amazon Polly**

The downloadable audio outputs provide a flexible and engaging way to consume academic content on the go. By integrating advanced technologies, this solution bridges the gap in academic dissemination.

---

## ⚙️ Methodology

### 1️⃣ **Input and Parsing**  
The system accepts IEEE-format PDF papers, extracting text from both columns using **pdfplumber**.

- **Input Format Handling**: Supports PDF files, typical in academic dissemination.
- **Text Extraction**: Using pdfplumber to handle complex layouts with two columns, ensuring accurate content capture.
- **Preprocessing**: Text cleaning, normalization, and segmentation for effective summarization.

### 2️⃣ **Summarization**  
The preprocessed text is fed into **AWS Bedrock’s LLaMA model** to generate clear and concise summaries of the research paper.

- **Model Selection**: AWS LLaMA model optimized for academic summarization.
- **Summarization Process**: The text is formatted to generate a precise summary, retaining key insights.
  
### 3️⃣ **Audio Conversion**  
**Amazon Polly** is used to convert the summarized text into natural-sounding speech.

- **Audio Generation**: High-quality MP3 audio compatible across devices.
- **Audio Enhancement**: Volume normalization and trimming for improved listening experience.
- **Downloadable Audio**: Users can download the MP3 audio for offline access.

---

## 🛠️ Services Used

- **[AWS Bedrock](https://aws.amazon.com/bedrock/)**: Powerful AI models like LLaMA for text summarization.
- **[Amazon Polly](https://aws.amazon.com/polly/)**: Converts text to natural, human-like speech.
- **[Boto3](https://boto3.amazonaws.com/)**: AWS SDK for Python, enabling seamless interaction with AWS services.
- **[Azure Web Service](https://azure.microsoft.com/en-us/services/web-apps/)**: Platform-as-a-Service (PaaS) for hosting the Flask application.

---

## 🚀 Features

- **Custom Parsing Logic**: Tailored adjustments to pdfplumber for precise text extraction.
- **Error Handling**: Robust mechanisms to detect and handle issues during processing.
- **User-Friendly Interface**: Easy upload of PDF files, summary viewing, and audio download.
- **Configurable Summarization**: Customizable summary length and detail level.
- **Audio Playback**: Immediate audio playback functionality for instant listening.

---

## 🖼️ Workflow

![WorkFlow](https://github.com/user-attachments/assets/99cdd3c5-95a7-4c4c-b1df-e3f738e09902)

_The automated pipeline for text extraction, summarization, and audio conversion._

---

## 🏆 Results

The system effectively generates audio summaries from IEEE research papers, enhancing academic content accessibility. It allows users to consume complex research on-the-go, whether for study, research, or leisure.
![Results](https://github.com/user-attachments/assets/b5428672-7c18-4fd3-89ec-1eb4a2c100f0)


---

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/deepan484/Reasearch_Echopedia.git
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

