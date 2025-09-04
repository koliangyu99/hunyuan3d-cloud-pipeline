# Use an official Python runtime as a parent image
# For GPU support, use an image like: nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git

COPY Hunyuan3D/requirements.txt /app/Hunyuan3D/requirements.txt
# We will create requirements.txt for the app later
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r Hunyuan3D/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir huggingface_hub

ENV HF_HOME=/app/huggingface_cache

# This command downloads the model files during the build
RUN huggingface-cli download tencent/Hunyuan3D-2 --repo-type model --local-dir /app/hunyuan3d_models --local-dir-use-symlinks False

COPY hunyuan_pipeline_app.py .
COPY Hunyuan3D/ ./Hunyuan3D/

RUN mkdir -p /app/gcs_buckets/inputs && mkdir -p /app/gcs_buckets/outputs

EXPOSE 5001

CMD ["gunicorn", "--workers", "1", "--threads", "8", "--timeout", "300", "-b", "0.0.0.0:5001", "hunyuan_pipeline_app:app"]
