# Emboldened Birth — website

> **Taking over?** Start with [TESSA-START-HERE.md](TESSA-START-HERE.md).
>
> **Live site:** <https://emboldenedbirth.com/>

A small, plain static website for **Emboldened Birth by Tessa Millerick**, a birth doula practice in Hidden Valley Lake, serving Lake, Sonoma, and Napa Counties, California.

The site is intentionally simple:

- Plain HTML, CSS, and SVG. No framework, no build step, no JavaScript.
- Self-hosted fonts (Cormorant Garamond and Source Sans 3, both SIL Open Font License).
- Four main pages: Home, About, Services, Contact. Plus a privacy page and a 404 page.
- No cookies, analytics, or third-party scripts. Contact is by a contact form (posted to FormSubmit, formsubmit.co, which emails hello@emboldenedbirth.com; no JavaScript) or email. No phone number on the site.

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
| `contact.html` | Contact form (name, phone, email, optional due date and message), email, next steps |
| `thanks.html` | Shown after the contact form is sent (not indexed) |
| `privacy.html` | Plain-language privacy note |
| `404.html` | GitHub Pages not-found page |
| `TESSA-START-HERE.md` | Plain-language takeover and publishing guide |
| `assets/css/styles.css` | All styling |
| `assets/fonts/` | Self-hosted WOFF2 fonts + OFL licenses |
| `assets/img/` | Original watercolor botanicals (`botanical-*.webp`, plus larger `botanical-corner-tr-lg.webp` and `botanical-corner-bl-lg.webp` for wide screens), the logo's mark (`logo-mark.svg`, and `logo-mark-on-green.svg` for the footer), browser-tab icons (`favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`), social preview image (`og-image.jpg`) |
| `tools/generate-botanicals.py` | Paints the botanical artwork (see Design notes) |
| `tools/make-og-image.py` | Rebuilds the social preview image, `og-image.jpg` (see Design notes) |
| `tools/stamp-css-version.py` | Updates the `?v=` version tag on every page's stylesheet link (run after changing `styles.css`) |
| `robots.txt` | Allows search engines and points to the sitemap |
| `sitemap.xml` | The five public pages, for search engines |
| `CNAME` | The custom domain, `emboldenedbirth.com` (GitHub writes this file; leave it alone) |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is |

## Published site

- **Live:** <https://emboldenedbirth.com/>
- **Repository:** <https://github.com/tessamillerick/emboldened-birth-site>
- **Pages:** deploys from `main`, folder `/ (root)`.

**Public since 2026-11-23 at <https://emboldenedbirth.com/>.** The `CNAME` file holds the domain; DNS is at Porkbun (four GitHub Pages A records for the domain, `www` CNAME to `tessamillerick.github.io`; Proton's mail records unchanged). The github.io address and `www` redirect to the domain. HTTPS is enforced; GitHub's Let's Encrypt certificate covers the domain and `www` and renews itself. If it ever stops renewing, clear and re-save the custom domain in the repository's Pages settings (that is what got the first certificate issued). Search engines are allowed (`robots.txt`, `sitemap.xml`); only `404.html` keeps a `noindex` tag. Each page has a canonical link.

To update it, commit and push:

```sh
git add -A
git commit -m "Describe the change"
git push
```

GitHub Pages rebuilds automatically. The site uses relative links, so it works both at the `github.io/...` subpath and at the root of a custom domain.

If the change touches `assets/css/styles.css`, run `python3 tools/stamp-css-version.py` before committing. It updates the `?v=` tag on the stylesheet link in every page, so browsers and phones load the new design straight away. Otherwise they can keep showing a saved copy of the old stylesheet.

## Launch checklist

- [x] Public wording for the **$750 introductory rate** confirmed by Tessa 2026-11-23: $250 retainer, and the $500 balance due 4 weeks before the due date.
- [x] Free consultation decided (2026-11-10): the site advertises a free, no-obligation first consultation.
- [x] Service area confirmed: **Lake, Sonoma, and Napa Counties** (Napa added 2026-11-23). The site lists the Lake County cities by name. Confirm whether travel beyond those counties is offered.
- [x] Training sentence confirmed by Tessa 2026-11-23: DONA-approved Birth Doula Workshop with Birthing Gently (Tara Campbell), working toward CD(DONA). Do not call Tessa a certified doula until CD(DONA) is complete.
- [x] CPR added to the About page (2026-11-17): American Red Cross Adult and Pediatric First Aid/CPR/AED, **valid until 2028-11-17**. Before then, renew it or remove the CPR sentence and the CPR line in the facts list.
- [x] Backup doula: **every mention removed 2026-11-23 at Tessa's request** (Home package list, Services list and descriptions, About), until she has a backup she knows is reliable. Put it back then.
- [ ] Add Tessa's portrait (launched without it, 2026-11-23). The home page and About page each have a framed spot that currently holds a botanical print; see “Add your portrait” in `TESSA-START-HERE.md`. No stock photos or client images.
- [x] `noindex` removed from every page except `404.html` (2026-11-23).
- [x] `robots.txt` allows search engines and names the sitemap (2026-11-23).
- [x] `CNAME` file and DNS records (2026-11-23). **Never change or remove Proton mail records**: MX, SPF, DKIM CNAMEs, DMARC, and the Proton verification TXT.
- [x] `og:url` and `og:image` already use `https://emboldenedbirth.com/`.
- [x] `sitemap.xml` and canonical links added (2026-11-23). Add a page to the sitemap when one is added to the site.

