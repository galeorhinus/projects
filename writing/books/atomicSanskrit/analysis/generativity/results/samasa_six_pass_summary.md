# Six-Pass Bounded समासः (*samāsaḥ*) Expansion

This block counts directly reconstructible compounds in the pinned Kāśikā regression sources. It does not treat compounding as a finite universal multiplier.

| Pass | Result |
|---:|---|
| 1 | Inventory all 8 compound types exposed by pinned Vidyut 0.4.0. |
| 2 | Extract 167 assertions: 132 active and 35 ignored. |
| 3 | Admit 113 unique, directly reconstructible source relations at depth one; collapse 7 repeated assertions. |
| 4 | Confirm all 113 relations as literal active assertions in the pinned engine suite and locally regenerate 113 of them. |
| 5 | Add 113 compound word-meanings without collapsing different meanings by spelling. |
| 6 | Raise the combined bounded subtotal to **12,845,500 word-meanings**. |

## Examples

| Members | Result | Relation |
|---|---|---|
| राजन् (*rājan*) + पुरुष (*puruṣa*) | राजपुरुष (*rājapuruṣa*) | the king's man |
| महत् (*mahat*) + पुरुष (*puruṣa*) | महापुरुष (*mahāpuruṣa*) | a great person |
| प्लक्ष (*plakṣa*) + न्यग्रोध (*nyagrodha*) | प्लक्षन्यग्रोध (*plakṣanyagrodha*) | plakṣa and banyan together |
| वाच् (*vāc*) + त्वच् (*tvac*) | वाक्त्वच (*vāktvaca*) | speech and skin taken as a collection |
| ग्राम (*grāma*) + गत (*gata*) | ग्रामगत (*grāmagata*) | gone to the village |

## Boundary

A source example proves one compound relation; it does not license every pair of nominal meanings. Recursive compounds, unrestricted pairwise combination, source examples with constructed members, and broad semantic generalization remain outside this subtotal. The Rust compound API is not exposed in Vidyut 0.4.0's Python binding. The included pinned Rust verifier regenerated the admitted examples locally and retained their rule paths.
