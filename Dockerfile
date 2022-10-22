FROM --platform=linux/amd64 python:slim-bullseye

# Define Git SHA build argument for sentry
ARG git_sha="development"

COPY . .

RUN pip install .

CMD ["python", "-m", "bot"]
