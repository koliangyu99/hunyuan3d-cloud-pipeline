# Hunyuan3D Generation Pipeline

This project provides an easy way to run the Hunyuan3D model using Docker. It starts a simple web server (API) that you can use to create 3D models from text and images.

Because it's a Docker application, it's simple to run on your own machine or deploy to the cloud.

---

## How It Works

This setup is designed to be efficient. It separates the slow, one-time model download from the actual 3D generation.

* **One-Time Setup:** When you build the Docker image, it downloads the large Hunyuan3D model. This only happens once.
* **Running the App:**
    * A **fast API** instantly accepts your request to create a 3D model.
    * A **background worker** takes the request and does the heavy lifting of generating the 3D model. This keeps the API responsive.
    * It uses local folders (`gcs_buckets`) to simulate cloud storage, making it easy to provide input images and get your finished 3D models.

---

## Getting Started

### Prerequisites
* [Git](https://git-scm.com/)
* [Docker](https://docs.docker.com/get-docker/)

### Step-by-Step Instructions

1.  **Clone the Project**

    Download the code and the necessary model files.
    ```bash
    git clone https://github.com/koliangyu99/hunyuan3d-cloud-pipeline.git
    cd hunyuan3d-cloud-pipeline
    
    ```

2.  **Build the Docker Image**

    This command packages the app and downloads the large 3D model.
    **Warning:** This will take a long time and download several gigabytes.
    ```bash
    docker build -t hunyuan3d-local .
    ```

3.  **Run the Application**

    Start the server. This also connects the `gcs_buckets` folders on your computer to the folders inside the container, so you can easily access your files.
    ```bash
      # Run the container with port mapping
      docker run -p 8080:8080 --name hunyuan3d-test hunyuan3d-local

      # Alternative: Run with volume mounting for development
      docker run -p 8080:8080 -v $(pwd):/app --name hunyuan3d-dev hunyuan3d-local

      # Test the health endpoint
      curl http://localhost:8080/health

      # Test with a sample image (you'll need to create test_image.json)
      curl -X POST http://localhost:8080/generate \
        -H "Content-Type: application/json" \
        -d @test_image.json

      # View logs
      docker logs hunyuan3d-test

      # Stop and remove container
      docker stop hunyuan3d-test
      docker rm hunyuan3d-test

      # Remove image if needed
      docker rmi hunyuan3d-local
    ```


