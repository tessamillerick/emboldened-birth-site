# Emboldened Birth — website

> **Taking over?** Start with [TESSA-START-HERE.md](TESSA-START-HERE.md).
>
> **Live preview:** <https://tessamillerick.github.io/emboldened-birth-site/>

A small, plain static website for **Emboldened Birth by Tessa Millerick**, a birth doula practice in Hidden Valley Lake, serving Lake and Sonoma Counties, California.

The site is intentionally simple:

- Plain HTML, CSS, and SVG. No framework, no build step, no JavaScript.
- Self-hosted fonts (Cormorant Garamond and Source Sans 3, both SIL Open Font License).
- Four main pages: Home, About, Services, Contact. Plus a privacy page and a 404 page.
- No contact form, cookies, analytics, or third-party scripts. Contact is by email, phone, or text.

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
| `assets/img/` | Original watercolor botanicals (`botanical-*.webp`), favicon, social preview image (`og-image.jpg`) |
| `tools/generate-botanicals.py` | Paints the botanical artwork (see Design notes) |
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
- [x] Free consultation decided (2026-11-10): the site advertises a free, no-obligation first consultation.
- [x] Service area confirmed: **Lake and Sonoma Counties**. The site lists the Lake County cities and Sonoma County by arrangement. Confirm whether travel beyond those counties is offered.
- [ ] Confirm the training sentence: DONA-approved Birth Doula Workshop with Birthing Gently (Tara Campbell), working toward CD(DONA). Do not add “certified” until certification is complete.
- [ ] Confirm the backup-doula sentence (“Before services begin, I’ll name a backup doula…”).
- [ ] Add Tessa's portrait. The home page and About page each have a framed spot that currently holds a botanical print; see “Add your portrait” in `TESSA-START-HERE.md`. No stock photos or client images.
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

The design follows the business card and the visual-direction notes in the private research repository: warm ivory paper, a copper wordmark and accents, deep eucalyptus labels, thin brass rules, and framed panels like the card front. Headings use Cormorant Garamond; body text, labels, and buttons use Source Sans 3. Every text color meets WCAG AA contrast on every background; sage and brass are used only for decoration.

The botanical artwork is original. `tools/generate-botanicals.py` paints watercolor eucalyptus with a small pigment model (layered washes, pooled edges, paper grain) and writes the `assets/img/botanical-*.webp` files. It uses no template, stock, or clip-art source, so there is no license to track. Each piece has a fixed seed, so running the script again paints the same pictures:

```sh
python3 tools/generate-botanicals.py                        # repaint assets/img/botanical-*.webp
python3 tools/generate-botanicals.py --preview              # also save previews on ivory
python3 tools/generate-botanicals.py --scale 3 --out print-art   # larger masters, e.g. for print
```

It needs Python 3 with numpy, Pillow (with WebP), and pycairo. Change a seed or a composition in the script to paint new variations.

The voice stays editorial and understated: generous white space and no exclamation points. It borrows the *feel* of a magazine like Garden & Gun without copying any logo, type lockup, or trade dress.
