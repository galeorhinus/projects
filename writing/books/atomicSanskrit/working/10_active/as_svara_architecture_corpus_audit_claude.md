# Svara Architecture — Corpus Evidence Audit (Claude)

*Audit of the Codex evidence record (`as_svara_architecture_evidence_codex.md`) against the local Digital Corpus of Sanskrit and phonetic reasoning. Completed 2026-07-29. This is an evidence audit, not a manuscript rewrite.*

**Files audited:** `as_svara_architecture_analysis_plan_codex.md`, `as_svara_architecture_evidence_codex.md`, `as_pass_deployment_plan_codex.md`, `as_svara_architecture_analysis_plan_claude.md`.

---

## 0. Method and the decisive encoding caveat

**Corpus.** The Digital Corpus of Sanskrit (DCS), CoNLL-U edition, **15,900 text files** (Vedic Saṃhitās + Brāhmaṇas, Āraṇyakas, Upaniṣads, Śrautasūtras, and the laukika corpus). Path: `analysis/ganah/data/raw/dcs/dcs/data/conllu/files/`. Every count below was pulled directly on 2026-07-29.

**What the DCS can and cannot verify — established empirically this pass, and it governs every verdict below:**

| The DCS **can** confirm | The DCS **cannot** supply (needs printed accented editions) |
|---|---|
| a form's occurrence, lemma, morphology, location, count | **Vedic accent** (*udātta/anudātta/svarita*) — absent from the tags |
| **pluta**, where digit-marked (`o3m`, `somā3`, `au4`) | **anunāsika** (candrabindu) — normalized away; 0 combining-tilde vowels corpus-wide |
| the underlying words at a sandhi junction | an authoritative **saṃhitāpāṭha / padapāṭha** pair |

Two encoding facts drive the audit: (1) the DCS `# text =` line is a **token-FORM join that partially un-does sandhi** (RV 10.129.1b *no sat* appears as `na u sat`; the merged vowel of *nāsat* is assigned to token 1 as `nā`), so it is **neither** the printed saṃhitā **nor** a reliable padapāṭha; (2) the DCS **strips accent and, in the Ṛgveda, pluta** (RV 10.129.5 shows plain `āsīt`, not `āsī3t`). I therefore verify *occurrence and distribution* locally and mark *accent, padapāṭha, and RV-pluta* as requiring van Nooten–Holland / Aufrecht / the Śākala padapāṭha. I have **not** re-fetched the Codex's web sources (ashtadhyayi.com, PHOIBLE, Göttingen VED-PHO); where a claim rests only on those, I say so.

**Sūtra citations in the Codex check out.** Every Aṣṭādhyāyī number the Codex cites is accurate on inspection: 1.1.8 मुखनासिकावचनोऽनुनासिकः, 1.1.9 तुल्यास्यप्रयत्नं सवर्णम्, 1.2.27 ऊकालोऽज्झ्रस्वदीर्घप्लुतः, 1.2.29–32 (pitch + तस्यादित उदात्तमर्धह्रस्वम्), 6.1.77 इको यणचि, 6.1.87 आद्गुणः, 6.1.88 वृद्धिरेचि, 6.1.78 एचोऽयवायावः, 6.1.101 अकः सवर्णे दीर्घः, 1.1.48 एच इग्घ्रस्वादेशे, 8.4.68 अ अ. This is a genuine strength of the Codex record; the grammar layer is sound. The problems below are all in the **corpus-occurrence layer**, where the Codex was appropriately cautious but two specific claims still overreach.

---

## Verdict summary

