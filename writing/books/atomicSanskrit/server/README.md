# Request-access service

A tiny loopback-only HTTP service with two flows for getting a reader from
"doesn't have access" to "whitelisted." Neither flow grants access without
either a trust decision already made (a named invite) or a human review
(the generic form / an invite used with an unexpected email).

**Flow 1 — generic, `secondshanti.org/as/request-access`.** For strangers
you don't know. Every submission is logged and emailed to you; nothing is
auto-granted.

**Flow 2 — named invites, `secondshanti.org/as/invite/<slug>`.** For
people you deliberately invited by name. Creating the `invites.json` entry
*is* the approval, so submissions here are handled by trust tier:

- no email on file for that slug → auto-whitelist whatever they submit
- submitted email matches the one on file → auto-whitelist
- submitted email differs from the one on file → falls back to the same
  manual-review path as the generic form, clearly flagged as unexpected

Files:

- `request_access.py` — the service (pure standard library, no `pip
  install` needed). Handles both flows, dispatching on path.
- `secondshanti-request-access.service` — systemd unit to run it
  persistently.
- `add_invite.py` — CLI to add/update a named invite without hand-editing
  JSON.
- `invites.example.json` — schema reference (fake data, safe to read; the
  real file lives only on the server, never in git).
- The Caddy routes live in the repo's `Caddyfile`: `/as/request-access*`
  and `/as/invite/*`, both proxied to `127.0.0.1:8090`, both deliberately
  outside the oauth2-proxy gate — reaching either is exactly how someone
  without access yet gets in.

## One-time server setup

1. **Copy the scripts.**
   ```
   sudo mkdir -p /opt/secondshanti
   sudo cp server/request_access.py server/add_invite.py /opt/secondshanti/
   ```

2. **Create the state directories** (outside the web root, never
   git-tracked):
   ```
   sudo mkdir -p /var/lib/secondshanti /etc/secondshanti
   sudo chown www-data:www-data /var/lib/secondshanti /etc/secondshanti
   ```
   `invites.json` will be created inside `/etc/secondshanti/` the first
   time you run `add_invite.py` or the service touches it.

3. **Generate a Gmail App Password** (the service sends its notification
   email via Gmail SMTP as `rhinusgaleo@gmail.com`):
   - Requires 2-Step Verification enabled on that Google account —
     App Passwords are hidden entirely until 2SV is on.
   - Generate one at <https://myaccount.google.com/apppasswords>.
   - Save it, restricted, where only the service can read it:
     ```
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

5. **Deploy the Caddyfile and reload:**
   ```
   sudo caddy validate --config /etc/caddy/Caddyfile
   sudo systemctl reload caddy
   ```

6. **Test the generic flow:** visit `https://secondshanti.org/as/request-access`,
   submit the form, confirm the notification email arrives and a line was
   appended to `/var/lib/secondshanti/access-requests.log`.

## Adding a named invite

```
cd /opt/secondshanti
python3 add_invite.py jk "JK" https://hypothes.is/groups/AbC123x/reading-group jk@known-email.com
```

Leave off the email if you don't have it yet:

```
python3 add_invite.py rm "R. Kumar" https://hypothes.is/groups/DeF456y/reading-group
```

This prints the invite link to send them: `secondshanti.org/as/invite/rm`.

**Confirmed: oauth2-proxy does not need a reload.** Tested end-to-end
2026-08-06 — appending to `/etc/oauth2-proxy/authenticated-emails.txt` and
immediately logging into `/as/book/` with the newly-added email worked
with no restart of anything. `WHITELIST_RELOAD_COMMAND` can stay `None`;
no sudo privileges need to be granted to the service user for this.

## Review workflow

**Generic form submissions** (always manual):
1. A request email arrives (or check
   `/var/lib/secondshanti/access-requests.log` directly — one JSON object
   per line: `name`, `email`, `note`, `ip`, `time`).
2. Decide whether to approve. If yes, add the email to
   `/etc/oauth2-proxy/authenticated-emails.txt`, add them to the
   appropriate Hypothesis group, and reply to them (the notification
   email's Reply-To is already set to their submitted address) with their
   reading link and the group invite link.
3. If declining or ignoring spam, no action needed — nothing is
   auto-granted.

**Named-invite submissions matching the trust rules above** need no
action — you'll get an "Auto-approved" notification email as an FYI.

**Named-invite submissions with an unexpected email** land in the same
manual queue as the generic form, clearly labeled with the slug and both
the expected and submitted email, so you can quickly tell whether it's
really them (maybe they just prefer a different address) before adding
the *submitted* email to the whitelist yourself.

## Notes

- Both forms have a honeypot field (`website`) and a 60-second per-IP
  throttle (shared across both routes); neither is bulletproof bot
  protection, just enough friction for a low-traffic invite-only site.
  Tighten if it starts attracting spam.
- `invites.json` doubles as a lightweight status tracker — each record
  picks up `status` (`invited` → `whitelisted` or `pending_review`),
  `submitted_email`, `hypothesis_username`, and `submitted_at` once
  someone uses their link, so `cat /etc/secondshanti/invites.json` gives
  you an at-a-glance view of who's actually gotten in.
- Hypothesis doesn't hand out a "confirmation code" for joining a group —
  the `hypothesis_username` field is a self-reported convenience for your
  own bookkeeping (linking the slug to their actual Hypothesis identity),
  not a verified fact. Don't rely on it if you ever need real proof of
  membership.
- `BIND_PORT` (8090) was chosen to avoid the existing `4180` (oauth2-proxy)
  and `18080` (book content loopback listener). Change it in both
  `request_access.py` and both `Caddyfile` routes together if it ever
  collides with something else on the host.
- Email delivery failure doesn't lose the request — it's logged to disk
  (or written to `invites.json`) first; email is best-effort on top of
  that.
- `add_invite.py` writes `invites.json` without the same file-locking the
  running service uses. Fine for its actual use (you, running it by hand,
  occasionally) — just don't script it to run concurrently with itself or
  expect it to race safely against a live submission at the same instant.
