# Stage 1: Base image
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_NO_INTERACTION 1

# Set working directory
WORKDIR /app

# Stage 2: Install dependencies
FROM base AS dependencies

# Install Poetry
RUN pip install --upgrade pip && pip install poetry

# Copy only the dependency files
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies
RUN poetry config virtualenvs.create false && poetry install --only main

# Stage 3: Final build
FROM dependencies AS final

# Copy the rest of the application code
COPY . /app

# Expose both FastAPI and Streamlit ports
EXPOSE 8000 8501

# Run FastAPI and Streamlit in parallel
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_UI.py --server.port=8501 --server.address=0.0.0.0"]
