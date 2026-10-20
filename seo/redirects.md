# Old → new URL map (301 redirects) for the ubm.co.in migration

Brand folders (`/epson/`, `/bose/`, `/aten/`, `/liberty-av-solutions/`, `/viewsonic/`, `/benq/`) keep **the same URL** on the new site, so they need no redirect.

| Old URL | New URL |
|---|---|
| /index.php | / |
| /about-us.php | /about-us/ |
| /vertical.php | /industries/ |
| /brand.php | /brands/ |
| /solution.php | /solutions/ |
| /career.php | /careers/ |
| /contact.php, /contact-us.php, /*/contact-us.php | /contact/ |
| /whatsapp.php | /contact/ |
| /epson/corporate-education/, /epson/high-brightness-projectors/, /epson/interactive-projector/, /epson/lighting-signage-laser-projectors/ | /epson/ |
| /bose/loudspeakers/, /bose/amplifiers/, /bose/portable-pa/, /bose/conferencing/ | /bose/ |
| /aten/kvm/, /aten/professional-audio-video/, /aten/usb/, /aten/cables/ | /aten/ |
| /liberty-av-solutions/* (sub-pages) | /liberty-av-solutions/ |
| /benq/projector.php, /benq/digital-display.php, /benq/wireless-presentation.php | /benq/ |
| /viewsonic/* (sub-pages) | /viewsonic/ |

## nginx (the current server runs nginx)

```nginx
# inside the server { } block for www.ubm.co.in
rewrite ^/index\.php$            /                 permanent;
rewrite ^/about-us\.php$         /about-us/        permanent;
rewrite ^/vertical\.php$         /industries/      permanent;
rewrite ^/brand\.php$            /brands/          permanent;
rewrite ^/solution\.php$         /solutions/       permanent;
rewrite ^/career\.php$           /careers/         permanent;
rewrite ^/(.*/)?contact(-us)?\.php$ /contact/      permanent;
rewrite ^/whatsapp\.php$         /contact/         permanent;
rewrite ^/(epson|bose|aten|liberty-av-solutions|viewsonic|benq)/.+$ /$1/ permanent;

# also: force https + www, and return a REAL 404 for unknown URLs
# (today every unknown URL returns the homepage with status 200 — a "soft 404")
error_page 404 /404.html;
location / { try_files $uri $uri/ =404; }
```
