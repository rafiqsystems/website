# rafiqsystems.com

Public website for Rafiq. Static HTML and CSS in `public/`, no JavaScript, no third-party
requests, no cookies, no analytics. Served by Cloudflare as static Worker assets; the Worker
runs no code.

## Deploy

Every push to `main` runs `.github/workflows/deploy.yml`, which calls `wrangler deploy` using the
repository secrets `CLOUDFLARE_API_TOKEN` (Workers Scripts: Edit, Workers Routes: Edit, Zone DNS:
Edit for the rafiqsystems.com zone) and `CLOUDFLARE_ACCOUNT_ID`.

Manual deploy from a machine with wrangler logged in:

```bash
npx wrangler deploy
```

## Headers and redirects

`public/_headers` sets a strict Content-Security-Policy, no-referrer, HSTS and a one-week
immutable cache for `/assets/`. `public/_redirects` sends `www` to the apex.

In the Cloudflare dashboard keep these **off** for the zone, since each injects JavaScript or
contradicts the privacy statement in the footer: Rocket Loader, Email Address Obfuscation,
Web Analytics (RUM), Bot Fight Mode's JavaScript detections. Keep Always Use HTTPS on.

## Local preview

```bash
python3 -m http.server 8080 --directory public
```

Content is CC BY-SA 4.0. The Rafiq name and logo are covered by the trademark policy at
`/trademark/`.