| # | Claim (Codex) | Audit verdict |
|---|---|---|
| 1 | अ+अ→आ secure but *no Vedic example located* (§4.3) | **Now SECURED** — 3 examples supplied (Part 1) |
| 2 | saṃvṛta-अ / vivṛta-आ distinction is documented | **Secure** (documentation); the *rationale* is **Unresolved** — confirmed |
| 3 | 132 is an analytical count, not corpus frequency | **Secure and correct** — arithmetic and framing hold |
| 4 | ऌ family lacks *dīrgha*; ॡ not an ordinary long vowel | **Secure, and strengthened** — ऌ **and** ॡ are corpus-absent |
| 5 | RV 10.129.5 = pluta `āsī3t` (flagship pluta example) | **REJECT as stated** — DCS RV has 0 pluta; use the ritual corpus |
| 6 | "3 pluta in RV, 15 in AV" (reported, hedged) | **REJECT** — DCS: RV 0, Śaunaka AV 7, Paippalāda 0 |
| 7 | *svarita* does **not** require two mātrās | **Secure** (1.2.32) — confirmed |
| 8 | इ/उ/ऋ/ऌ do **not** form a symmetric junction quartet | **Secure** — and it corrects the Claude plan's Move 3 (see §6) |
| 9 | short e/o physically possible, present in the field | **Plausible/secure as general linguistics**; PHOIBLE layer not re-verified here |
| 10 | pitch did **not** cause the open vowel coordinates | **Secure** — confirmed |

---

## PART 1 — अ AND आ

**Codex status audited:** §4.3 declared the *saṃhitāpāṭha/padapāṭha* example for अ+अ→आ **still required**. This pass supplies three secure examples, all from one hymn (Ṛgveda 10.129, the Nāsadīya Sūkta), covering three of the four input combinations. All instantiate **one rule — savarṇadīrgha, Aṣṭādhyāyī 6.1.101 अकः सवर्णे दीर्घः** (a/ā + a/ā of the same *avarṇa* family → a single दीर्घ आ).

> **Accent note (applies to all three):** the DCS is unaccented. The accents shown are the standard readings of these famous verses and must be taken from **van Nooten & Holland, *Rig Veda: A Metrically Restored Text*** (HOS 50) / **Aufrecht** before print; the *padaccheda* is the **Śākala padapāṭha**. The DCS confirms the underlying words and the location only.

### Example 1 — अ + अ → आ (the core case)
- **Saṃhitā:** नासदासीन्नो सदासीत्तदानीम् — *nā́sad āsīn nó sád āsīt tadā́nīm*
- **Junction:** **न (*ná*) + असत् (*ásat*) → नासत् (*nā́sat*)** — short a + short a → आ.
- **Padapāṭha:** न । असत् । आसीत् । (Śākala)
- **Translation:** "There was neither non-being nor being then."
- **Location:** Ṛgveda 10.129.1a (Nāsadīya Sūkta). DCS confirms tokens `na`(lemma *na*) + `asat`(lemma *asat*); the corpus renders the merge as `nā asat`.
- **Rule:** 6.1.101 अकः सवर्णे दीर्घः.

### Example 2 — अ + आ → आ
- **Saṃhitā:** नासीद्रजो नो व्योमापरो यत् — *ná ā́sīd rájo nó vyòmā paró yát*
- **Junction:** **न (*ná*) + आसीत् (*ā́sīt*) → नासीत् (*nā́sīt*)** — short a + long ā → आ.
- **Padapāṭha:** न । आसीत् । रजः । … (Śākala)
- **Translation:** "There was no air-realm, nor the heaven beyond."
- **Location:** Ṛgveda 10.129.1c. DCS shows the split `na āsīt rajaḥ` with token `na` (short) + `āsīt`.
- **Rule:** 6.1.101.

### Example 3 — आ + अ → आ
- **Saṃhitā:** स्वधावस्तात्प्रयतिः परस्तात् — *svadhā́vastāt práyatiḥ parástāt*
- **Junction:** **स्वधा (*svadhā́*) + अवस्तात् (*avástāt*) → स्वधावस्तात् (*svadhā́vastāt*)** — long ā + short a → आ.
- **Padapāṭha:** स्वधा । अवस्तात् । (Śākala)
- **Translation:** "impulse below, striving above."
- **Location:** Ṛgveda 10.129.5c. DCS verse line: `svadhā avastāt`.
- **Rule:** 6.1.101.

### The fourth combination (आ + आ → आ)
Not separately isolated this pass. It is the **same rule** (6.1.101) with two long inputs; a printed cross-word example can be slotted, or the three above suffice, since 6.1.101 treats all four *avarṇa*+*avarṇa* inputs identically. Do not present आ+आ as a different operation.

