import os
from tenacity import retry, stop_after_attempt, wait_fixed
import httpx

api_key = os.getenv("LEMONFOX_API_KEY")

def retry_on_failure():

  return retry(stop=stop_after_attempt(2), wait=wait_fixed(5))


async def transcribe_audio(audio_file, language: str = "spanish", response_format: str = "json"):

  url = "https://api.lemonfox.ai/v1/audio/transcriptions"
  headers = {"Authorization": f"Bearer {api_key}"}

  async with httpx.AsyncClient(timeout=300.0) as client:
    files = {}
    data = {
      "language": language,
      "response_format": response_format
    }

    if isinstance(audio_file, str):
      if audio_file.startswith("http"):
        data["file"] = audio_file
      else:
        files = {"file": open(audio_file, "rb")}
    elif isinstance(audio_file, bytes):
      files = {"file": ("audio.ogg", audio_file, "audio/ogg")}
    else:
      files = {"file": audio_file}

    try:
      response = await client.post(url, headers=headers, data=data, files=files)
      response.raise_for_status()

      if response_format == "json" or response_format == "verbose_json":
        result = response.json()
        return result.get("text", result)
      else:
        return response.text
    finally:
      if files and "file" in files and hasattr(files["file"], "close"):
        files["file"].close()