# Domain email

Mail to `paragtope@secondshanti.org` and `paragtope@atomicsanskrit.org` is
received by Mailgun and forwarded to `paragtope@gmail.com`. Two pieces make
that work, and only one of them is scripted: DNS is edited by hand at two
different providers, and the Mailgun routes are created by
`setup_routes.py`.

## DNS

The two domains are **not** at the same provider, whatever the registrar
listing says:

| Domain | Nameservers | Edit DNS at |
|---|---|---|
| `secondshanti.org` | `ns-cloud-*.googledomains.com` | Squarespace (its Google-Domains-era backend) |
| `atomicsanskrit.org` | `*.ns.porkbun.com` | Porkbun |

Add each **root** domain to Mailgun — not `mg.<domain>`. Mailgun steers you
toward a subdomain, which is right for a domain that only sends; these have to
receive mail addressed to `@<domain>`, so the MX belongs on the root and the
Mailgun domain has to match it.

| Type | Host | Value | For |
|---|---|---|---|
| MX | `@` | `mxa.mailgun.org` priority 10 | receiving |
| MX | `@` | `mxb.mailgun.org` priority 10 | receiving |
| TXT | `@` | `v=spf1 include:mailgun.org ~all` | sending |
| TXT | `<selector>._domainkey` | the DKIM key Mailgun generates | sending |
| CNAME | `email` | `mailgun.org` | click tracking (optional) |

Copy the TXT values from Mailgun's own panel; the DKIM key is per domain.
Neither domain's A record is touched — both keep pointing at amrut.

## Routes

```
export MAILGUN_API_KEY=...        # Settings -> API Keys -> private API key
python mail/setup_routes.py --dry-run
python mail/setup_routes.py
```

The private API key is required: the Routes API is account-scoped, so a domain
sending key returns 401. For an EU-region account also set
`MAILGUN_API_BASE=https://api.eu.mailgun.net` — the US base answers an EU
account with a 401 too, which reads as a bad key rather than a wrong region,
so the script says so when it sees one.

Rerunning is safe. The script creates only what is missing, reports a route
that exists but forwards somewhere unexpected rather than overwriting it, and
first prints each domain's verification state — a route on an unverified
domain is accepted by the API and then never fires, because no mail arrives.

Addresses live in `FORWARDS` at the top of the script. A third domain is one
line plus a rerun.

## Replying from these addresses

Forwarding only brings mail in. To answer as `paragtope@secondshanti.org`:
Gmail → Settings → Accounts and Import → **Send mail as**, SMTP
`smtp.mailgun.org` port 587 with the domain's SMTP credentials from Mailgun.
Do this after forwarding works — Gmail sends a confirmation code to the
address, which has to reach the inbox first.

## Known limits

Forwarding rewrites the envelope sender, so SPF passes and the original
sender's DKIM signature normally survives, which is what carries DMARC at
Gmail. Mail from a strict-DMARC sender still lands in spam occasionally. That
is inherent to forwarding rather than a Mailgun setting.

No DMARC record is published yet. Once sending is in use, start at
`_dmarc` TXT → `v=DMARC1; p=none; rua=mailto:paragtope@gmail.com` and tighten
only after reading the reports.
