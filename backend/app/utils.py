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

"""Module for generic functions."""

import os
from concurrent import futures
import google.cloud.logging as gcp_logging


# Attach the Cloud Logging handler to the Python root logger
logging_client = gcp_logging.Client()
logging_client.setup_logging()

# Videos


def get_videos_bucket_base_path(story_id: str):
    """
    Constructs the base GCS bucket path for storing videos.

    This path includes a unique story ID to organize video segments for
    each specific project or execution.

    Args:
        story_id: The unique identifier for the story.

    Returns:
        A string representing the base GCS URI for video storage.
        Example: "gs://your-bucket-name/dreamboard/story_id_123/videos"
    """
    return f"gs://{os.getenv("GCS_BUCKET")}/dreamboard/{story_id}/videos"


def get_videos_bucket_folder_path(story_id: str):
    """
    Gets the folder path for videos within the bucket.

    Args:
        story_id: The unique identifier for the story.

    Returns:
        The folder path within the GCS bucket (e.g., "dreamboard/story_id/videos").
    """
    return f"dreamboard/{story_id}/videos"


def get_videos_local_base_path(story_id: str):
    """
    Gets the local base path where videos are stored in GCS.

    Args:
        story_id: The unique identifier for the story.

    Returns:
        The local file system path for videos.
    """
    return f"{os.getcwd()}/dreamboard/{story_id}/videos"


def get_videos_server_base_path(story_id: str):
    """
    Gets the local path where videos are stored on the server.

    Args:
        story_id: The unique identifier for the story.

    Returns:
        The server's file system path for videos, typically a mounted directory.
    """
    return f"{os.getcwd()}/app/mounted_files/dreamboard/{story_id}/videos"


def get_videos_gcs_fuse_path(story_id: str):
    """
    Gets the appropriate video output file path, local for dev or server for prod.

    Args:
        story_id: The unique identifier for the story.

    Returns:
        The GCS FUSE compatible path for video output, adapting for dev/prod.
    """
    # Download videos locally for dev
    if os.getenv("ENV") == "dev":
        return get_videos_local_base_path(story_id)
    else:
        return get_videos_server_base_path(story_id)


def get_videos_public_bucket_path(story_id: str):
    """
    Gets the public URL for the videos bucket (for local testing).

    Args:
        story_id: The unique identifier for the story.

    Returns:
        The public HTTP URL to access videos in the GCS bucket.
    """
    return f"https://storage.googleapis.com/{os.getenv("GCS_BUCKET")}/dreamboard/{story_id}/videos"


def get_scene_folder_path_from_uri(uri: str):
    """
    Extracts the scene folder path from a given URI.

    Example URI: bucket/dreamboard/story_id/scene_number/veo_gen_folder/sample_0.mp4
    Returns: scene_number (in dev) or scene_number/veo_gen_folder (in prod)

    Args:
        uri: The URI of the file.

    Returns:
        The extracted scene folder path.
    """
    uri_paths = uri.split("/")
    if os.getenv("ENV") == 'dev':
        scene_folder_path = uri_paths[len(uri_paths) - 2]
    else:
        scene_folder_path = uri_paths[len(uri_paths) - 3]

    return scene_folder_path


# Images


def get_images_local_base_path(story_id: str):
    """
    Gets the local base path where images are stored.

    Args:
        story_id: The unique identifier for the story.

    Returns:
        The local file system path for images.
    """
    return f"{os.getcwd()}/dreamboard/{story_id}/images"


def get_images_server_base_path(story_id: str):
    """
    Gets the server base path where images are stored.

    Args:
        story_id: The unique identifier for the story.

    Returns:
        The server's file system path for images, typically a mounted directory.
    """
    return f"{os.getcwd()}/app/mounted_files/dreamboard/{story_id}/images"


def get_images_gcs_fuse_path(story_id: str):
    """
    Gets the appropriate image output file path, local for dev or server for prod.

    Args:
        story_id: The unique identifier for the story.

    Returns:
        The GCS FUSE compatible path for image output, adapting for dev/prod.
    """
    # Download images locally for dev
    if os.getenv("ENV") == "dev":
        return get_images_local_base_path(story_id)
    else:
        return get_images_server_base_path(story_id)


def get_images_bucket_base_path(story_id: str):
    """
    Gets the base GCS bucket path for images.
    Includes a unique generation ID to identify images for each execution.
    """
    return f"gs://{os.getenv("GCS_BUCKET")}/dreamboard/{story_id}/images"


