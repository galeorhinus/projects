# Request-access service

A tiny loopback-only HTTP service with two flows for getting a reader from
"doesn't have access" to "whitelisted." Neither flow grants access without
either a trust decision already made (a named invite) or a human review
(the generic form / a leaked or mismatched invite link).

**Flow 1 — generic, `secondshanti.org/as/request-access`.** For strangers
you don't know. Every submission is logged and emailed to you; nothing is
auto-granted.

**Flow 2 — named invites, `secondshanti.org/as/invite/<slug>`.** For
people you deliberately invited by name. Adding the roster entry *is* the
approval, so submissions here are handled by trust tier:

- roster has a known email for that slug → auto-whitelist if the
  submitted email matches it, else manual review (unexpected email)
- roster has no known email for that slug (bare-slug, "trust on first
  use") → the *first* submission auto-whitelists **and locks** the slug
  to that email; a repeat submission of the same email is an idempotent
  no-op (not a second grant); a *different* email showing up at an
  already-locked slug is manual review, flagged as a possible leaked
  invite link
- generic `/as/request-access` submissions → always manual review

## The roster / status split

Invite data lives in two separate files with two separate authority
models — this is the load-bearing design decision, so read this section
before touching either file.

- **`invite_roster.json`** — admin-authored, git-tracked (this repo, this
  file: `server/invite_roster.json`). Who you invited, under what slug,
  with what known email (if any) and what Hypothesis group. Deployed to
  `/etc/secondshanti/invite_roster.json`, **read-only** to the running
  service (installed by `deploy.sh`, owned by `www-data`, mode 640 —
  the service's systemd unit does not grant it write access via
  `ReadWritePaths`, so even a bug in the service code can't corrupt the
  roster).
- **`invite_status.json`** — service-authored, server-only, **never
  git-tracked, never committed**. Lives at
  `/etc/secondshanti/invite_status.json`. Tracks what actually happened
  per slug at runtime: `used`, `locked_email`, `status`
  (`whitelisted` / `pending_review`), `submitted_email`,
  `hypothesis_username`, `submitted_at`, and (for the leaked-link case)
  a `review_attempts` list of every mismatched submission against an
  already-locked slug, so a later legitimate attempt never clobbers the
  record of the original successful grant.

Splitting these was a correctness fix, not just a tidiness one: the old
single `invites.json` mixed admin-authored fields with live-written
fields in the same record, so there was no way to redeploy the roster
from git without either wiping live status data or needing to merge
around it by hand. Now a roster redeploy (`deploy.sh`) never touches
status, and the service never touches the roster.

**Why the roster can live in this (private) repo.** The repo is private
with no plan to make it public, so the emails in `invite_roster.json`
carry no more exposure than any other file here. `authenticated-emails.txt`
(the actual OAuth whitelist) is deliberately *not* pre-seeded from the
roster and stays 100% server-authoritative — every real grant is the
result of a confirmed request/invite-use event, not a repo push, so
pushing the roster alone never grants anyone access by itself.

Files:

- `request_access.py` — the service (pure standard library, no `pip
  install` needed). Handles both flows, dispatching on path.
- `secondshanti-request-access.service` — systemd unit to run it
  persistently. `invite_roster.json` is deliberately absent from its
  `ReadWritePaths` (see the comment in the unit file) — `ProtectSystem
  =strict` makes `/etc` read-only by default, so leaving it out is what
  makes the roster genuinely read-only to the service.
- `add_invite.py` — CLI to add/update a roster entry without hand-editing
  JSON. **Run this locally against the repo, not on the server** — see
  below.
- `invite_roster.example.json` — schema reference for the roster file
  (fake data, safe to read).
- The Caddy routes live in the repo's `Caddyfile`: `/as/request-access*`
  and `/as/invite/*`, both proxied to `127.0.0.1:8090`, both deliberately
  outside the oauth2-proxy gate — reaching either is exactly how someone
  without access yet gets in.

## One-time server setup

1. **Copy the scripts.**
   ```
   sudo mkdir -p /opt/secondshanti
   sudo cp server/request_access.py /opt/secondshanti/
   ```
   (`add_invite.py` runs locally, not on the server — see "Adding a
   named invite" below. No need to copy it up.)

2. **Create the state directories** (outside the web root, never
   git-tracked):
   ```
   sudo mkdir -p /var/lib/secondshanti /etc/secondshanti
   sudo chown www-data:www-data /var/lib/secondshanti /etc/secondshanti
   ```
   `invite_status.json` will be created inside `/etc/secondshanti/` the
   first time the service writes to it. `invite_roster.json` is installed
   by `deploy.sh` (see below), not created by the service.

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

5. **Deploy the Caddyfile and the roster:**
   ```
   ./deploy.sh
   ```
   (or, from the server, `sudo caddy validate --config /etc/caddy/Caddyfile
   && sudo systemctl reload caddy` plus the roster-install step in
   `deploy.sh` by hand if you're not running the full script).

6. **Test the generic flow:** visit `https://secondshanti.org/as/request-access`,
   submit the form, confirm the notification email arrives and a line was
   appended to `/var/lib/secondshanti/access-requests.log`.

## Adding a named invite

Run this **locally**, against the repo — the roster is git-tracked, and
`deploy.sh` is what installs it to the server. Running it directly on the
server edits a file nothing will ever redeploy from and that isn't
backed up in git.

```
cd server
python3 add_invite.py jk "JK" https://hypothes.is/groups/AbC123x/reading-group jk@known-email.com
```

Leave off the email if you don't have it yet (bare-slug, trust-on-first-use):

```
python3 add_invite.py rm "R. Kumar" https://hypothes.is/groups/DeF456y/reading-group
```

This prints the invite link to send them: `secondshanti.org/as/invite/rm`.
Then:

```
git add server/invite_roster.json
git commit -m "Add invite: rm"
git push
ssh amrut 'cd ~/projects/writing/books/atomicSanskrit && ./refresh.sh'
```

(`refresh.sh` pulls, rebuilds, and runs `deploy.sh`, which installs the
new roster. No service restart is needed — the roster is read fresh on
every request.)

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
manual queue as the generic form. Two distinct cases, distinguished in
the notification email's subject and reason text:

- **First-touch mismatch** — the roster has a known email on file for
  the slug, and the submission doesn't match it. Probably just a
  different address they prefer; check and, if it's really them, add
  the *submitted* email to the whitelist yourself.
- **Possible leaked link** — the slug has no known roster email (it was
  a bare-slug, trust-on-first-use invite), it's already locked to a
  *different* email from an earlier successful grant, and this
  submission doesn't match that locked email. Someone may have
  forwarded their personal invite link. The original grant's status is
  left untouched (it's still recorded as `used`/`locked_email` in
  `invite_status.json`); this new attempt is appended to that slug's
  `review_attempts` list instead of overwriting anything, so you can see
  the full history — who got in first, and who else has since tried the
  same link — before deciding whether to also whitelist the new
  submitter or ignore it.

## Notes

- Both forms have a honeypot field (`website`) and a 60-second per-IP
  throttle (shared across both routes); neither is bulletproof bot
  protection, just enough friction for a low-traffic invite-only site.
  Tighten if it starts attracting spam.
- `invite_status.json` is the live status tracker — each record picks up
  `used`, `locked_email`, `status` (`whitelisted` / `pending_review`),
  `submitted_email`, `hypothesis_username`, `submitted_at`, and (leaked-
  link case only) `review_attempts` once someone uses their link, so
  `cat /etc/secondshanti/invite_status.json` gives you an at-a-glance
  view of who's actually gotten in. It is never git-tracked and never
  redeployed from the repo — it's purely server-side runtime state.
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
  (or written to `invite_status.json`) first; email is best-effort on
  top of that.
- `add_invite.py` writes `invite_roster.json` without file-locking. Fine
  for its actual use (you, running it by hand, locally, occasionally) —
  it never runs on the server and never races against the live service,
  which only ever reads the roster.
