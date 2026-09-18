# Reader invite instructions (WhatsApp)

The four operational steps every new advance reader needs. Both
`friends_advance_reader_whatsapp.md` and its short sibling end with "the
instructions are in the link below" — this is that content, kept in one place so
it does not get retyped per reader and drift.

Fill three values from the reader's entry in `server/invite_roster.json`:

| Placeholder | Where it comes from | Example |
|---|---|---|
| `{{SLUG}}` | the entry's key | `bk` |
| `{{EMAIL}}` | the entry's `email` | `gbkansara@gmail.com` |
| `{{GROUP}}` | the entry's `groups[].name` | `as-bk-rs` |

Send only after `./deploy.sh` has run on amrut. The deploy installs the roster,
rebuilds the pages so the reader's group enters `groupsAllowlist`, and runs
`check_roster_sync.py`. Before that, the group is not selectable in the sidebar
— which is the exact condition that sends a new reader to the public group.

## The message

WhatsApp formatting is not standard Markdown: `*asterisks*` are **bold** and
`_underscores_` are _italic_, the reverse of what a Markdown habit produces.

```
{{NAME}} — the draft of _Atomic Sanskrit_ is ready for you.

Start here: https://secondshanti.org/as/invite/{{SLUG}}

1. Sign in with *{{EMAIL}}* — it has to be that address, or it goes to manual review.
2. That's all you need to read the book.
3. To leave comments, create a free account at hypothes.is (separate from the Google sign-in).
4. Then join your reading group, *{{GROUP}}*, *before* you start highlighting. If you skip that step your notes go to Hypothesis's public group, where anyone on the internet can read them — and they can't be moved afterwards.

Margin comments are ideal, but WhatsApp or email is fine too.

It's the pre-publication manuscript, so please don't circulate it without checking with me.
```

## Why step 4 is not optional

A reader who annotates before joining their group posts to Hypothesis's public
group, and four already have. Those annotations are readable by anyone with no
account and no token — on an unpublished manuscript — and they cannot be
relocated afterwards: an annotation belongs to its author, a reply inherits its
parent's group, and `move_annotation.py` refuses both cases. The pipeline now
collects public annotations so they at least reach the dashboard, but the
exposure is permanent. One sentence in the invite prevents it.

## After they sign up

Add `hypothesis_username` to their roster entry. Without it their own notes and
your replies do not reach their reader dashboard, which is how one reader asked
five questions, was answered, and saw an empty page.
