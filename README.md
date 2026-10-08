# Indikators

## GFX MS 2026 – Trade Map (`gfx-ms-2026-trade-map.pine`)

TradingView indikátor (Pine Script v6) pre **XAUUSD**. Zobrazí všetkých 158 manuálnych signálov GFX Premier Club (29.12.2025 – 08.10.2026) priamo na grafe zlata: ponor, trvanie, zisk a štatistiky.

### Inštalácia
1. Otvor graf **XAUUSD** (najlepšie M5 – H1) a dole klikni na **Pine Editor**.
2. Zmaž obsah editora a vlož celý súbor `gfx-ms-2026-trade-map.pine`.
3. Klikni na **Uložiť** a potom na **Pridať do grafu**.

### Čo je na grafe pri každom obchode
| Prvok | Význam |
|---|---|
| Tyrkysová zóna | entry → TP. Výška je zisk, šírka je čas od postu po TP hit. |
| Farebná zóna pod entry | **max ponor** (MAE). Výška ukazuje, koľko USD išiel obchod proti. |
| Biela čiara | entry |
| Bodkovaná diagonála + ◆ | dráha od entry k bodu, kde padol TP |
| Štítok ▼ pod zónou | hĺbka ponoru (len pri ponore ≥ prah, štandardne 15 $) |
| Hlavný štítok | číslo, stav, entry/TP, zisk, ponor + trieda, trvanie, pomer zisk/ponor |
| Tooltip (myš na štítku) | celý detail vrátane prepočtu na USD pri zvolenom lote |

### Farby podľa ponoru (prahy sa dajú meniť)
`ČISTÝ ≤ 5 $` zelená · `MIERNY ≤ 15 $` limetková · `VÝRAZNÝ ≤ 30 $` oranžová · `HLBOKÝ ≤ 100 $` červená · `EXTRÉM > 100 $` fialová
`OTVORENÝ` modrá: ponor, P/L a trvanie sa živo dopočítavajú z grafu, a ak graf ukáže TP hit, obchod sa prepne na „TP ✓ (graf)“.
`BEZ METRÍK` sivomodrá prerušovaná čiara: TP hit len podľa postu alebo nevyhodnotený signál, entry nie je známe.

### Tabuľky
- **Prehľad**: počty, TP %, priemerný, mediánový a maximálny ponor, trvanie, Ø zisk / Ø ponor, ponor prepočítaný na lot.
- **Rozdelenie ponoru**: počet a % v každej triede, textový histogram a priemerné trvanie triedy.
- **Mesačný prehľad**: signály, TP, Ø a max ponor, Ø trvanie a počet hlbokých ponorov za mesiac.
- **TOP N najhlbších ponorov**: vrátane otvorených obchodov.

### Nastavenia
Filter dátumu, typy signálov, minimálny ponor, režim „zvýrazniť iba hlboké“, režim štítkov (Plné / Kompaktné / Iba číslo / Skryť), veľkosti, pipy, lot pre prepočet, časová zóna, všetky farby a pozície tabuliek.

Dáta pochádzajú z `gfx.db setup_metrics` (MAE strict fill), otvorené signály podľa stavu 2026-10-07. Symbol ✎ znamená, že čas postu bol upravený.
