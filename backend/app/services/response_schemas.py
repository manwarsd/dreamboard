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

"""Module to define JSON response schemas for Gemini requests."""

RESPONSE_SCHEMAS = {
    # Schema for creating new scenes
    "CREATE_SCENES": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "number": {
                    "type": "integer",  # Scene number
                },
                "description": {
                    "type": "string",  # Textual description of the scene
                },
                "image_prompt": {
                    "type": "string",  # Prompt for generating an image
                },
                "video_prompt": {
                    "type": "string",  # Prompt for generating a video
                },
            },
            # Required fields for each scene object
            "required": [
                "number",
                "description",
                "image_prompt",
                "video_prompt",
            ],
        },
    },
    # Schema for creating scenes with brand guideline alignment
    "CREATE_SCENES_WITH_BRAND_GUIDELINES": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "number": {
                    "type": "integer",  # Scene number
                },
                "description": {
                    "type": "string",  # Textual description of the scene
                },
                "brand_guidelines_alignment": {
                    "type": "string",  # How scene aligns with brand guidelines
                },
                "image_prompt": {
                    "type": "string",  # Prompt for generating an image
                },
            },
            # Required fields for each scene object with brand guidelines
            "required": [
                "number",
                "description",
                "brand_guidelines_alignment",
                "image_prompt",
            ],
        },
    },
    # Schema for a simple text response
    "JUST_TEXT": {"type": "string"},
}
