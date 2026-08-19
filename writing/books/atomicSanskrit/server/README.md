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
  with what known email (if any) and which Hypothesis group(s) — `groups`
  is an array, so a reader can be in more than one. Deployed to
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

4a. **Install the whitelist-reload trigger** (see "oauth2-proxy needs a
    reload" below for why this exists):
   ```
   sudo cp server/oauth2-proxy-whitelist-reload.path server/oauth2-proxy-whitelist-reload.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now oauth2-proxy-whitelist-reload.path
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

## One-time setup: the per-reader dashboard resolver

`/as/private/dashboard/*` used to be a static-file handler, owner-only —
everyone else got a 404. It's now `dashboard_resolver.py`
(`server/dashboard_resolver.py`), which maps the authenticated visitor's
email to their own scoped reader page, built by
`hypothesis/build_dashboard.py --readers`. See that script's module
docstring for the full design and why it runs as `www-data`, and
`working/10_active/as_reader_dashboards_plan.md` for the feature design.

1. **Create the shared directory** the resolver reads from and the
   dashboard cron job (`hypothesis/refresh_dashboard.sh`, runs as `ubuntu`)
   writes to. Neither user can read/write the other's home or `/etc`
   territory directly (`ubuntu`'s home is `750 ubuntu:ubuntu`;
   `/etc/secondshanti` is `640 www-data:www-data`) — this directory is the
   one place both meet, `ubuntu` owning it so cron can write, `www-data` in
   its group with the setgid bit so files `ubuntu` creates are readable by
   the resolver without a second `chgrp`:
   ```
   sudo mkdir -p /var/lib/secondshanti/dashboard_readers
   sudo chown ubuntu:www-data /var/lib/secondshanti/dashboard_readers
   sudo chmod 2750 /var/lib/secondshanti/dashboard_readers
   ```

2. **Copy the resolver script and install its service:**
   ```
   sudo cp server/dashboard_resolver.py /opt/secondshanti/
   sudo cp server/dashboard-resolver.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now dashboard-resolver
   sudo systemctl status dashboard-resolver
   ```

3. **Deploy the Caddyfile** (already routes `/as/private/dashboard/*` to
   `127.0.0.1:8091` — see the Caddyfile's own comment at that block):
   ```
   ./deploy.sh
   ```

4. **First reader-page build:** either wait for the next 15-minute cron
   tick, or run by hand:
   ```
   cd /home/ubuntu/projects/writing/books/atomicSanskrit/hypothesis
   ./refresh_dashboard.sh
   ls /var/lib/secondshanti/dashboard_readers/
   ```

5. **Test:** sign in as a whitelisted reader and confirm their own scoped
   page loads at `/as/private/dashboard/`; sign in as the owner and confirm
   the full triage dashboard still loads unchanged, and that
   `?as=<slug>` previews a specific reader (banner reads "Previewing as
   ...", composer/TODO absent).

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

### Readers in more than one group

A roster entry's `groups` is an array, so a reader can belong to several
reading groups; their dashboard shows the union, and their invite page
gets one join button per group. Add a second group with `--add-group`:

```
python3 add_invite.py rm "R. Kumar" https://hypothes.is/groups/GhI789z/another-group --add-group
```

Without `--add-group` the array is **replaced** by the single group given.

**Prefer adding over moving.** A Hypothesis annotation's group is fixed
when it is created and cannot be changed afterwards — the API silently
drops `group` on `PATCH` and returns `200`, so a "move" looks like it
worked and does nothing. Replacing a reader's group therefore strands
every note they have already written: it stays in the old group, and
their dashboard — now scoped to the new one — shows none of their own
history. Adding a group keeps the old notes and gains the new ones.

Entries are matched to annotations by the **group id** parsed out of the
URL, not by `name`. Group ids are immutable; names are not (group
`QpG9pDKd` was renamed `as-pr` → `as-pr-sr` on 2026-08-19). `name` is for
display, and is the fallback only when a URL carries no parseable id.

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

**oauth2-proxy needs a reload — its own file-watcher is not reliable
enough to trust.** oauth2-proxy ships a live watcher for
`authenticated-emails.txt` (visible in its startup log: `watching '...'
for updates`), and a same-day test on 2026-08-06 — append, then
immediately log in with the new email — worked with no restart. But a
real invite on 2026-08-15 (jk) was appended correctly, oauth2-proxy's own
logs showed it reading the exact matching email back, and it still
rejected him with `AuthFailure ... unauthorized` — the watcher had gone
stale sometime after nine days of uptime and never picked up the file
change. A restart fixed it instantly.

The service can't just `sudo systemctl restart oauth2-proxy` itself:
it runs as `www-data` with `NoNewPrivileges=true`
(`secondshanti-request-access.service`), which blocks `sudo` outright
regardless of any sudoers entry, and a scoped polkit rule for the
systemd D-Bus restart action didn't fire reliably in testing either.
Instead, `add_to_whitelist()` touches a trigger file
(`WHITELIST_RELOAD_TRIGGER`, default
`/var/lib/secondshanti/reload-oauth2-proxy`) that it already has write
access to via `ReadWritePaths`, and a root-owned systemd `.path` unit
does the actual restart:

```
sudo cp server/oauth2-proxy-whitelist-reload.path server/oauth2-proxy-whitelist-reload.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now oauth2-proxy-whitelist-reload.path
```

The `.path` unit watches for the trigger file's existence, fires the
`.service` unit (root, `Type=oneshot`), which restarts oauth2-proxy and
removes the trigger file. Confirmed end-to-end 2026-08-15: touching the
trigger as `www-data` restarted oauth2-proxy in under a second with no
privilege escalation anywhere in the chain.

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
