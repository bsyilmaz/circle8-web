# circle8 landing page

Waitlist site for Twitter/X ads. Email capture + live counter.

## Setup (5 minutes)

**1. Create the form backend (Google Sheets + Apps Script, free)**
   - Go to https://sheets.google.com and create a new spreadsheet (name it "circle8 waitlist")
   - Menu: **Extensions > Apps Script**
   - Delete the sample code, paste the contents of `apps_script.gs`
   - Click **Deploy > New deployment** (gear icon > Web app)
   - Settings: *Execute as: Me*, *Who has access: Anyone* → **Deploy** → copy the URL

**2. Connect the form**
   - Open `index.html`, find `FORM_ENDPOINT = "PASTE_APPS_SCRIPT_URL_HERE"` near the bottom
   - Paste your URL between the quotes. Done.

**3. Publish (pick one)**
   - **Fastest:** drag the `website` folder onto https://app.netlify.com/drop → you get a live URL
   - **Or** GitHub Pages: push this folder to a public repo, Settings > Pages > main branch
   - Test: submit an email → it appears as a new row in your spreadsheet

## Files

| File | What it is |
|---|---|
| `index.html` | The landing page (single file, no build step) |
| `apps_script.gs` | Backend: stores emails in Google Sheets, returns the signup count |
| `og.png` | Social preview image for Twitter/X cards |
| `make_og.py` | Regenerates `og.png` if you want to change the text |

## Notes

- The counter on the page is live (reads from the spreadsheet).
- Honeypot field blocks simple bots. Don't run ads to bots-heavy audiences blindly.
- Emails are only stored in your Google Sheet. Nothing else touches them.
