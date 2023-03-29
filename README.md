# MedNoteAI
 
![MedNoteAI screenshot](https://raw.githubusercontent.com/tig3r66/mednoteai/main/mednoteai.png)

The goal of MedNoteAI was to convert PDFs, audio, and video files into notes, and use the generated note to create multiple-choice questions and free-form Q&A exercises. In our data processing pipeline, we converted PDFs to text and transcribed audio files after splitting them into three-minute chunks. To transcribe videos, we first converted them to audio and then transcribed the resulting audio files after also dividing them into three-minute segments. This approach allowed us to efficiently process multiple transcripts in parallel. The transcription of the audio files was completed using Whisper, an open-source speech recognition tool created by OpenAI.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/tig3r66/mednoteai.git
cd mednoteai
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file and add your OpenAI API key as such (see `.env.example` for an example). You can get an API by following [these instructions](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key). Copy this file into the `mednoteai` and `soap_note` directories.

4.

*Run the MedNoteAI app*

```bash
cd mednoteai
python3 run app.py
```

*Run the SOAP note app*

```bash
cd soap_note
python3 run app.py
```
