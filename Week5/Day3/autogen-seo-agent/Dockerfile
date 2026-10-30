
# Python runtime
FROM python:3.12-slim

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show Python logs immediately
ENV PYTHONUNBUFFERED=1

# Set application directory
WORKDIR /app

# Copy dependency definitions first
COPY requirements.txt .

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install \
    --index-url https://pypi.org/simple \
    --timeout 120 \
    --retries 5 \
    -r requirements.txt

# Copy application source
COPY . .

# Streamlit configuration
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true

# Expose Streamlit port
EXPOSE 8501

# Start SEO AI Studio
CMD ["python", "-m", "streamlit", "run", "app.py"]
