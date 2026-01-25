from datetime import datetime, timedelta
from anthropic import AsyncAnthropic, transform_schema
from app.models import internals, helpers
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

import litellm, os, asyncio

load_dotenv()

litellm.success_callback=["helicone"]

HELICONE_LLAVE=os.environ.get("HELICONE_API_KEY")

client = AsyncAnthropic(
  base_url="https://anthropic.helicone.ai",
  default_headers={
    "Helicone-Auth": f"Bearer {HELICONE_LLAVE}",
  },
)

async def call_claude(sistema,messages,tools,modelo,temperatura,tipo_funciones="auto",timeout_seconds:int=15):
  
  modelo_usar=helpers.COTRespuesta

  response_claude = await asyncio.wait_for(
      client.beta.messages.create(
          model=modelo,
          system=sistema,
          messages=messages,
          tools=tools,
          tool_choice={"type": tipo_funciones, "disable_parallel_tool_use": True},
          temperature=temperatura,
          max_tokens=12000
          #output_format={
          #   "type": "json_schema",
          #   "schema": transform_schema(modelo_usar)
          #},
          #betas=["structured-outputs-2025-11-13"]
      ),
      timeout=timeout_seconds
  )

  return response_claude