# Local HTTPS certificates

Generate a local self-signed certificate before running Docker Compose:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/certs/localhost.key \
  -out nginx/certs/localhost.crt \
  -subj "/C=DE/ST=NRW/L=Bielefeld/O=WebTech/OU=Development/CN=localhost"
```

The generated `localhost.key` and `localhost.crt` files are ignored by Git.
