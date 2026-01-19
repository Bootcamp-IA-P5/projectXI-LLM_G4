# Multi-stage build for smaller image size
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt .

# Install dependencies in a virtual environment
RUN pip install --user --no-cache-dir -r requirements.txt


# Final stage - much smaller
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Create non-root user first
RUN useradd -m -u 1000 appuser

# Copy only the installed packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY app.py content_generator.py ./

# Fix permissions for appuser
RUN chown -R appuser:appuser /app /home/appuser/.local

# Switch to non-root user
USER appuser

# Make sure scripts in .local are usable
ENV PATH=/home/appuser/.local/bin:$PATH

# Environment variables for Streamlit and UTF-8
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    PYTHONIOENCODING=utf-8 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Expose port
EXPOSE 8501

# Command to run
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
