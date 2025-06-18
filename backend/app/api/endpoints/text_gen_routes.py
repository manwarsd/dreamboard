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

"""
Text Generation endpoints handled by the FastAPI Router.

This module defines FastAPI endpoints for interacting with various text
generation services, including health checks, brainstorming scenes, and
generating/enhancing image and video prompts.
"""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from models.text import text_request_models
from models.text.text_gen_models import SceneItem
from services.text.text_generator import TextGenerator


def instantiate_text_generator() -> TextGenerator:
  """For use in generating a TextGenerator across all text routes"""
  return TextGenerator()


TextServiceDep = Annotated[TextGenerator, Depends(instantiate_text_generator)]

# Initialize the FastAPI router for text generation endpoints.
text_gen_router = APIRouter(prefix="/text_generation")


@text_gen_router.get("/text_health_check")
def text_health_check():
  """
  Endpoint to perform a health check for the Dreamboard text service.

  Returns:
      A JSON response indicating the status of the health check.
  """

  return {"status": "Success!"}


@text_gen_router.post("/brainstorm_scenes")
def brainstorm_scenes(
    brainstorm_scenes_request: text_request_models.BrainstormScenesRequest,
    text_generator: TextServiceDep,
) -> list[SceneItem]:
  """
  Brainstorms and generates a list of scene ideas based on user input.

  This endpoint takes an idea, brand guidelines, and desired number of
  scenes, then uses the `text_generator` to produce scene items.

  Args:
      brainstorm_scenes_request: A `BrainstormScenesRequest` object
                                 containing the idea, brand guidelines,
                                 and number of scenes.

  Returns:
      A list of `SceneItem` objects, each representing a brainstormed scene.

  Raises:
      HTTPException (500): If an error occurs during text generation.
  """
  try:
    gen_status = text_generator.brainstorm_scenes(
        brainstorm_scenes_request.idea,
        brainstorm_scenes_request.brand_guidelines,
        brainstorm_scenes_request.num_scenes,
    )
  except Exception as ex:
    logging.error("ERROR - text generation %s", str(ex))

    return Response(
        content=f"ERROR: {str(ex)}.  Please try again.",
        status_code=500,
    )
  return gen_status


@text_gen_router.post("/create_image_prompt_from_scene")
def create_image_prompt_from_scene(
    text_requests: text_request_models.TextRequest,
    text_generator: TextServiceDep,
) -> str:
  """
  Generates an image prompt based on a given scene description.

  Args:
      text_requests: A `TextRequest` object containing the scene description.

  Returns:
      A string representing the generated image prompt.

  Raises:
      HTTPException (500): If an error occurs during text generation.
  """
  try:
    gen_status = text_generator.create_image_prompt_from_scene(
        text_requests.scene
    )
  except Exception as ex:
    logging.error("ERROR - text generation %s", str(ex))

    return Response(
        content=f"ERROR: {str(ex)}.  Please try again.",
        status_code=500,
    )
  return gen_status


@text_gen_router.post("/create_video_prompt_from_scene")
def create_video_prompt_from_scene(
    text_requests: text_request_models.TextRequest,
    text_generator: TextServiceDep,
) -> str:
  """
  Generates a video prompt based on a given scene description.

  Args:
      text_requests: A `TextRequest` object containing the scene description.

  Returns:
      A string representing the generated video prompt.

  Raises:
      HTTPException (500): If an error occurs during text generation.
  """
  try:
    gen_status = text_generator.create_video_prompt_from_scene(
        text_requests.scene
    )
  except Exception as ex:
    logging.error("ERROR - text generation %s", str(ex))

    return Response(
        content=f"ERROR: {str(ex)}.  Please try again.",
        status_code=500,
    )
  return gen_status


@text_gen_router.post("/enhance_image_prompt")
def enhance_image_prompt(
    text_requests: text_request_models.TextRequest,
    text_generator: TextServiceDep,
) -> str:
  """
  Enhances an existing image prompt for improved generation quality.

  Args:
      text_requests: A `TextRequest` object containing the original prompt.

  Returns:
      A string representing the enhanced image prompt.

  Raises:
      HTTPException (500): If an error occurs during text generation.
  """
  try:
    gen_status = text_generator.enhance_image_prompt(text_requests.prompt)
  except Exception as ex:
    logging.error("ERROR - text generation %s", str(ex))

    return Response(
        content=f"ERROR: {str(ex)}.  Please try again.",
        status_code=500,
    )
  return gen_status


