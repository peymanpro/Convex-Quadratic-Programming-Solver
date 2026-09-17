FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY solver ./solver
COPY validation ./validation
COPY api ./api

RUN pip install --no-cache-dir "numpy>=1.26,<3" "scipy>=1.11" \
    "django>=5.0" "djangorestframework>=3.15" "drf-spectacular" \
    && pip install --no-cache-dir -e .

EXPOSE 8000

WORKDIR /app/api

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

