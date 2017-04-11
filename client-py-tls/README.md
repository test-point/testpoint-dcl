# TLS auth example

How to create valid local untusted nginx installation and TLS auth.

1. Start django app
2. install nginx
3. Run `generate_server_keys.sh` and `generate_client_cert.sh` or use existing demo keys from demo_keys directory
4. copy nginx config to nginx folder, copy keys to /etc/nginx/tls-ssl/ folder
5. start nginx
6. ensure script `pythonic_certificate.py` has access to client keys (put them in same directory or update pathes inside the script)
7. run `pythonic_certificate.py` script.

Leave any password empty when you create the certificates.

After the script has been started it will return you demo_auth result, where you expect some user returned. When you go http://127.0.0.1:5200/admin/auth/user/ here you can see this user. If you have already created some demo accredited party in django admin then you can add relationship between this user and this party http://127.0.0.1:5200/admin/accreditations/userpartyaccess/ here, and from now on `pythonic_certificate.py` script would return this party ID in `accredited_parties` list.

You may not worry about keys generation and just use keys from demo_keys folder here, I've generated it for you.