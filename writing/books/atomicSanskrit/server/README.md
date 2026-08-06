# Request-access service

A tiny loopback-only HTTP service that handles the public "I don't have
access yet" flow for `secondshanti.org/as/request-access`. It never grants
access by itself — it only logs a request and emails the owner. A human
always decides whether to actually add someone to the whitelist and a
Hypothesis group.

Files:

- `request_access.py` — the service (pure standard library, no `pip install`
  needed).
- `secondshanti-request-access.service` — systemd unit to run it persistently.
- The Caddy route lives in the repo's `Caddyfile` (`/as/request-access*`,
  proxied to `127.0.0.1:8090`, deliberately outside the oauth2-proxy gate).

## One-time server setup

1. **Copy the script.**
   ```
   sudo mkdir -p /opt/secondshanti
   sudo cp server/request_access.py /opt/secondshanti/
   ```

2. **Create the log directory** (outside the web root, never git-tracked):
   ```
   sudo mkdir -p /var/lib/secondshanti
   sudo chown www-data:www-data /var/lib/secondshanti
   ```

3. **Generate a Gmail App Password** (the service sends its notification
   email via Gmail SMTP as `rhinusgaleo@gmail.com`):
   - Requires 2-Step Verification enabled on that Google account.
   - Generate one at <https://myaccount.google.com/apppasswords>.
   - Save it, restricted, where only the service can read it:
     ```
     sudo mkdir -p /etc/secondshanti
     echo 'the-16-char-app-password' | sudo tee /etc/secondshanti/smtp-app-password
     sudo chown www-data:www-data /etc/secondshanti/smtp-app-password
     sudo chmod 600 /etc/secondshanti/smtp-app-password
     ```

4. **Install and start the systemd service:**
   ```
   sudo cp server/secondshanti-request-access.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now secondshanti-request-access
   sudo systemctl status secondshanti-request-access
   ```

5. **Reload Caddy** after deploying the updated `Caddyfile`:
   ```
   sudo systemctl reload caddy
   ```

6. **Test it:** visit `https://secondshanti.org/as/request-access`, submit
   the form, confirm the notification email arrives and a line was appended
   to `/var/lib/secondshanti/access-requests.log`.

## Review workflow (manual, by design)

1. A request email arrives (or check `/var/lib/secondshanti/access-requests.log`
   directly — one JSON object per line: `name`, `email`, `note`, `ip`, `time`).
2. Decide whether to approve. If yes:
   - Add the email to `/etc/oauth2-proxy/authenticated-emails.txt` and reload
     oauth2-proxy.
   - Add them to the appropriate Hypothesis group, and to your own
     group→person mapping file (kept outside this repo, alongside the
     whitelist — see the main project's `CLAUDE.md` for the reasoning).
   - Reply to them (the notification email's Reply-To is already set to
     their submitted address) with their reading link and Hypothesis group
     invite link.
3. If declining or ignoring spam/bot submissions, no action is needed —
   nothing is auto-granted.

## Notes

- The form has a honeypot field (`website`) and a 60-second per-IP
  throttle; neither is bulletproof bot protection, just enough friction for
  a low-traffic invite-only form. Tighten if it starts attracting spam.
- `BIND_PORT` (8090) was chosen to avoid the existing `4180` (oauth2-proxy)
  and `18080` (book content loopback listener). Change it in both
  `request_access.py` and the `Caddyfile` route together if it ever
  collides with something else on the host.
- Email delivery failure doesn't lose the request — it's logged to disk
  first, email is best-effort on top of that.
