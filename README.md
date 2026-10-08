# Indikators

## SARUJA 21596244 – Trade Map (`saruja-21596244-trade-map.pine`)

TradingView indikátor (Pine Script v6) pre **XAUUSD**. Zobrazí všetkých **31 reálnych uzavretých obchodov** účtu SARUJA (MT4 Pro USD, 01.09.2026 – 08.10.2026, vklad 10 000 USD, +11 643 USD) priamo na grafe zlata: **vstup, exit, trvanie, ponor (MAE), najlepší bod (MFE), koše (priemerovanie) a štatistiky účtu**.

Ponory nie sú v exporte – indikátor ich **dopočíta zo sviečok grafu** (high/low medzi otvorením a zatvorením). Preto je najlepší na **M1 – M15**; na vyšších TF je ponor hrubší.

### Inštalácia
1. Otvor graf **XAUUSD** (M5 ideál) a dole klikni na **Pine Editor**.
2. Zmaž obsah editora a vlož celý súbor `saruja-21596244-trade-map.pine`. **Uložiť** → **Pridať do grafu**.
3. Voliteľne pridaj aj `saruja-21596244-equity.pine` – otvorí sa v samostatnom okne pod grafom (equity, plávajúci P/L, DD %, počet otvorených pozícií).

### Čas exportu (dôležité)
Časy v histórii sú „ako na stránke“, bez pásma. Indikátor si **sám skalibruje UTC posun**: vyskúša UTC-12 … UTC+14 a vyberie posun, pri ktorom najviac cien entry/exit padne do rozpätia sviečky. Výsledok a kvalitu zhody vidíš v tabuľke Prehľad v riadku **Kalibrácia času** (zelená ≥ 80 % zhoda). Ak je zhoda slabá (napr. na H1), prepni na **Ručne** a zadaj posun servera (MT4 v lete typicky UTC+3). Rovnaký posun zadaj do equity skriptu.

### Čo je na grafe pri každom obchode
| Prvok | Význam |
|---|---|
| Biela čiara | entry (cena otvorenia) po celé trvanie obchodu |
| Zelená / červená zóna | entry → exit: výška = zisk alebo strata v $/oz, šírka = trvanie |
| Farebná zóna nad entry | **max ponor (MAE)** – koľko $/oz išiel obchod proti, farba podľa triedy |
| ▼ marker | sviečka, kde bol ponor najhlbší |
| ▲ marker | najlepší bod (MFE) – koľko bolo k dispozícii; v štítku „využité X %“ |
| Bodkovaná diagonála + ◆ | dráha entry → exit a bod zatvorenia |
| Štítok ▼ nad zónou | hĺbka ponoru v $/oz a USD na účte (od prahu, štandardne 10 $) |
| Hlavný štítok | číslo, lot, entry → exit, zisk USD, ponor ($/oz · USD · % účtu · trieda), trvanie, MFE, zisk/ponor |
| KÔŠ | pozície zatvorené naraz: počet, loty, vážený Ø entry (prerušovaná čiara), net, **spoločný ponor** koša |
| Tooltip (myš na štítku) | ticket, presné časy, zostatok pred/po, všetky metriky |

**Jednotky:** `$` = pohyb ceny v USD za uncu, `USD` = peniaze na účte (ponor × lot × 100 oz).

### Farby podľa ponoru (prahy sa dajú meniť)
`ČISTÝ ≤ 5 $` zelená · `MIERNY ≤ 15 $` limetková · `VÝRAZNÝ ≤ 30 $` oranžová · `HLBOKÝ ≤ 100 $` červená · `EXTRÉM > 100 $` fialová · `MIMO DÁT` sivá (graf nesiaha do obdobia obchodu – prepni na M5 / M15 alebo načítaj viac histórie). Obchod, ktorý graf pokrýva len čiastočne (história začína po otvorení alebo končí pred zatvorením, napr. pri Bar Replay), dostane ponor z dostupných sviečok a označenie **⚠ čiastočné**.

### Tabuľky
- **Prehľad účtu**: obchody, WR, čistý zisk a % vkladu, profit factor, Ø zisk / Ø strata, ponor (Ø, medián, max – v $/oz aj USD a % účtu), trvanie, zisk/ponor, využitie MFE, closed DD, najhorší plávajúci P/L, **equity DD** (zostatok + plávajúci P/L podľa sviečok), max súčasne otvorené pozície, koše, kalibrácia času a riadok **⚠ PROFIL** (jednosmernosť, priemerovanie, pomer strát a ziskov, držanie strát).
- **Rozdelenie ponoru**: počet a % v každej triede, histogram, Ø trvanie a Ø USD triedy.
- **Týždenný prehľad**: obchody, ziskové, net USD, loty, Ø / max ponor, Ø trvanie.
- **TOP N najhlbších ponorov** a voliteľný **zoznam všetkých obchodov**.

### Nastavenia
Časové pásmo (auto / ručne), pásmo zobrazenia, filter dátumu a výsledku (všetky / ziskové / stratové / koše), minimálny ponor, zvýraznenie hlbokých ponorov, všetky prvky kreslenia, krivka plávajúceho P/L účtu (pás pod cenou, štandardne vypnutá), režim štítkov (Plné / Kompaktné / Iba číslo / Skryť), prahy a farby, pozície a veľkosť tabuliek.

### Dáta a regenerácia
`saruja-21596244-historia.xlsx` (export účtu) → `python3 tools/build_saruja.py saruja-21596244-historia.xlsx .` vyrobí `saruja-21596244-trades.csv` (tabuľka obchodov), `saruja-21596244-data.pine` (Pine polia – prekopíruj do sekcie DÁTA oboch skriptov) a `saruja-21596244-data.json` (štatistiky). Skript overí počet obchodov a súčet zisku voči hárku Súhrn a každý zisk voči (entry − exit) × lot × 100. Vklady a výbery (riadky BALANCE) idú do polí `BOT` / `BOA`, takže zostatok pred/po obchode, equity a DD ich zohľadňujú chronologicky; closed DD sa počíta iba z obchodného P/L.

---

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
