# Tessa — start here

Your website is public at **<https://emboldenedbirth.com/>** (launched November 23, 2026):

- **Website:** <https://emboldenedbirth.com/> (the old preview address now forwards there)
- **GitHub repository:** <https://github.com/tessamillerick/emboldened-birth-site>
- **Local folder:** `/home/sean/emboldened-birth-site`

Search engines may list it now; it can take a few weeks before it shows up in Google. The domain's DNS is at Porkbun. Your Proton email records there were left exactly as they were: never delete the MX, TXT, `_dmarc` or `protonmail…_domainkey` records.

## 1. See it

Open the website above, or preview locally:

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
- No cookies, analytics, advertising trackers, or contact forms. Contact is by email, phone, or text.
- Fonts are self-hosted, so no requests go to Google Fonts.
- The design matches your business card: warm ivory, copper, and deep eucalyptus; Cormorant Garamond with Source Sans 3; and original watercolor eucalyptus painted for the site by `tools/generate-botanicals.py` (no template or stock art).
- A thin deep green bar across the top of every page says the first consultation is free and links to Contact.
- On phones and tablets, Home, About and Services have a contact bar at the bottom of the screen (Email, Text, Call), so a visitor can always reach you without scrolling back.
- The site is public, and search engines are allowed to list it.

## 3. How to update the site

Edit the files in this folder, preview locally, then save and publish the change:

```sh
cd /home/sean/emboldened-birth-site
git add -A
git commit -m "Describe the change"
git push
```

GitHub Pages rebuilds automatically after a push. It usually takes about a minute. Check the website afterward.

Your GitHub account is active on this machine. You can confirm with:

```sh
gh auth status
```

Your local Git identity is already set to `Tessa Millerick <tessamillerick@users.noreply.github.com>`, so future commits use your GitHub noreply address instead of your personal email.

## 4. Add your portrait

The home page and the About page each have an arch-shaped frame for your photo. Until you add one, it shows a botanical print.

1. Pick a warm, natural-light photo in portrait (vertical) orientation, at least 1000 × 1250 pixels. The frame crops to a 4:5 shape and rounds off the top corners into an arch, so your face should sit in the middle, with some room above your head.
2. Save it in the site folder as `assets/img/tessa-portrait.jpg`.
3. In `index.html` and `about.html`, find the comment that starts with `PORTRAIT:`. Two lines below it, change

   ```html
   <img class="portrait__print" src="assets/img/botanical-bouquet.webp" alt="" width="881" height="1102" fetchpriority="high">
   ```

   to

   ```html
   <img src="assets/img/tessa-portrait.jpg" alt="Tessa Millerick, birth doula" width="1000" height="1250" fetchpriority="high">
   ```

   The new line has no `class`: that is what lets the photo fill the arch edge to edge. Use your photo's real width and height, and describe the photo in the `alt` text (for example, “Tessa Millerick smiling outdoors in Hidden Valley Lake”).
4. Preview locally, then commit and push (section 3).

You can use two different photos: a portrait on the home page and a candid one on the About page.

## 5. Still to do, and things to keep true

- The **$750 introductory rate** wording is confirmed (2026-11-23): $250 retainer, and the $500 balance due 4 weeks before the due date. Keep it matching the contract.
- Service area confirmed: **Lake, Sonoma, and Napa Counties**. Confirm whether travel beyond those counties is offered.
- Your CPR certification (American Red Cross, valid until **November 17, 2028**) is on the About page. Renew it before then, or take the CPR sentence and the CPR line off the page.
- Free consultation: decided. The site says the first consultation is free, with no obligation.
- Add your portrait (section 4).
- No backup doula is mentioned anywhere on the site until you have a backup you know is reliable. Ask to have it put back then.
- Don't call yourself a certified doula until CD(DONA) is complete.

## 6. If something goes wrong

- The site is static; you can always preview it locally.
- See recent commits with `git log --oneline`.
- Undo an uncommitted edit with `git restore <file>`.
- GitHub Pages build status is in **Settings → Pages** and the **Actions** tab.
- If a push fails, check `gh auth status` and switch to your account with `gh auth switch --user tessamillerick`.
- Do not change DNS as a troubleshooting step.

## 7. Account cleanup

Your GitHub account is active. Sean's accounts are still stored on this machine:

- `SRMillerick`
- `sean-adoraway`

After you are comfortable with the repository and your own login, you can remove them:

```sh
gh auth logout --hostname github.com --user SRMillerick
gh auth logout --hostname github.com --user sean-adoraway
```

Do not remove them until your account and the repository are working. The first setup commits were authored with Sean's email; future commits use your name and GitHub noreply address. Rewriting the old commits is a separate step if you ever want it.

## 8. Where things live

- Website: `/home/sean/emboldened-birth-site`
- Website: <https://emboldenedbirth.com/>
- Planning handoff: `/home/sean/emboldened-birth-handoff-2026-10-27`
- Private research repository: `/home/sean/doula-cert-ca`
