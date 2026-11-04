# Tessa — start here

This is your website, built as a plain static site for GitHub Pages. It currently exists only as a **local preview**. Nothing has been published to GitHub, and the custom domain and DNS have not been changed.

## 1. See it

The preview server is probably already running. Open:

**http://127.0.0.1:8000**

If it is not running, start it from this folder:

```sh
cd /home/sean/emboldened-birth-site
python3 -m http.server 8000
```

Then open <http://127.0.0.1:8000>. Stop the server with `Ctrl+C`.

## 2. What is here

- Home, About, Services, Contact, Privacy, and a custom 404 page.
- Plain HTML and CSS. No build step and no JavaScript.
- No cookies, analytics, advertising trackers, or contact forms. Contact is by email and phone.
- Fonts are self-hosted, so no requests go to Google Fonts.
- The design uses the cream, sage, and blush palette and floral artwork from your business card.
- The site is currently marked `noindex`, and `robots.txt` blocks search engines while it is a draft.

## 3. Publish under your GitHub account

This machine currently has **Sean's GitHub accounts** signed in. Add yours and switch to it before creating the repository.

1. Check who is signed in:

   ```sh
   gh auth status
   ```

2. Sign in as yourself. Choose GitHub.com, HTTPS, and “Login with a web browser”:

   ```sh
   gh auth login
   ```

3. Switch to your account:

   ```sh
   gh auth switch --user tessamillerick
   ```

4. Set your Git identity for future commits. A commit email is visible in a public repository, so use the GitHub **noreply** address from Settings → Emails if you want to keep your personal address private:

   ```sh
   git config user.name "Tessa Millerick"
   git config user.email "YOUR_GITHUB_NOREPLY_EMAIL"
   ```

5. Create a **public** repository under your account and push the site:

   ```sh
   cd /home/sean/emboldened-birth-site
   gh repo create tessamillerick/emboldened-birth-site --public --source=. --remote=origin --push
   ```

6. Turn on GitHub Pages:

   - Open `https://github.com/tessamillerick/emboldened-birth-site/settings/pages`
   - Source: **Deploy from a branch**
   - Branch: **main**, folder: **/ (root)**
   - Save.

7. Wait a minute, then open:

   **https://tessamillerick.github.io/emboldened-birth-site/**

   It should look like the local preview. It will stay out of search results until you remove the `noindex` tag.

If you would rather not use the command line, create an empty public repository on github.com and add `SRMillerick` as an **Admin** collaborator. Do not share your password or a personal access token in chat.

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
- Do not change DNS as a troubleshooting step.

## 6. Account cleanup

After your own GitHub account is working and the repository is pushed, Sean should remove his accounts from this machine if he no longer needs them here:

```sh
gh auth logout --hostname github.com --user SRMillerick
gh auth logout --hostname github.com --user sean-adoraway
```

Do not do this until your account and the repository are working.

## 7. Where things live

- Website: `/home/sean/emboldened-birth-site`
- Planning handoff: `/home/sean/emboldened-birth-handoff-2026-10-27`
- Private research repository: `/home/sean/doula-cert-ca`