## Privacy and content rules

- Do not put client names, birth stories, health details, or private contact information in this repository.
- Do not publish invented testimonials or stock photos of people as if they were clients.
- The site currently has no form and no analytics. If either is added, update `privacy.html` and review where the data goes before publishing.

## Design notes

The design follows the business card and the visual-direction notes in the private research repository: warm ivory paper, a copper wordmark and accents, deep eucalyptus labels, and thin brass rules. Headings use Cormorant Garamond at regular weight; body text, labels, and buttons use Source Sans 3. Text columns are held to about 70 characters (`--measure`).

- **One deep green** (`--evergreen`, `#2e3b2e`) anchors the pale pages. It is used in four places only: the top bar, the buttons, the phone contact bar, and the footer. Nothing else is dark.
- **Top bar.** A thin deep green strip on every page: "Free first consultation" (a link to Contact) and the service area, which is hidden on narrow phones.
- **Header.** Stays at the top of the screen from 1080 px wide, with a "Book a free consultation" button (not on the Contact page). Below that it scrolls away.
- **Contact bar.** On phones and tablets (below 1080 px), Home, About and Services have a bar at the bottom of the screen with Email and Free consult (links to the contact form). It slides in once the visitor starts scrolling; where a browser cannot do that, or the visitor prefers reduced motion, it is simply always there. Pages that use it have `<body class="has-contact-bar">`.
- **One framed moment per page.** The closing card near the foot of Home, About and Services (`.cta__card`) carries the business card's open frame: two brass corners where the eucalyptus leaves room (top left and bottom right), with no full border. On wide screens they keep the card's proportions; on narrow screens, where the text runs nearly edge to edge, they stay in the space above and below it. Everything else is open, with single rules at most.
- **The arch.** The portrait frame on Home and About is an arch (4:5, rounded top). A photo fills it edge to edge.
- **The logo.** The logo's mark, a eucalyptus stem growing up inside an open arch, sits beside the wordmark in the header, so the two read as the horizontal logo while the name stays real text. In its deep green colours it sits above the wordmark in the footer, and a heavier version drawn for small sizes is the browser-tab icon. The icon links end in `?v=arch` so browsers drop the old icon; change that tag if the icons change again.
- **Motion is CSS only:** a gentle rise as blocks scroll into view (`reveal`), page cross-fades, and sliding FAQ answers. All of it is switched off for visitors who ask for reduced motion.

Every text color meets WCAG AA contrast on its background. On the pale papers, sage and brass are used only for decoration; on the deep green, a lighter brass (`--brass-on-dark`) is used for small text.

The botanical artwork is original. `tools/generate-botanicals.py` paints watercolor eucalyptus with a small pigment model (layered washes, pooled edges, paper grain) and writes the `assets/img/botanical-*.webp` files. It uses no template, stock, or clip-art source, so there is no license to track. Each piece has a fixed seed, so running the script again paints the same pictures:

```sh
python3 tools/generate-botanicals.py                        # repaint assets/img/botanical-*.webp
python3 tools/generate-botanicals.py --preview              # also save previews on ivory
python3 tools/generate-botanicals.py --scale 3 --out print-art   # larger masters, e.g. for print
python3 tools/generate-botanicals.py --scale 1.8 --suffix=-lg --only botanical-corner-tr botanical-corner-bl
                                                            # the larger corners used on wide screens
```

Write `--suffix=-lg` with the equals sign; with a space, the leading hyphen is read as another option. Phones still load the smaller corners through `srcset`.

It needs Python 3 with numpy, Pillow (with WebP), and pycairo. Change a seed or a composition in the script to paint new variations.

The social preview image, `assets/img/og-image.jpg` (1200 × 630), shows the business card's front, open frame included, on the closing card's oat ground. `python3 tools/make-og-image.py` rebuilds it with headless Chrome (`google-chrome-stable`) and Pillow. Run it again after changing the wordmark, the colors or the corner paintings.

The voice stays editorial and understated: generous white space and no exclamation points. It borrows the *feel* of a magazine like Garden & Gun without copying any logo, type lockup, or trade dress.