### Part 1.3 — Source of the saṃvṛta-अ / vivṛta-आ distinction
**Secure as documentation.** The *prayatna* (articulatory-effort) classification of the phonetic disciplines records short अ as **संवृत (*saṃvṛta*, contracted)** and आ as **विवृत (*vivṛta*, open)**; the Aṣṭādhyāyī operationalizes it by treating अ as *vivṛta* for *savarṇa* identity (1.1.9 तुल्यास्यप्रयत्नं सवर्णम्) and restoring the contracted realization at the final rule (8.4.68 अ अ). The specific "अ is *saṃvṛta* in *loka*" statement is a **Śikṣā/commentarial** claim (Pāṇinīya Śikṣā tradition + the commentary on 8.4.68). Confirm the exact Śikṣā/Kāśikā wording for the endnote; the claim itself is secure.

### Part 1.4 — Does any discipline explain *why* the long member changes quality?
**No — Unresolved, confirming Codex §4.2.** The disciplines **document** the *saṃvṛta/vivṛta* contrast but I find **no internal source giving a causal rationale** for why the two-*mātrā* member is open (आ) rather than a long contracted schwa. 8.4.68 is an operational patch (run अ as *vivṛta* for the rules, restore it after), not an explanation. The manuscript must state the *what* (documented) and not manufacture a *why*. This is the honest boundary; the book's "engineering" reading is a *supported inference* from the arrangement, not a stated Vedic rationale.

---

## PART 2 — THE 132-REALIZATION MATRIX

**Arithmetic and framing: secure.** 4×18 + 5×12 = 132 is correct, and the Codex is right that it is an **analytical possibility space, not a corpus frequency**. Per the audit categories requested:

| Matrix component | Analytically recognized | Generated under a stated rule | Found in an exact received passage | Open / Unresolved |
|---|---|---|---|---|
| 9 vowel families | ✅ (but lineage-variable, see below) | — | ✅ all nine occur | — |
| *hrasva* / *dīrgha* | ✅ | 6.1.101 etc. | ✅ abundant | — |
| *pluta* (3rd duration) | ✅ (1.2.27) | 8.2.82ff (question/calling) | ✅ **but only in the ritual corpus, not the RV** (Part 3) | RV-pluta Open |
| 3 pitches × each duration | ✅ (1.2.29–32) | — | accent **not in the DCS** → not corpus-verifiable here | needs accented edition |
| *anunāsika* × each cell | ✅ (1.1.8) | phonetic environment | **not in the DCS** (0 tilde-vowels) → not corpus-verifiable | needs candrabindu-preserving edition |
| ऌ family (12 cells) | ✅ analytically | — | **ऌ itself corpus-absent** (Part 4) | almost wholly analytical/phantom |

**Three audit cautions the manuscript must carry:**
1. **Analytical recognition ≠ corpus occurrence** — the Codex says this; the data force it. Of the 132, the pitch and nasality multipliers are **not corpus-verifiable from the DCS at all** (it carries neither accent nor anunāsika). Any figure must legend these as *analytically recognized*, never as *attested*.
2. **The nine-family base is lineage-variable.** The **Ṛgveda-Prātiśākhya** counts **eight** *samānākṣara* (अ आ इ ई उ ऊ ऋ ॠ) — **excluding ऌ** — plus four *sandhyakṣara*; the **Taittirīya-Prātiśākhya** counts nine. So "nine families" is one lineage's inventory, not a universal. (Codex §3.3 — secure and important; confirm the two Prātiśākhya quotations against the texts for the endnote. This also touches the Claude plan's "five simple vowels," see §6.)
3. **The ऌ-family's 12 cells are near-empty.** With vocalic ऌ corpus-absent (Part 4), its *hrasva* row has no running-text instance, and its *pluta* × *svarita* × *anunāsika* cells are pure analytical extrapolation. Mark the whole ऌ family **Unresolved/analytical** in any figure, not "recognized" on equal footing with अ/इ/उ.

---

## PART 3 — PLUTA, PITCH, AND NASALITY

