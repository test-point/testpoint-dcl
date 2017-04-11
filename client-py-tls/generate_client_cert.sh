#!/bin/bash
echo "you are about to create client certificate. Empty all passphrases empty"
echo "Please fill 'Email Address' equal to new django user email address (unique)"
echo "Please fill 'Common Name' equal to new django user username (unique, only letters, digits and -_ characters)"

openssl genrsa -out client.key 1024
openssl req -new -key client.key -out client.csr

# Sign the client certificate with our CA cert.  Unlike signing our own server cert, this is what we want to do.
openssl x509 -req -days 365 -in client.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out client.crt