@text_gen_router.post("/enhance_image_prompt_with_scene")
def enhance_image_prompt_with_scene(
    text_requests: text_request_models.TextRequest,
    text_generator: TextServiceDep,
) -> str:
  """
  Enhances an image prompt using additional context from a scene.

  Args:
      text_requests: A `TextRequest` object containing the prompt and scene.

  Returns:
      A string representing the enhanced image prompt.

  Raises:
      HTTPException (500): If an error occurs during text generation.
  """
  try:
    gen_status = text_generator.enhance_image_prompt_with_scene(
        text_requests.prompt, text_requests.scene
    )
  except Exception as ex:
    logging.error("ERROR - text generation %s", str(ex))

    return Response(
        content=f"ERROR: {str(ex)}.  Please try again.",
        status_code=500,
    )
  return gen_status


@text_gen_router.post("/enhance_video_prompt")
def enhance_video_prompt(
    text_requests: text_request_models.TextRequest,
    text_generator: TextServiceDep,
) -> str:
  """
  Enhances an existing video prompt for improved generation quality.

  Args:
      text_requests: A `TextRequest` object containing the original prompt.

  Returns:
      A string representing the enhanced video prompt.

  Raises:
      HTTPException (500): If an error occurs during text generation.
  """
  try:
    text_generator = TextGenerator()
    gen_status = text_generator.enhance_image_prompt(text_requests.prompt)
  except Exception as ex:
    logging.error("ERROR - text generation %s", str(ex))

    return Response(
        content=f"ERROR: {str(ex)}.  Please try again.",
        status_code=500,
    )
  return gen_status


@text_gen_router.post("/enhance_video_prompt_with_scene")
def enhance_video_prompt_with_scene(
    text_requests: text_request_models.TextRequest,
    text_generator: TextServiceDep,
) -> str:
  """
  Enhances a video prompt using additional context from a scene.

  Args:
      text_requests: A `TextRequest` object containing the prompt and scene.

  Returns:
      A string representing the enhanced video prompt.

  Raises:
      HTTPException (500): If an error occurs during text generation.
  """
  try:
    gen_status = text_generator.enhance_video_prompt_with_scene(
        text_requests.prompt, text_requests.scene
    )
  except Exception as ex:
    logging.error("ERROR - text generation %s", str(ex))

    return Response(
        content=f"ERROR: {str(ex)}.  Please try again.",
        status_code=500,
    )
  return gen_status


@text_gen_router.post("/generate_image_prompts_from_scenes")
def generate_image_prompts_from_scenes(
    text_requests: text_request_models.TextRequest,
    text_generator: TextServiceDep,
) -> list[str]:
  """
  Generates multiple image prompts from a list of scene descriptions.

  Args:
      text_requests: A `TextRequest` object containing a list of scenes.

  Returns:
      A list of strings, where each string is an image prompt.

  Raises:
      HTTPException (500): If an error occurs during text generation.
  """
  try:
    gen_status = text_generator.generate_image_prompts_from_scenes(
        text_requests.scenes
    )
  except Exception as ex:
    logging.error("ERROR - text generation %s", str(ex))

    return Response(
        content=f"ERROR: {str(ex)}.  Please try again.",
        status_code=500,
    )
  return gen_status


@text_gen_router.post("/generate_video_prompts_from_scenes")
def generate_video_prompts_from_scenes(
    text_requests: text_request_models.TextRequest,
    text_generator: TextServiceDep,
) -> list[str]:
  """
  Generates multiple video prompts from a list of scene descriptions.

  Args:
      text_requests: A `TextRequest` object containing a list of scenes.

  Returns:
      A list of strings, where each string is a video prompt.

  Raises:
      HTTPException (500): If an error occurs during text generation.
  """
  try:
    gen_status = text_generator.generate_video_prompts_from_scenes(
        text_requests.scenes
    )
  except Exception as ex:
    logging.error("ERROR - text generation %s", str(ex))

    return Response(
        content=f"ERROR: {str(ex)}.  Please try again.",
        status_code=500,
    )
  return gen_status
