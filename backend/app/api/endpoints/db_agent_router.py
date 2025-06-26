from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from services.agent.db_agent_request_service import DBAgentRequestService

router = APIRouter(
    prefix="/db_agent",
    responses={404: {"description": "Not found"}},
)


class AgentRequest(BaseModel):
  agent_name: str
  message: str
  session_id: str
  user_id: str


@router.post("/request")
async def request_agent_response(
    agent_name: str = Form(...),
    message: str = Form(...),
    user_id: str = Form(...),
    session_id: str = Form(...),
):

  db_agent_request_service = DBAgentRequestService()
  # Get the agent's response
  response = await db_agent_request_service.request_agent_response(
      user_id,
      session_id,
      message,
  )

  # Convert the response to speech
  # if return_audio_response and response.text:
  #     audio_content = await text_to_speech_service.text_to_speech(response.text)
  # else:
  #     audio_content = None
  audio_content = None

  # Return both the text response and audio content
  return JSONResponse(
      content={
          "text": response.text,
      }
  )
