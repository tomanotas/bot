from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class MessageText(BaseModel):
    body: str


class MessageAudio(BaseModel):
    id: str
    mime_type: str | None = None
    sha256: str | None = None
    voice: bool | None = None


class MessageImage(BaseModel):
    id: str
    mime_type: str | None = None
    sha256: str | None = None
    caption: str | None = None

class KapsoMediaData(BaseModel):
    url: str = Field(description="Direct URL to download the media")
    filename: str = Field(description="Original filename (e.g., 'voice.ogg', 'photo.jpg')")
    content_type: str = Field(description="MIME type (e.g., 'audio/ogg', 'image/jpeg')")
    byte_size: int = Field(description="File size in bytes")

class KapsoTranscript(BaseModel):
    text: str

class KapsoMessageTypeData(BaseModel):
    caption: str | None = None
    has_media: bool | None = None

class MessageKapso(BaseModel):
    direction: str | None = Field(default=None, description="Message direction: 'inbound' or 'outbound'")
    status: str | None = Field(default=None, description="Message status: 'received', 'sent', etc.")
    processing_status: str | None = Field(default=None, description="Processing status: 'pending', 'completed'")
    origin: str | None = Field(default=None, description="Message origin: 'cloud_api', etc.")
    has_media: bool | None = Field(default=None, description="Whether the message contains media")
    content: str | None = Field(default=None, description="Formatted content string with media info")

    transcript: KapsoTranscript | None = Field(default=None, description="Audio transcript (Kapso transcribes audio)")

    media_url: str | None = Field(default=None, description="Direct URL to download media")
    media_data: KapsoMediaData | None = Field(default=None, description="Media metadata including URL")

    message_type_data: KapsoMessageTypeData | None = Field(default=None, description="Type-specific metadata")


class Conversation(BaseModel):
    id: str
    origin: dict | None = None
    expiration_timestamp: str | None = None

class BatchInfo(BaseModel):
    size: int = Field(description="Number of messages in the batch")
    window_ms: int = Field(description="Buffer window in milliseconds")
    sequences: list[int] | None = Field(default=None, description="Sequence numbers of batched messages")

class KapsoContact(BaseModel):
    wa_id: str = Field(description="WhatsApp ID of the contact")
    profile: dict | None = Field(default=None, description="Profile information")


class KapsoMessage(BaseModel):
    id: str = Field(description="Message ID")
    from_: str = Field(alias="from", description="Sender's WhatsApp ID")
    text: MessageText | None = Field(default=None, description="Text message content")
    audio: MessageAudio | None = Field(default=None, description="Audio message content")
    image: MessageImage | None = Field(default=None, description="Image message content")
    type: str = Field(description="Message type: text, image, audio, etc.")
    kapso: MessageKapso | None = Field(default=None, description="Kapso-specific metadata")
    context: Any | None = Field(default=None, description="Message context for replies")
    timestamp: str = Field(description="Unix timestamp of the message")


class WebhookDataItem(BaseModel):
    message: KapsoMessage = Field(description="The message object")
    conversation: Conversation | None = Field(default=None, description="Conversation context")
    phone_number_id: str = Field(description="Phone number ID receiving the message")
    is_new_conversation: bool = Field(default=False, description="Whether this is a new conversation")
    contacts: list[KapsoContact] | None = Field(default=None, description="Contact information")


class KapsoWebhookPayload(BaseModel):
    data: list[WebhookDataItem] = Field(description="List of buffered messages")
    type: str = Field(description="Webhook event type")
    batch: bool = Field(default=False, description="Whether this is a batched payload")
    batch_info: BatchInfo | None = Field(default=None, description="Batch metadata when batch=true")

