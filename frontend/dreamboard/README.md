# DreamBoard Frontend Code

This directory contains the frontend code to run the Angular UI of DreamBoard.  The code is to be hosted on a Google Cloud Platform (GCP) Cloud Run Service.  It can also be run locally.  On GCP, The frontend deployment is meant to be run after the backend server code is deployed as it needs to refer to the backend service locations.

# Structure

The frontend code is built in Angular.  Outside of the configuration and supporting utility files, the source code folder structure in src/app is separated into the following:
- components: Contains the various UI components on the DreamBoard app.
- models: Contains files representing image, video, scene, and other objects used in the UI or for requesting from the backend API.
- services: Contains all services used to communicate with the backend API and supporting services.

# Requirements

- A Google Cloud Platform project to host the Cloud Run Service.
- Backend API code deployed before the frontend.  See requirements of the backend server from the backend README for details.
- A service account to invoke Cloud Run Service, start AI generation, and other associated compute access.  Please see the deploy_backend.sh script for specific service account permissions
- Deployment individual to have permission to the following:
  - Build Cloud Run Service
  - Create Cloud Storage Buckets
  - Enable APIs
  - Create service account and apply IAM permissions (if creating at deployment time)

# Installation

The DreamBoard frontend can be installed locally or on GCP.

## Installing on GCP
To install it on GCP:

1. Deploy the backend code and make note of the following when creating :
    - GCP Project Id
    - Cloud Storage Bucket Name
    - Location the service is deployed
    - Cloud Run Service Name
2. Navigate to the frontend folder and run deploy_frontend.sh with the following arguments noted from the previous step in the following order:
    a. **GCP Project ID**
    b. **Cloud Storage Bucket Name**
    c. **Location to deploy**
    d. **Cloud Run Service Name**

## Installing Locally

To install locally on a Linux-based computer, run the following commands in the command line:
1. npm install
2. ng build
3. ng serve

The application will be available on `http://localhost:4200/`.
