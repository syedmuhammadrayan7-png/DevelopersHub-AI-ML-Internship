# MediGuide AI
## Live Demo

[Open MediGuide AI]((https://mediguide-ai-rayan.streamlit.app/))
## Objective

MediGuide AI is a modern Streamlit chatbot for the AI/ML Engineering Internship Task 4: General Health Query Chatbot. It answers general health-related questions using prompt engineering, the Google Gemini API, emergency safety filtering, and a local fallback response system.

This project is designed for a polished internship submission while keeping medical safety and API key security at the center.

## Tools Used

- Python
- Streamlit
- python-dotenv
- Google Gemini API
- google-genai Python package

## Features

- Premium Streamlit interface with gradient styling, glassmorphism panels, and rounded chat bubbles
- Chat history using `st.session_state`
- Example question buttons for quick testing
- Reset chat button
- Sidebar with app details, safety notes, and current response mode
- Gemini-powered responses when an API key is configured
- Local fallback mode when the API key is missing or the API call fails
- Medical disclaimer included in responses

## Safety Handling

The app checks for emergency or dangerous medical phrases before calling Gemini. If an emergency phrase is detected, the app immediately returns an urgent safety response and does not send the message to the AI model.

Emergency examples include:

- chest pain
- heart attack
- cannot breathe
- severe bleeding
- unconscious
- stroke
- seizure
- overdose
- suicidal or suicide
- severe allergic reaction

The chatbot is designed to avoid diagnosis, prescriptions, and exact dosage instructions. It recommends consulting a qualified healthcare professional for serious, unusual, or persistent symptoms.

## Gemini API Integration

MediGuide AI uses the official `google-genai` package. The API key is read from the `GEMINI_API_KEY` environment variable with `python-dotenv`.

The app uses a safety-focused prompt created by:

```python
build_health_prompt(user_question)
```

The prompt instructs Gemini to provide simple general health information, avoid diagnosis, avoid prescribing medicine, avoid exact dosages, and include a medical disclaimer.

## Local Fallback Mode

If `GEMINI_API_KEY` is not available or the Gemini API call fails, the app still works using local fallback responses.

Fallback topics include:

- sore throat
- dehydration
- sleep
- paracetamol
- headache
- stress

Questions outside those topics receive a safe general response.

## Example Questions

1. What causes a sore throat?
2. What are symptoms of dehydration?
3. How can I improve sleep naturally?
4. Is paracetamol safe for children?
5. What can cause headaches?
6. How can I manage stress?

## How To Run The App

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file from `.env.example`:

```bash
GEMINI_API_KEY=your_api_key_here
```

3. Run the app:

```bash
streamlit run app.py
```

## Environment Variables

Create a `.env` file in the project folder:

```bash
GEMINI_API_KEY=your_api_key_here
```

Never hardcode the API key in `app.py`.

## GitHub Security Note

Do not upload `.env` to GitHub. This project includes `.env` in `.gitignore` and provides `.env.example` as a safe template.

If an API key is accidentally shared publicly, revoke or rotate it immediately in Google Cloud or Google AI Studio.

## Conclusion

MediGuide AI demonstrates a complete safety-aware health chatbot workflow with Streamlit, prompt engineering, Gemini API integration, emergency filtering, fallback responses, and secure environment variable handling.

## Disclaimer

MediGuide AI is for general health information only. It is not medical advice, does not diagnose conditions, does not prescribe medicine, and does not replace a doctor. For personal medical concerns, serious symptoms, or persistent symptoms, consult a qualified healthcare professional.