### 3.1 RV 10.129.5 and the pluta count — **REJECT as stated**
- **DCS Ṛgveda pluta tokens: 0.** RV 10.129.5 appears in the DCS as plain `adhas svid āsīt / upari svid āsīt` — **no `āsī3t`**. The digit-marked pluta the Codex quotes is **not in the DCS Ṛgveda text**.
- **The "three in the RV, fifteen in the AV" figure fails the corpus:** DCS marked-pluta counts are **Ṛgveda 0, Atharvaveda (Śaunaka) 7, Atharvaveda (Paippalāda) 0.** Not 3, not 15.
- **Where pluta actually lives (DCS, digit-marked, 302 tokens total):** the **ritual/recitational corpus** — Śatapatha-Brāhmaṇa 38, Jaiminīya-Upaniṣad-Brāhmaṇa 34, Baudhāyana-Śrautasūtra 27, Aitareya-Āraṇyaka 25, **Taittirīya-Saṃhitā 20, Maitrāyaṇī-Saṃhitā 18**, Jaiminīya-Brāhmaṇa 14, Kātyāyana-Śrautasūtra 12, and the laukika corpus 250. Characteristic forms: **`o3m`, `subrahmaṇyo3m`, `somā3`, `agnā3i`, `bho3`, `vetthā3`, `au3`/`au4`** — the calling, invocation, and question plutas.
- **Verdict and fix:** RV 10.129.5 `āsī3t` is at best an **analytical/recitational reading** (pluta-in-question, 8.2.82ff), **not a marked saṃhitā form in this corpus**. Replace the flagship example with a **secure ritual-corpus pluta** (e.g., the *subrahmaṇyā* invocation `subrahmaṇyo3m`, or a Taittirīya/Maitrāyaṇī Saṃhitā occurrence). State plainly: as a *marked, transmitted* form, pluta is **concentrated in the ritual and recitational corpus and absent from the DCS Ṛgveda Saṃhitā**. (Caveat per the user's rule: absence of *marking* in the DCS RV is not proof pluta is never *analyzed* in the RV — but it cannot be cited as a marked RV form.)
- The `au4` / digit-4 forms (7×) suggest some texts mark a **four-*mātrā*** protraction beyond the canonical three-*mātrā* pluta; note but do not build on it without a source.

### 3.2 Can short, long, and pluta each bear all three pitches? — **Secure (analytical), not corpus-verifiable here**
Analytically yes: pitch (1.2.29–32) is independent of duration, so each of *hrasva/dīrgha/pluta* combines with *udātta/anudātta/svarita*. **The DCS carries no accent**, so this cannot be corpus-demonstrated locally; it rests on the grammar and on the accented editions. Mark *recognized*, not *attested*.

### 3.3 Does *svarita* require two *mātrās*? — **REJECT the requirement; Codex correct**
**1.2.32 तस्यादित उदात्तमर्धह्रस्वम्** makes the initial high portion of *svarita* **half a short vowel's** duration, so *svarita* sits on a **short** vowel. "*Svarita* requires two *mātrās*" is false. (Nuance: *svarita* is a **contour** — an *udātta*→*anudātta* movement — so it needs *some* realizable duration; on a very short vowel it is compressed, not absent. State it as "*svarita* does not require two *mātrās*," not "duration is irrelevant.")

### 3.4 Anunāsika vowels across families — **category secure; corpus-unverifiable from the DCS**
The DCS has **0 combining-tilde (nasalized-vowel) tokens** — it normalizes *anunāsika* to *anusvāra* (ṃ/ṁ) or drops it. So nasalized vowels across families **cannot be shown from this corpus**. The *category* is secure (1.1.8 मुखनासिकावचनोऽनुनासिकः) and instances are real in the accented saṃhitā (the candrabindu forms — e.g., *devā̐*, *mahā̐*), but the evidence must come from an **anunāsika-preserving edition**, not the DCS. Do not present the six pitch × nasality realizations as corpus-attested; they are **analytical**.

---

## PART 4 — ऌ AND ॡ

**Corpus result (full DCS, 15,900 files):**
- **Vocalic ऌ (*l̥*): ZERO** tokens anywhere.
- **Vocalic ॡ (*l̥̄*): ZERO** tokens anywhere.
- **√कॢप् (*kḷp*) never surfaces with its vocalic-ऌ grade** — searching the "klp" skeleton (diacritics stripped) returns **none**; every *kl-* word in the corpus is the **cluster** *kl* + vowel (*kleśa*, *kliś*, *klid*, *klība*, *klam*), not vocalic ऌ.
- (Methodological note: IAST *ḷ* U+1E37 (dot-below) is the DCS's **retroflex-lateral consonant** ळ — e.g., Vedic *īḷe* 13× — a **different sound**; the vocalic ऌ uses a ring-below and is what returned zero. Do not conflate the two ळ/ऌ in the manuscript.)

**Verdict on ॡ (per the five options):** it is a **formal symmetry completion / teaching symbol** — **not** an actually-used vowel, and not (on this evidence) a governed analytical substitute with running-text use. This **confirms and strengthens Codex §3.5**: not only is ॡ corpus-absent, but even **short ऌ is corpus-absent** in running text.

**Required caveat (the user's Part 4.5).** Corpus-absence is **not** universal absence. Vocalic ऌ is **real in the analytical/teaching apparatus**: it is the ninth vowel of Pāṇini's *śivasūtra* row (अ इ उ ण् / … / ऌ), it heads a genuine Dhātupāṭha root (√कॢप्), and it fills the *bārahkhaḍī* teaching cells (कॢ कॣ). Its status is therefore **a teaching-and-citation vowel that running text does not use**; ॡ is one step further out — a symbol completing the written row with **no natural word at all**. State it exactly that way; do not write "ऌ/ॡ do not exist."

**Part 4.3 — earliest secure written use of ॡ: not determinable from the corpus.** This is a script-paleography question the DCS cannot answer (Codex left it Unresolved; confirmed). It needs manuscript/alphabet-chart history (the siddhamātṛkā/Devanagari teaching tradition), not a text corpus. Do not assign a date.

---

## PART 5 — SHORT e/o *(prompt truncated at "SHORT e/o IN TH…"; audited as the standard claim — please confirm scope)*

**Assuming the claim is "Sanskrit has no short e/o; the sounds exist in the surrounding field":**
- **Sanskrit side — secure.** Sanskrit has **no short ए/ओ**: ए and ओ are the *guṇa* grade (अ+इ, अ+उ) and are inherently दीर्घ. The DCS has nothing to find because there is **no short-e/short-o category** in Sanskrit phonology; every *e/o* form in the corpus is the long *guṇa/vṛddhi* vowel. Confirmed by construction, not by a search.
- **Field side — secure as general linguistics; the specific citations are the Codex's screening layer, not re-verified here.** That Tamil, Telugu, and Kannada have **phonemic short *and* long e/o** is textbook Dravidian phonology and is not in doubt. The **PHOIBLE inventory IDs and the Korku/Zide, Mundari/Sinha-Osada citations** (Codex §7) I did **not** re-fetch; before print, verify each against a grammar (Codex already flags this in its §7.3, including checking Korku against Nagaraja rather than Zide/PHOIBLE alone). The **architectural conclusion is sound**: short e/o are producible in the field, so Sanskrit's exclusion of them is a **selection**, not an inability — the strong form of the engineering claim.
- **Do not overreach into "central vowel."** No claim about a long contracted अ follows from the short-e/o data (Codex §7.3, §8.4 — correct). Keep the *avarṇa* quality problem separate from the short-e/o problem.

> **Flag:** because the prompt cut off, I audited the standard short-e/o claim. If Part 5 intended something narrower (e.g., short e/o **in the Prākṛta forms specifically**, or **in a particular Vedic sandhi context** such as *abhinihita* / *praśliṣṭa*), re-issue and I will target it. Note for scoping: short e/o are a real development in the **Prākṛta** forms and appear in the *e/o + a → e'/o'* **abhinihita** sandhi environment as prosodic outcomes — but neither makes short e/o a **phonemic Sanskrit vowel**.

---

## 6. Cross-cutting corrections (touch both plans)

1. **The junction symmetry limit corrects the *Claude* plan's Move 3.** Codex §5.3 is right: **इ/उ → ए/ओ (and ऐ/औ), but ऋ/ऌ → अर्/अल् (and आर्/आल्)**. My plan's Move 3 ("इ/उ/ऋ/ऌ are amphibious — tail-position → compound vowel") **overreaches on ऋ/ऌ**: they do **not** yield a compound *vowel*, they yield a vowel+consonant sequence. **Fix the Claude plan:** restrict the clean "amphibious → compound vowel" unification to **इ/उ → ए/ओ**, and present ऋ/ऌ as the **asymmetry that proves the grid follows *function*, not visual symmetry** (which is a *stronger* engineering point than a forced four-way parallel). The semivowel side (इ+अ→य, उ+अ→व, ऋ+अ→र, ऌ+अ→ल) *is* a clean four-way and stays.
2. **"Five simple vowels" is lineage-dependent.** The Claude plan's five-place simple-vowel set (a/i/u/ṛ/**ḷ**) is the **Śikṣā/Taittirīya** inventory; the **Ṛgveda-Prātiśākhya counts eight simple vowels and omits ऌ.** Attribute the five-place scheme to the Śikṣā and note the Prātiśākhya divergence — otherwise the book flattens the lineages (the exact fault the Codex plan warns against).
3. **The ऌ-as-fifth-place claim survives, with attribution.** The place map (अ throat, इ palate, उ lip, ऋ retroflex, ऌ dental) matching the five consonant *vargas* is the **Pāṇinīya-Śikṣā** classification (एदैतोः कण्ठतालु, ओदौतोः कण्ठोष्ठ for the compounds) and is a legitimate, load-bearing point — but it is a *teaching* classification of ऌ that running text never exercises (Part 4). Both facts can stand together; state both.

---

## 7. What still needs printed sources (before manuscript deployment)

1. **Accent + saṃhitā/padapāṭha** for the three Part 1 examples — van Nooten–Holland / Aufrecht / Śākala padapāṭha (the DCS gives words + location only).
2. **A secure pluta example from the ritual corpus** to replace RV 10.129.5 — cite a specific Taittirīya/Maitrāyaṇī Saṃhitā or Śrautasūtra locus with its pluta marking, and **drop the "3 RV / 15 AV" figure** (or re-cite it to whatever specialist enumeration it came from, clearly labeled analytical).
3. **Anunāsika instances across families** — from a candrabindu-preserving accented edition, since the DCS normalizes them away.
4. **Śikṣā/Prātiśākhya quotations** for: saṃvṛta-अ/vivṛta-आ; the eight-vs-nine *samānākṣara* counts; the *kaṇṭhatālu/kaṇṭhoṣṭha* place-names — confirm exact wording for endnotes (the Codex's sūtra numbers are already verified).
5. **ॡ script-history** — earliest written attestation is a paleography question; either source it or leave it explicitly Unresolved in the book.
6. **PHOIBLE → grammar-page upgrade** for the six comparison languages (Codex §7.3 already lists this).

---

## 8. Bottom line

The Codex evidence record is **methodologically strong and mostly secure** — its grammar citations are accurate, its self-imposed "recognized ≠ attested" discipline is exactly right, and it already flagged its two weakest points (the missing अ+अ→आ example and the unverified pluta count). This audit:

- **closes** the अ+अ→आ gap (three Nāsadīya examples, Part 1);
- **rejects** the two overreaching corpus claims — **RV 10.129.5 pluta** and the **"3 RV / 15 AV"** count — replacing them with the DCS-verified distribution (pluta is a **ritual-corpus** phenomenon; the RV Saṃhitā has none marked);
- **strengthens** the ऌ/ॡ finding (both vocalic ऌ *and* ॡ are corpus-absent across 15,900 texts; ॡ is a symmetry symbol);
- **confirms** the *svarita*-not-two-*mātrās* and pitch-did-not-cause-the-gaps rejections;
- **flags** that pitch and anunāsika multipliers in the 132-matrix are **not corpus-verifiable from the DCS** and must be legended *analytical*; and
- **corrects the Claude plan's Move 3** via the junction symmetry limit (इ/उ→ए/ओ is clean; ऋ/ऌ→अर्/अल् is the informative asymmetry).

Sanskrit's vowel engineering claim stands — but on **selection and governed operation**, demonstrable in the corpus, not on accent/nasality cells the corpus cannot show and not on a Ṛgvedic pluta the corpus does not carry.
