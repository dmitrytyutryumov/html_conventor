FROM python:3.8-alpine

ENV PYTHONPATH="/usr/src/app"
WORKDIR $PYTHONPATH

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY site_parser .
COPY .env .

EXPOSE 8000
CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=2", "--threads=2", "--log-level=critical", "--capture-output",  "site_parser.wsgi"]