def get_images_bucket_folder_path(story_id: str):
    """
    Gets the folder path for images within the bucket.

    Args:
        story_id: The unique identifier for the story.

    Returns:
        The folder path within the GCS bucket (e.g., "dreamboard/story_id/images").
    """
    return f"dreamboard/{story_id}/images"


def get_images_public_bucket_path(story_id: str):
    """
    Gets the public URL for the images bucket (for local testing).

    Args:
        story_id: The unique identifier for the story.

    Returns:
        The public HTTP URL to access images in the GCS bucket.
    """
    return f"https://storage.googleapis.com/{os.getenv("GCS_BUCKET")}/dreamboard/{story_id}/images"


def get_images_bucket_folder(story_id: str):
    """
    Gets the parent folder name for images within the bucket.

    Args:
        story_id: The unique identifier for the story.

    Returns:
        The parent folder name (e.g., "dreamboard/story_id/images").
    """
    return f"dreamboard/{story_id}/images"


def get_images_bucket_path(story_id: str):
    """
    Gets the full GCS bucket path for images.
    Includes a unique generation ID to identify images for each execution.
    """
    return f"gs://{os.getenv("GCS_BUCKET")}/dreamboard/{story_id}/images"


def get_images_local_path(story_id: str):
    """
    Gets the local path where images are stored.

    Args:
        story_id: The unique identifier for the story.

    Returns:
        The local file system path for images, relative to the current working
        directory.
    """
    return f"dreamboard/{story_id}/images"


# Generic


def get_public_url_from_uri(auth_uri: str):
    """
    Gets the public URL from a GCS URI.

    Args:
        auth_uri: The GCS URI (e.g., "gs://my-bucket/path/to/file").

    Returns:
        The public HTTP URL to access the resource.
    """
    file_path = auth_uri.replace("gs://", "")
    return f"https://storage.googleapis.com/{file_path}"


def get_uri_from_public_url(public_uri: str):
    """
    Gets the GCS URI from a public URL.

    Args:
        public_uri: The public HTTP URL (e.g.,
                    "https://storage.googleapis.com/my-bucket/path/to/file").

    Returns:
        The GCS URI (e.g., "gs://my-bucket/path/to/file").
    """
    file_path = public_uri.replace("https://storage.googleapis.com/", "")
    return f"gs://{file_path}"


def get_file_name_from_uri(uri: str):
    """
    Gets the file name from a URI.

    Args:
        uri: The URI of the file.

    Returns:
        The extracted file name, or an empty string if not found.
    """
    uri_parts = uri.split("/")
    if len(uri_parts) > 1:
        # File name is the last element in the URI parts
        return f"{uri_parts[-1]}"
    return ""


def get_folder_path_from_uri(uri: str):
    """
    Gets the folder path from a URI.

    Args:
        uri: The URI of the file.

    Returns:
        The extracted folder path as a list of directory names.
    """
    folder_path = uri.replace("gs://", "")  # Remove GCS prefix
    uri_parts = folder_path.split("/")
    folder_path = uri_parts[0 : (len(uri_parts) - 2)]

    return folder_path


def get_full_path_from_uri(uri: str):
    """
    Gets the full path from a URI without the GCS prefix.

    Args:
        uri: The GCS URI of the file.

    Returns:
        The full path of the file within the bucket.
    """
    full_path = uri.replace("gs://", "")  # Remove GCS prefix

    return full_path


def get_signed_uri_from_gcs_uri(uri: str):
    """
    Converts a GCS URI to a signed URI.

    Args:
        uri: The GCS URI (e.g., "gs://my-bucket/path/to/file").

    Returns:
        A signed URI (e.g.,
        "https://storage.mtls.cloud.google.com/my-bucket/path/to/file").
    """
    return uri.replace("gs://", "https://storage.mtls.cloud.google.com/")


def get_gcs_uri_from_signed_uri(uri: str):
    """
    Converts a signed URI back to a GCS URI.

    Args:
        uri: The signed URI (e.g.,
             "https://storage.mtls.cloud.google.com/my-bucket/path/to/file").

    Returns:
        The GCS URI (e.g., "gs://my-bucket/path/to/file").
    """
    return uri.replace("https://storage.mtls.cloud.google.com/", "gs://")


def execute_tasks_in_parallel(tasks: list[any]) -> None:
    """
    Executes a list of tasks in parallel using a thread pool.

    Args:
        tasks: A list of callable tasks to be executed.

    Returns:
        A list of results from the executed tasks.
    """
    results = []
    with futures.ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            results.append(running_task.result())
    return results
