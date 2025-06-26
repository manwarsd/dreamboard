from google.adk.agents import BaseAgent
from google.adk.runners import Runner
from google.genai import types
from pydantic import BaseModel

import os
from .db_agent_service import DBAgentService
from google.adk.artifacts import InMemoryArtifactService  # Or GcsArtifactService
from .session_service import SessionService


class AgentResponse(BaseModel):
  text: str | None
  text_string: str | None = None
  image_byte_string: str | None = None
  video_byte_string: str | None = None


# TODO: DRY this out with agent_request_service and a base class
class DBAgentRequestService:

  def __init__(
      self,
  ):
    """Retrieves an agent response from the specified agent

    Args:
        agent_service
    """
    self.app_name = os.getenv("APP_NAME", "Don Draper Bot")
    self.db_agent_service = DBAgentService()
    self.session_service = SessionService()

  async def request_agent_response(
      self,
      user_id: str,
      session_id: str,
      message: str,
  ) -> AgentResponse:
    """Sends a query to the LLM agent and returns the final response.

    Args:
        root_agent_name: The name of the root agent.
        runner: The ADK runner
        user_id: The user ID
        session_id: The session ID
        message: The message to send to the agent

    Returns:
      AgentResponse: The final response from the agent.
    """
    root_agent = self.db_agent_service.initialize_root_ml_agent()
    await self.initialize_agent_runner(user_id, session_id, root_agent)
    return await self.call_agent_async(message, user_id, session_id)

  async def initialize_agent_runner(
      self, user_id: str, session_id: str, root_agent: BaseAgent
  ) -> None:
    """Starts an agent session and then creates a Runner and assigns it to the object

    Args:
        user_id: The user ID
        session_id: The session ID

    """

    # TODO: can pass in initial state here
    # TODO: do we actually need to initialize the session here or should we do it in the call_agent_async method?
    _ = await self.session_service.get_or_create_session(user_id, session_id)

    # Create a Runner
    self.runner = Runner(
        app_name=self.app_name,
        agent=root_agent,
        session_service=self.session_service.get_session_service(),
        artifact_service=InMemoryArtifactService(),
    )

  def get_runner(self) -> Runner:
    """Gets the current runner assigned to the object"""
    if self.runner is None:
      raise ValueError("Agent runner not initialized")

    return self.runner

  async def call_agent_async(
      self, query: str, user_id: str, session_id: str
  ) -> AgentResponse:
    """Sends a query to the LLM agent and prints the final response.

    Args:
        query: The message to send to the agent
        user_id: The user ID
        session_id: The session ID

    Returns:
      AgentResponse: The final response from the agent.

    """
    print(f"\n>>> User Query: {query}")

    # Prepare the user's message in ADK format
    content = types.Content(role="user", parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response."  # Default
    # Key Concept: run_async executes the agent logic and yields Events.
    # We iterate through events to find the final answer.
    async for event in self.runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
      # You can uncomment the line below to see *all* events during execution
      print(
          f"  [Event] Author: {event.author}, Type: {type(event).__name__},"
          f" Final: {event.is_final_response()}, Content: {event.content}"
      )

      # Key Concept: is_final_response() marks the concluding message for the turn.
      if event.is_final_response():
        if event.content and event.content.parts:
          # Assuming text response in the first part
          final_response_text = event.content.parts[0].text
        elif (
            event.actions and event.actions.escalate
        ):  # Handle potential errors/escalations
          final_response_text = (
              "Agent escalated:"
              f" {event.error_message or 'No specific message.'}"
          )
        # Add more checks here if needed (e.g., specific error codes)
        break  # Stop processing events once the final response is found

    return AgentResponse(text=final_response_text)
