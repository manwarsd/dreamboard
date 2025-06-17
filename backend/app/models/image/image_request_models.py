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
Module for the Data models used by the APIRouter to define the request
parameters.

This file defines Pydantic models specifically for structuring incoming
request payloads related to image generation via the API Router.
"""

from models import request_models
from pydantic import BaseModel


class ImageRequest(BaseModel):
    """
    Represents the basic structure for an Imagen API request.

    This model encapsulates a collection of `Scene` objects, where each
    scene contains the necessary parameters for image generation or editing.

    Attributes:
        scenes: A list of `Scene` objects, each defining a specific
                image generation task.
    """

    scenes: list[request_models.Scene]
