# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (for Manim and fonts)
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        pkg-config \
        ffmpeg \
        sox \
        libcairo2-dev \
        libpango1.0-dev \
        texlive \
        texlive-latex-extra \
        texlive-fonts-recommended \
        dvipng \
        dvisvgm \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Use Gunicorn for production, with 2 worker processes
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "720", "--workers", "1", "server:app"]
