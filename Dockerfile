# syntax=docker/dockerfile:1

# Specify Python version as a build argument
ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim as base

# Optimize Python behavior in Docker
# Avoid writing .pyc files
# Ensure stdout and stderr are flushed
ENV PYTHONDONTWRITEBYTECODE=1  
ENV PYTHONUNBUFFERED=1         

# Set the working directory at the root
WORKDIR /

# Create a non-privileged user to run the application
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Create home directory and give ownership to appuser
RUN mkdir -p /home/appuser && chown appuser:appuser /home/appuser
# Assuming you're creating appuser as non-root user
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# Install dependencies with cache optimizations
# The --mount flag is used to cache pip packages during the build
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=./requirements.txt,target=requirements.txt \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory into the container
COPY ./app/ /app/
COPY ./scripts/ /scripts/

# Expose FastAPI port
EXPOSE 8000

# Switch to non-privileged user
USER appuser

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
