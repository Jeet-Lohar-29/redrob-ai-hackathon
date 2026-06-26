from concurrent.futures import ThreadPoolExecutor, TimeoutError
from google import genai
from dotenv import load_dotenv
import os
import time
from typing import Optional

import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None
client = None


def _get_gemini_client():
    global client
    if client is None:
        if not API_KEY:
            raise ValueError("No Gemini API key configured.")
        client = genai.Client(api_key=API_KEY)
    return client


def _call_gemini(prompt: str) -> str:
    client = _get_gemini_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    text = getattr(response, "text", None)
    if not text:
        raise ValueError("Gemini returned empty text")
    return str(text).strip()


def ask_gemini(prompt: str, retries: int = 3, backoff: float = 1.0, timeout: float = 20.0) -> str:
    if not API_KEY:
        return "Gemini Error: API key not configured."

    for attempt in range(1, retries + 1):
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_call_gemini, prompt)
                return future.result(timeout=timeout)
        except TimeoutError:
            if attempt == retries:
                return "Gemini Error: request timed out"
            time.sleep(backoff * attempt)
        except Exception as exc:
            if attempt == retries:
                return f"Gemini Error: {exc}"
            time.sleep(backoff * attempt)

    return "Gemini Error: retry failed"
