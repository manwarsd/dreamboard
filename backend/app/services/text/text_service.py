# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provides a service for interacting with the Gemini API for text generation."""

import logging
import os
import time
from dataclasses import dataclass, field

from google import genai
from google.api_core import exceptions
from google.genai import types


@dataclass
class LLMParameters:
  """
  Represents the parameters required to make a prediction to the LLM.

  These parameters control the model, location, and generation
  configuration for the Gemini API calls.
  """

  model_name: str = "gemini-2.0-flash-001"
  location: str = "us-central1"
  # modality: dict = field(default_factory= lambda: {
  #     "type": "text"
  # }) # Commented out as it's not currently used in the generation config.
  generation_config: types.GenerateContentConfig = field(
      default_factory=lambda: {
          "max_output_tokens": 8192,
          "temperature": 1,
          "top_p": 0.95,
          "top_k": 3,
      }
  )


# Default configuration for LLM parameters, used if none are explicitly
# provided.
DEFAULT_CONFIG = LLMParameters()


class TextService:
  """
  Service to interact with the Gemini API for text generation.

  This class handles the initialization of the Gemini client and provides
  methods to execute text generation requests with retry logic for common
  API errors.
  """

  client: genai.Client = None

  def __init__(self):
    """
    Initializes the TextService by setting up the Google Generative AI
    client.

    The client is configured to use Vertex AI and retrieves project ID and
    location from environment variables.
    """
    self.client = genai.Client(
        vertexai=True,
        project=os.getenv("PROJECT_ID"),
        location=os.getenv("LOCATION"),
    )

  def execute_gemini(
      self, prompt: str, llm_params: LLMParameters | None = None
  ) -> str:
    """
    Makes a request to Gemini to get a response based on the provided
    prompt.

    Includes retry logic with exponential backoff for transient errors
    like quota issues or service unavailability.

    Args:
        prompt: The text prompt to send to the Gemini model.
        llm_params: Optional `LLMParameters` to override default settings.

    Returns:
        A string with the generated response from Gemini, or an empty
        string if all retries fail or no response is received.
    """
    if not llm_params:
      llm_params = DEFAULT_CONFIG
    retries = 3  # Number of retries for API calls.
    for this_retry in range(retries):
      logging.info("retry #: %s for prompt %s", this_retry, prompt)
      try:
        # TODO: Make the config section dynamically use LLMParameters.
        # Currently hardcoded to default values.
        response = self.client.models.generate_content(
            model=LLMParameters.model_name,
            contents=[prompt],
            config=types.GenerateContentConfig(
                max_output_tokens=8192,
                temperature=1,
                top_p=0.95,
                top_k=1,
            ),
        )
        # TODO (ae) add system instructions if supported by API.
        return response.text if response else ""
      except exceptions.ResourceExhausted as ex:
        # Handle quota exhaustion errors with exponential backoff.
        logging.error("QUOTA RETRY: %s. ERROR %s ...", this_retry + 1, str(ex))
        wait = 10 * 2**this_retry  # Exponential backoff calculation.
        time.sleep(wait)
      except AttributeError as ex:
        # Handle specific attribute errors, possibly due to safety
        # filtering.
        error_message = str(ex)
        if "Content has no parts" in error_message:
          logging.error(
              (
                  "Error: %s Gemini might be blocking the response due "
                  "to safety issues. Retrying %s times using "
                  "exponential backoff. Retry number %s...\n"
              ),
              ex,
              retries,
              this_retry + 1,
          )
          wait = 10 * 2**this_retry
          time.sleep(wait)
        else:
          # Re-raise if it's an unhandled AttributeError.
          raise
      except Exception as ex:
        # Catch general exceptions for other API errors.
        logging.error("GENERAL EXCEPTION...\n")
        error_message = str(ex)
        # Check for common retriable API errors (quota, unavailable,
        # internal server error).
        if (
            "429 Quota exceeded" in error_message
            or "503 The service is currently unavailable" in error_message
            or "500 Internal error encountered" in error_message
        ):
          logging.error(
              (
                  "Error %s. Retrying %s times using exponential "
                  "backoff. Retry number %s...\n"
              ),
              error_message,
              retries,
              this_retry + 1,
          )
          wait = 10 * 2**this_retry
          time.sleep(wait)
        else:
          # Log and re-raise if the error is not retriable.
          logging.error(
              "ERROR: the following issue can't be retried: %s\n",
              error_message,
          )
          raise
    return ""  # Return empty string if all retries fail.

  def _get_modality_params(self, prompt: str, modality: str) -> list[any]:
    """
    Builds the modality parameters based on the type of LLM capability.

    Args:
        prompt: The text prompt.
        modality: The type of modality (e.g., "text").

    Returns:
        A list of content parts for the Gemini model.
    """
    if modality == "text":
      return [prompt]
    return []  # Return empty list if modality is not "text".
