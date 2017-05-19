#!/bin/bash
echo "you are about to create server certificate, to configure Nginx"
echo "Please create it directly in your nginx /etc/nginx/tls-ssl/ folder (client cert as well)"
echo "Don't forget to restart nginx after that"
echo "Only 'Common Name' field is important and shall be equal to domain name of your installation"
echo "(You'll have to add certificate exception in your browser anyway because it's self-signed)"

openssl genrsa -out ca.key 4096
openssl req -new -x509 -days 365 -key ca.key -out ca.crt

# Create the Server Key, CSR, and Certificate
openssl genrsa -out server.key 1024
openssl req -new -key server.key -out server.csr

# We're self signing our own server cert here.  This is a no-no in production.
openssl x509 -req -days 365 -in server.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out server.crt
