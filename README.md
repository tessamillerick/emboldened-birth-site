# Emboldened Birth — website

> **Taking over?** Start with [TESSA-START-HERE.md](TESSA-START-HERE.md).
>
> **Live preview:** <https://tessamillerick.github.io/emboldened-birth-site/>

A small, plain static website for **Emboldened Birth by Tessa Millerick**, a birth doula practice in Hidden Valley Lake, Lake County, California.

The site is intentionally simple:

- Plain HTML, CSS, and SVG. No framework, no build step, no JavaScript.
- Self-hosted fonts (Playfair Display and Inter, both SIL Open Font License).
- Four main pages: Home, About, Services, Contact. Plus a privacy page and a 404 page.
- No contact form, cookies, analytics, or third-party scripts. Contact is by email and phone.

## Preview locally

From this folder:

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>. Stop the server with `Ctrl+C`.

## Files

| Path | Purpose |
| --- | --- |
| `index.html` | Home page |
| `about.html` | Tessa's story, approach, training |
| `services.html` | Birth package, investment, FAQ, service area |
| `contact.html` | Email, phone, what to include, next steps |
| `privacy.html` | Plain-language privacy note |
| `404.html` | GitHub Pages not-found page |
| `TESSA-START-HERE.md` | Plain-language takeover and publishing guide |
| `assets/css/styles.css` | All styling |
| `assets/fonts/` | Self-hosted WOFF2 fonts + OFL licenses |
| `assets/img/` | Floral bands, sprig, favicon, social preview image |
| `robots.txt` | Preview-only block on search engines |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is |

## Published preview

- **Live:** <https://tessamillerick.github.io/emboldened-birth-site/>
- **Repository:** <https://github.com/tessamillerick/emboldened-birth-site>
- **Pages:** deploys from `main`, folder `/ (root)`.

The site is currently a **noindex preview**: every page has a `noindex` tag and `robots.txt` blocks search engines.

To update it, commit and push:

```sh
git add -A
git commit -m "Describe the change"
git push
```

GitHub Pages rebuilds automatically. The site uses relative links, so it works both at the `github.io/...` subpath and at the root of a custom domain.

## Before the site goes public

- [ ] Confirm the public wording for services and the **$750 introductory rate**, including the $250 deposit / $500 balance. Confirm these before launch.
- [ ] Decide whether to advertise a **free** initial consultation. The draft calls it an initial consultation, not free.
- [ ] Confirm the service-area list (Hidden Valley Lake, Lakeport, Clearlake, Middletown, Kelseyville, Lower Lake) and whether travel outside Lake County is offered.
- [ ] Confirm the training sentence: DONA-approved Birth Doula Workshop with Birthing Gently (Tara Campbell), working toward CD(DONA). Do not add “certified” until certification is complete.
- [ ] Confirm the backup-doula sentence (“Before services begin, I’ll name a backup doula…”).
- [ ] Add real photographs if desired. The current design uses only the business-card floral artwork; no stock photos or client images are used.
- [ ] Remove the `noindex` meta tag from every page. It is marked with `PREVIEW ONLY`.
- [ ] Replace `robots.txt` with an allow rule.
- [ ] Add a `CNAME` file and DNS records only after a separate domain/DNS review. **Do not change or remove Proton mail records**: MX, SPF, DKIM CNAMEs, DMARC, and the Proton verification TXT.
- [ ] Update `og:url` and `og:image` if the final address differs from `https://emboldenedbirth.com/`.
- [ ] Add a sitemap and canonical links if desired after the domain is live.

## Privacy and content rules

- Do not put client names, birth stories, health details, or private contact information in this repository.
- Do not publish invented testimonials or stock photos of people as if they were clients.
- The site currently has no form and no analytics. If either is added, update `privacy.html` and review where the data goes before publishing.

## Design notes

The palette, serif wordmark, and floral bands come from the existing Emboldened Birth business card. The floral bands are extracted from that card as standalone SVG files. The type pairing is Playfair Display for headings and Inter for labels and body copy.

The brand direction is editorial and understated: cream paper, sage and blush botanicals, generous white space, and no exclamation points. It borrows the *feel* of a magazine like Garden & Gun without copying any logo, type lockup, or trade dress.
