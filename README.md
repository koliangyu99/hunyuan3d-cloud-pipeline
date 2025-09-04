Hunyuan3D Cloud-Ready Generation Pipeline
This project provides a Python Flask application that demonstrates a robust, cloud-native architecture for running the Hunyuan3D model. The entire application is containerized with Docker, allowing for easy local testing and deployment to cloud services like Google Cloud Run.

The application exposes an asynchronous API for generating 3D models from text prompts and input images.

Core Architecture
This application simulates a scalable cloud architecture locally, separating the one-time model setup from the recurring inference tasks.

Build-Time (Initialization in Dockerfile):

The Docker image build process downloads the large, pre-trained Hunyuan3D model weights from Hugging Face. This is done only once when the image is created.

Run-Time (Live Application):

API Service: A Flask/Gunicorn server accepts job requests at /generate and provides status updates at /status/<job_id>. This is designed to be a lightweight and fast entry point.

Task Queue: An in-memory queue decouples the API from the heavy processing, allowing the API to respond instantly. In a real cloud environment, this would be replaced by a service like Google Cloud Tasks.

Background Worker: A background thread pulls jobs from the queue and uses the globally loaded Hunyuan3D model to perform inference. This simulates a separate, long-running worker service.

Object Storage: Local folders (/gcs_buckets) are used to simulate cloud storage buckets for inputs and outputs.

Setup and Usage
Prerequisites
Git

Docker

1. Clone the Repository
First, clone this repository to your local machine.

git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME

2. Initialize the Hunyuan3D Submodule
This project includes the official Hunyuan3D repository as a Git submodule. To download it, run:

git submodule update --init --recursive

This will pull the Hunyuan3D repository into the correct directory.

3. Build the Docker Image
This command executes the steps in the Dockerfile, including the multi-gigabyte model download. This will take a long time.

docker build -t hunyuan3d-app .

4. Run the Docker Container
This command starts the application and maps the local gcs_buckets folders to the container, so you can easily add inputs and see the outputs.

# Create local directories first
mkdir -p gcs_buckets/inputs gcs_buckets/outputs

# Run the container
docker run -p 5001:5001 \
  -v $(pwd)/gcs_buckets/inputs:/app/gcs_buckets/inputs \
  -v $(pwd)/gcs_buckets/outputs:/app/gcs_buckets/outputs \
  hunyuan3d-app

Your server is now running and accessible at http://localhost:5001.

5. Use the API
Place your input image (e.g., car.png) in the gcs_buckets/inputs folder.

a. Submit a Generation Job
Use curl or any API client to send a request.

curl -X POST [http://127.0.0.1:5001/generate](http://127.0.0.1:5001/generate) \
-H "Content-Type: application/json" \
-d '{
    "prompt": "a photorealistic red sports car",
    "image_filenames": ["car.png"],
    "output_filename": "red_sports_car.glb"
}'

The server will respond with a job_id.

b. Check the Job Status
Use the job_id to poll the status endpoint.

curl [http://127.0.0.1:5001/status/YOUR_JOB_ID_HERE](http://127.0.0.1:5001/status/YOUR_JOB_ID_HERE)

When the status is "completed", your .glb file will be available in the gcs_buckets/outputs folder.
