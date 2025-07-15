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

This file defines Pydantic models for structuring incoming request
payloads related to video generation, including video segments, creative
direction, and transitions.
"""

from enum import Enum

from pydantic import BaseModel, Field


class VideoTransition(Enum):
  """
  Enum to represent available video transition types.

  These transitions define how one video segment flows into the next.
  """

  X_FADE = "X_FADE"
  WIPE = "WIPE"
  ZOOM = "ZOOM"
  ZOOM_WARP = "ZOOM_WARP"
  DIP_TO_BLACK = "DIP_TO_BLACK"
  CONCATENATE = "CONCATENATE"
  BLUR = "BLUR"
  SLIDE = "SLIDE"
  SLIDE_WARP = "SLIDE_WARP"
  FLICKER = "FLICKER"


class VideoTransitionRequest(BaseModel):
  """
  Represents a request for a specific transition between two video segments.

  Attributes:
      type: The type of video transition to apply. Defaults to "X_FADE".
  """

  type: VideoTransition | None = "X_FADE"


class VideoCreativeDirectionRequest(BaseModel):
  """
  Represents the overall creative direction for a video generation task.

  Attributes:
      transitions: A list of `VideoTransition` enums. The order in this
                   list defines the sequence in which transitions will be
                   applied between video segments. Defaults to an empty list.
  """

  transitions: list[VideoTransition] | None = []


class VideoItem(BaseModel):
  """
  Represents a video asset, typically used as an input or selection.

  Attributes:
      name: The name of the video file.
      gcs_uri: The Google Cloud Storage (GCS) URI of the video.
      signed_uri: A pre-signed URL for temporary public access to the video.
      gcs_fuse_path: The FUSE path if the GCS bucket is mounted locally.
      mime_type: The MIME type of the video (e.g., 'video/mp4').
  """

  name: str
  gcs_uri: str
  signed_uri: str
  gcs_fuse_path: str
  mime_type: str


class ImageItem(BaseModel):
  """
  Represents an image asset, typically used as a seed image for video
  generation.

  Attributes:
      name: The name of the image file.
      gcs_uri: The Google Cloud Storage (GCS) URI of the image.
      signed_uri: A pre-signed URL for temporary public access to the image.
      gcs_fuse_path: The FUSE path if the GCS bucket is mounted locally.
      mime_type: The MIME type of the image (e.g., 'image/jpeg').
  """

  name: str
  gcs_uri: str
  signed_uri: str
  gcs_fuse_path: str
  mime_type: str


class VideoSegmentRequest(BaseModel):
  """
  Represents a single segment within a larger video generation request.

  Each segment can specify its own prompt, seed image, and generation
  parameters.

  Attributes:
      scene_id: The unique identifier for the scene associated with this
                video segment.
      segment_number: The sequential number of this video segment.
      prompt: The text prompt for generating this video segment.
      seed_image: An optional `ImageItem` to be used as a visual starting
                  point for this segment's generation.
      regenerate_video_segment: A boolean flag indicating if this segment
                                should be regenerated. Defaults to `False`.
      duration_in_secs: The desired duration of the video segment in
                        seconds. Defaults to 8.
      aspect_ratio: The aspect ratio of the video segment (e.g., "16:9").
                    Defaults to "16:9".
      frames_per_sec: The desired frames per second for the video segment.
                      Defaults to 24.
      person_generation: Controls the generation of human figures
                         (e.g., "allow_adult"). Defaults to "allow_adult".
      sample_count: The number of video samples to generate for this
                    segment. Defaults to 1.
      seed: An optional integer seed for reproducible video generation.
      negative_prompt: An optional prompt specifying elements to avoid in
                       the generated video.
      transition: An optional `VideoTransition` type to apply before
                  this segment.
      enhance_prompt: A boolean indicating whether to automatically enhance
                      the input prompt. Defaults to `True`.
      use_last_frame: A boolean flag to use the last frame of the previous
                      segment as a starting point. Defaults to `False`.
      include_video_segment: A boolean flag to include this segment in the
                             final video. Defaults to `True`.
      generate_video_frames: A boolean flag to indicate if individual
                             frames should be generated. Defaults to `False`.
      selected_video: An optional `VideoItem` if an existing video is to
                      be used for this segment.
  """

  scene_id: str
  segment_number: int
  prompt: str
  seed_image: ImageItem | None = None
  regenerate_video_segment: bool = False
  duration_in_secs: int | None = 8
  aspect_ratio: str | None = "16:9"
  frames_per_sec: int | None = 24
  person_generation: str | None = "allow_adult"
  sample_count: int | None = 1
  seed: int | None = None
  negative_prompt: str | None = None
  transition: VideoTransition | None = None
  enhance_prompt: bool | None = True
  use_last_frame: bool | None = False
  include_video_segment: bool | None = True
  generate_video_frames: bool | None = False
  selected_video: VideoItem | None = None
  generate_audio: bool | None = False


class VideoGenerationRequest(BaseModel):
  """
  Represents the complete request for a video generation task.

  This model encapsulates all the individual video segments and overall
  creative direction for the video.

  Attributes:
      video_segments: A list of `VideoSegmentRequest` objects, defining
                      each part of the video.
      creative_direction: An optional `VideoCreativeDirectionRequest`
                          object specifying overall video creative settings.
                          Currently, this might be empty.
  """

  video_segments: list[VideoSegmentRequest]
  creative_direction: VideoCreativeDirectionRequest | None = None

class LogoOverlayOptions(BaseModel):
  """
  Represents options for overlaying a logo on a generated video.

  Attributes:
      start_time: The time (in seconds) when the logo should appear.
      duration: The duration (in seconds) the logo should be visible.
      width: The width of the logo in pixels.
      height: The height of the logo in pixels.
      x_position: The x position (top left corner) of the logo on the clip in pixels.
      y_position: The y position (top right corner) of the logo on the clip in pixels.
  """

  start_time: int
  duration: int
  width: int
  height: int
  x_position: int
  y_position: int

class LogoOverlay(BaseModel):
  """
  Represents a single logo overlay to be applied to a video.
  Attributes:
      gcs_logo_path: The GCS URI of the logo image.
      options: Details about how the overlay should be applied.
  """

  gcs_logo_path: str
  options: LogoOverlayOptions = Field(default_factory=LogoOverlayOptions)

class LogoOverlayRequest(BaseModel):
  """
  Represents a request to apply a logo overlay to a video.
  Attributes:
      gcs_video_path: The GCS URI of the input video.
      logo_overlay: The logo overlay to be applied to the video.
  """
  gcs_video_path: str
  logo_overlay: LogoOverlay = Field(default_factory=LogoOverlay)