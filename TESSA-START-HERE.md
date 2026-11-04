# Tessa — start here

Your website is live as a **preview**:

- **Live preview:** <https://tessamillerick.github.io/emboldened-birth-site/>
- **GitHub repository:** <https://github.com/tessamillerick/emboldened-birth-site>
- **Local folder:** `/home/sean/emboldened-birth-site`

The site is not searchable yet. Every page has a `noindex` tag, and `robots.txt` blocks search engines. The custom domain `emboldenedbirth.com` is still parked; no DNS changes were made, and Proton mail records were not touched.

## 1. See it

Open the live preview above, or preview locally:

**http://127.0.0.1:8000**

If the local server is not running, start it from this folder:

```sh
cd /home/sean/emboldened-birth-site
python3 -m http.server 8000
```

Stop it with `Ctrl+C`.

## 2. What is here

- Home, About, Services, Contact, Privacy, and a custom 404 page.
- Plain HTML and CSS. No build step and no JavaScript.
- No cookies, analytics, advertising trackers, or contact forms. Contact is by email and phone.
- Fonts are self-hosted, so no requests go to Google Fonts.
- The design uses the cream, sage, and blush palette and floral artwork from your business card.
- The site is currently a noindex preview, not a search-indexed public site.

## 3. How to update the site

Edit the files in this folder, preview locally, then save and publish the change:

```sh
cd /home/sean/emboldened-birth-site
git add -A
git commit -m "Describe the change"
git push
```

GitHub Pages rebuilds automatically after a push. It usually takes about a minute. Check the live preview afterward.

Your GitHub account is active on this machine. You can confirm with:

```sh
gh auth status
```

Your local Git identity is already set to `Tessa Millerick <tessamillerick@users.noreply.github.com>`, so future commits use your GitHub noreply address instead of your personal email.

## 4. Before the site goes public and searchable

- Confirm the services and the **$750 introductory rate**, including the $250 deposit and $500 balance.
- Confirm the service area list.
- Confirm the training wording: DONA-approved Birth Doula Workshop with Birthing Gently (Tara Campbell), working toward CD(DONA). Do not claim certification until it is complete.
- Confirm the backup-doula sentence.
- Decide whether to advertise a **free** initial consultation. The draft calls it an initial consultation, not free.
- Add real photographs if you want them; the current design uses only the business-card artwork.
- Remove the `noindex` meta tag from every page.
- Replace `robots.txt` with an allow rule.
- Add the custom domain only after a separate DNS review. Keep Proton's MX, SPF, DKIM, DMARC, and verification records intact.
- Optional: add a sitemap and canonical links once the domain is live.

## 5. If something goes wrong

- The site is static; you can always preview it locally.
- See recent commits with `git log --oneline`.
- Undo an uncommitted edit with `git restore <file>`.
- GitHub Pages build status is in **Settings → Pages** and the **Actions** tab.
- If a push fails, check `gh auth status` and switch to your account with `gh auth switch --user tessamillerick`.
- Do not change DNS as a troubleshooting step.

## 6. Account cleanup

Your GitHub account is active. Sean's accounts are still stored on this machine:

- `SRMillerick`
- `sean-adoraway`

After you are comfortable with the repository and your own login, you can remove them:

```sh
gh auth logout --hostname github.com --user SRMillerick
gh auth logout --hostname github.com --user sean-adoraway
```

Do not remove them until your account and the repository are working. The first setup commits were authored with Sean's email; future commits use your name and GitHub noreply address. Rewriting the old commits is a separate step if you ever want it.

## 7. Where things live

- Website: `/home/sean/emboldened-birth-site`
- Live preview: <https://tessamillerick.github.io/emboldened-birth-site/>
- Planning handoff: `/home/sean/emboldened-birth-handoff-2026-10-27`
- Private research repository: `/home/sean/doula-cert-ca`
