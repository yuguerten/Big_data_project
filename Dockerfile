FROM bitnami/spark:3.5.0

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir \
    torch==2.0.1 \
    transformers \
    numpy==1.24.1 \
    pandas

USER 1001