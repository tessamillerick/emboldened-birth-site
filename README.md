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
| `assets/img/` | Original watercolor botanicals (`botanical-*.webp`, plus larger `botanical-corner-tr-lg.webp` and `botanical-corner-bl-lg.webp` for wide screens), favicon, social preview image (`og-image.jpg`) |
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

The design follows the business card and the visual-direction notes in the private research repository: warm ivory paper, a copper wordmark and accents, deep eucalyptus labels, and thin brass rules. Headings use Cormorant Garamond at regular weight; body text, labels, and buttons use Source Sans 3. Text columns are held to about 70 characters (`--measure`).

- **One deep green** (`--evergreen`, `#2e3b2e`) anchors the pale pages. It is used in four places only: the top bar, the buttons, the phone contact bar, and the footer. Nothing else is dark.
- **Top bar.** A thin deep green strip on every page: "Free first consultation" (a link to Contact) and the service area, which is hidden on narrow phones.
- **Header.** Stays at the top of the screen from 1080 px wide, with a "Book a free consultation" button (not on the Contact page). Below that it scrolls away.
- **Contact bar.** On phones and tablets (below 1080 px), Home, About and Services have a bar at the bottom of the screen with Email, Text and Call. It slides in once the visitor starts scrolling; where a browser cannot do that, or the visitor prefers reduced motion, it is simply always there. Pages that use it have `<body class="has-contact-bar">`.
- **One framed moment per page.** The business card's double rule frames only the closing card near the foot of Home, About and Services (`.cta__card`). Everything else is open, with single rules at most.
- **The arch.** The portrait frame on Home and About is an arch (4:5, rounded top). A photo fills it edge to edge.
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

The voice stays editorial and understated: generous white space and no exclamation points. It borrows the *feel* of a magazine like Garden & Gun without copying any logo, type lockup, or trade dress.
