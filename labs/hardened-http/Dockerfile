FROM python:3.12-alpine

# Minimal learning container: no pip packages, no application root privileges.
RUN addgroup -S -g 10001 lab && adduser -S -D -H -u 10001 -G lab lab
WORKDIR /app
COPY --chown=10001:10001 server.py /app/server.py
USER 10001:10001
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 LAB_PORT=8080
EXPOSE 8080
CMD ["python", "-I", "/app/server.py"]
