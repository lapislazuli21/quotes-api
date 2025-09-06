# Use an official Python base image
FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app/src

# Install uv, the fast Python package installer
RUN pip install --no-cache-dir uv

# Copy the dependency files
COPY pyproject.toml uv.lock ./

# Install project dependencies using uv
RUN uv pip sync --system --no-cache uv.lock

# Copy the application source code into the container
COPY ./src /app/src

# Expose the port the app will run on
EXPOSE 8000

CMD ["uvicorn", "quotes_api.main:app", "--host", "0.0.0.0", "--port", "8000"]