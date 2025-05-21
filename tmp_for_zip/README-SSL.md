# SSL Configuration for Production Deployment

This document explains how to set up SSL certificates for secure HTTPS connections to your SceneIQ dashboard in production.

## Self-Signed Certificates (For Testing Only)

For testing purposes, you can generate self-signed certificates using the following commands:

```bash
# Create directory for SSL certificates if it doesn't exist
mkdir -p docker/nginx/ssl

# Generate a self-signed certificate (valid for 365 days)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout docker/nginx/ssl/sceneiq.key \
  -out docker/nginx/ssl/sceneiq.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=sceneiq.example.com"
```

**Note:** Self-signed certificates will cause browser warnings. They should only be used for testing, never in production.

## Production Certificates

For production use, you should obtain certificates from a trusted certificate authority like Let's Encrypt. Here's how to set up Let's Encrypt certificates:

### Using Certbot

1. Install Certbot on your host machine:
   ```bash
   # For Ubuntu/Debian
   apt-get update
   apt-get install certbot
   ```

2. Generate certificates:
   ```bash
   certbot certonly --standalone -d sceneiq.yourdomain.com
   ```

3. Copy the certificates to your NGINX configuration directory:
   ```bash
   cp /etc/letsencrypt/live/sceneiq.yourdomain.com/fullchain.pem docker/nginx/ssl/sceneiq.crt
   cp /etc/letsencrypt/live/sceneiq.yourdomain.com/privkey.pem docker/nginx/ssl/sceneiq.key
   ```

4. Set up auto-renewal:
   ```bash
   # Add a cron job to automatically renew certificates
   echo "0 3 * * * certbot renew --quiet && cp /etc/letsencrypt/live/sceneiq.yourdomain.com/fullchain.pem /path/to/docker/nginx/ssl/sceneiq.crt && cp /etc/letsencrypt/live/sceneiq.yourdomain.com/privkey.pem /path/to/docker/nginx/ssl/sceneiq.key && docker-compose restart nginx" | crontab -
   ```

## Custom Domain Configuration

Remember to update the `server_name` directive in the NGINX configuration file (`docker/nginx/conf/sceneiq.conf`) to match your actual domain name.