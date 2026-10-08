# Traced App

This project demonstrates a simple Python application that sends multiple prompts to Gemini using LangChain and prints each response. It is set up to make it easy to observe model runs and inspect traces through LangSmith.

## Overview

The app in `traced_app.py` does the following:

- Creates a Gemini chat model with `ChatGoogleGenerativeAI`
- Defines three example prompts
- Calls the model for each prompt
- Prints the prompt and returned answer

## Files

- `traced_app.py` — main application logic
- `Run1_Results.png` — example output for run 1
- `Run1_Tracing.png` — trace view for run 1
- `Run2_Results.png` — example output for run 2
- `Run2_Tracing.png` — trace view for run 2
- `Run3_Results.png` — example output for run 3
- `Run3_Tracing.png` — trace view for run 3
- `Tracing_LangSmith.png` — LangSmith tracing overview

## Requirements

- Python 3.9+
- A Google API key with access to Gemini
- The `langchain-google-genai` package

## Setup

1. Install dependencies:

   ```bash
   pip install langchain-google-genai
   ```

2. Set your Google API key:

   ```bash
   set GOOGLE_API_KEY=your_api_key_here
   ```

   On macOS/Linux:

   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```

## Run the app

```bash
python traced_app.py
```

The script will print three prompts and the model responses to the console.

## Notes

This example is useful for learning how to:

- connect to Google Gemini through LangChain
- run multiple prompts in sequence
- track model execution and inspect traces in LangSmith

If you are using LangSmith tracing, make sure your LangSmith environment variables are also configured so the traces are published correctly.
