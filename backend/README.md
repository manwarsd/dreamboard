# DreamBoard Backend Code

This directory contains the backend code to run the AI text/image/video generation services of DreamBoard.  The code is to be deployed on GCP as a Cloud Function and accessed as an API.

# Structure

The general folder structure is as follows under backend/app:
- api: Contains backend API routing code.
  - endpoints: Endpoints for each type of AI generation (text, image, video).
- core: Contains configuration of the backend server.
- dreamboard: (optional) Folder used for local/development environments.  Environment variable must be set to "DEV" to use this folder.
- models: Contains API request and response objects for text/image/video.
- prompts: Prompts used to for text/image/video generation.
- services: Actual code that runs the generation.
- tests: Directory for test cases.

# Installation
Installation on production is done by deploying deploy_backend.sh.  Locally, this code can run with the following commands in a Linux-based CLI: 

- gcloud auth application-default login
- export PROJECT_ID=<YOUR_PROJECT_ID>
- export LOCATION=<YOUR_PROJECT_LOCATION>
- export GCS_BUCKET=<YOUR_GCS_BUCKET>
- export ENV=dev
- fastapi dev main.py

## Requirements
- A project with access to the following:
  - Veo3
  - Imagen4
  - Gemini
  - Cloud Storage FUSE
  - Cloud Storage Bucket
- A service account to run the Cloud Function and AI generation.
- A GCS bucket created to store the image and video results.


## Install and Setup Requirements

## Update Config Settings and Install Into GCP
Edit Line 135-142 deploy_backend.sh with the information from the previous step.
