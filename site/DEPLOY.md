# Deploying themessmate.com

The landing site is fully static — 5 files, no build step:

```
messmate-landing/
├── index.html      # the page
├── styles.css      # design system
├── app.js          # interactions
├── CNAME           # custom domain for GitHub Pages
├── robots.txt
└── sitemap.xml
```

> **DNS note first:** Cloudflare Email Routing only works when the domain's
> nameservers point to Cloudflare. So your DNS is almost certainly managed in
> the **Cloudflare dashboard**, not BigRock. BigRock only "holds" the
> registration. Add all records below wherever your nameservers point
> (check with `nslookup -type=NS themessmate.com`).

---

## Option A — Vercel (recommended, fastest)

1. Push `messmate-landing/` to a Git repo, or deploy the folder directly:
   ```
   npm i -g vercel
   cd messmate-landing
   vercel --prod
   ```
2. In the Vercel dashboard → your project → **Settings → Domains** → add `themessmate.com` and `www.themessmate.com`.
3. Add these DNS records (Cloudflare DNS panel → Records):

   | Type  | Name | Value                | Proxy        |
   |-------|------|----------------------|--------------|
   | A     | @    | 76.76.21.61          | DNS only*    |
   | CNAME | www  | cname.vercel-dns.com | DNS only*    |

   \* Start with "DNS only" (grey cloud) until the SSL certificate is issued,
   then you may enable proxying. Also set `www` to redirect to the apex in
   Vercel's domain settings.

4. Wait for the cert (usually < 5 min). Site is live at https://themessmate.com.

## Option B — GitHub Pages (free forever, zero platform risk)

1. Push `messmate-landing/` to a repo (the included `CNAME` file makes the
   custom domain stick).
2. Repo → **Settings → Pages** → deploy from branch → select the folder.
3. Under **Custom domain** enter `themessmate.com`, then enable **Enforce HTTPS**
   once the certificate is issued.
4. DNS records (Cloudflare):

   | Type  | Name | Value                                      |
   |-------|------|--------------------------------------------|
   | A     | @    | 185.199.108.153                            |
   | A     | @    | 185.199.109.153                            |
   | A     | @    | 185.199.110.153                            |
   | A     | @    | 185.199.111.153                            |
   | CNAME | www  | abu-devel0per.github.io                    |

## Option C — Netlify

1. Drag-and-drop the `messmate-landing` folder at app.netlify.com/drop.
2. Site settings → **Domain management** → add `themessmate.com`.
3. DNS records:

   | Type  | Name | Value          |
   |-------|------|----------------|
   | A     | @    | 75.2.60.5      |
   | CNAME | www  | your-site.netlify.app |

---

## After deploying — checklist

- [ ] `https://themessmate.com` loads with a valid padlock (check at
      `https://developer.mozilla.org/en-US/observatory` or SSLShopper).
- [ ] `www.themessmate.com` redirects to the apex.
- [ ] **Email still works** — MX records and Cloudflare Email Routing rules are
      untouched by the records above. Send a test mail to your routed address
      and confirm delivery.
- [ ] Create the `beta@themessmate.com` alias in Cloudflare Email Routing →
      Routing rules (the page's waitlist CTAs mail to it). Point it at the
      inbox you actually read.
- [ ] Run a Lighthouse pass (Chrome DevTools → Lighthouse) — should score 95+
      on Performance/Accessibility/SEO out of the box.
- [ ] Submit `https://themessmate.com/sitemap.xml` to Google Search Console
      (optional, helps indexing).
- [ ] DNS propagation check: `nslookup themessmate.com` from a terminal.

## If the domain was bought on BigRock but DNS lives on Cloudflare

Nothing to do on BigRock. Only if `nslookup -type=NS themessmate.com` shows
BigRock nameservers instead of Cloudflare's should you add the records above in
BigRock's DNS management page instead — and in that case, re-check that MX
records for your email routing exist on BigRock's side too.
