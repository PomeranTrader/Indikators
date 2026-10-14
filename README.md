# Indikators

## Infinity Pullback Return – Buy the Dip (`infinity-pullback-return.pine`)

TradingView indikátor (Pine Script v6, overlay) pre **XAUUSD**. Po každej robustnej sviečke na impulznom timeframe (štandardne H4, voliteľne H1) meria, **kedy a s akou pravdepodobnosťou sa cena vráti na jej open** (zavretie gapu = pullback / buy the dip), koľko ešte pred návratom ubehne a ako hlboko pod open po návrate ide. Všetky čísla sú percentily zo skutočnej histórie grafu.

Spája všetko, čo sme doteraz robili:
- **MMA stack** (Focus Touch MA, Daily Tester MA, First / Second / Third Trend Tester, Last Barricade) + marker dotyku ✓/✗. Vzdialenosť ceny od každej línie pri impulze a počet línií vnútri gapu (bariéry) vstupujú do podmienenej štatistiky návratu.
- **Potvrdenie pullbacku** = otočka na Focus Touch MA (close pod líniu, voliteľne aj sklon).
- **Greed & Fear index 0–100** (RSI, natiahnutie od Daily Tester / First Trend Tester, momentum, séria bez dotyku Focus Touch MA, šírka býčích sviečok) s piatimi režimami; režim sa ukladá ku každému impulzu.
- **MS MODEL**: generuje vlastné BUY (SELL) signály = dotyk open impulzu + otočka + trend a G&F filter, hneď ich spätne testuje (TP v USD, max ponor, čas do TP) a porovnáva s reálnou štatistikou **GFX MS 2026** (158 signálov, dáta z Trade Mapy). Pri signáli kreslí očakávaný ponor GFX P50 / P75 / P90.
- **GFX overlap**: koľko reálnych GFX entry bolo postnutých na úrovni open aktívneho impulzu a v akom G&F režime.

### Inštalácia
1. Graf **XAUUSD M15 alebo H1** → Pine Editor → vlož celý súbor `infinity-pullback-return.pine` → Uložiť → Pridať do grafu.
2. Impulzný timeframe (vstup ①) musí byť rovnaký alebo vyšší ako graf. Odporúčané kombinácie: M15 + 240, H1 + 240, M15 + 60.
3. Čím viac histórie má graf, tým robustnejšie percentily. Bunky s menej ako N vzorkami (vstup ⑦) sú sivé.

### Čo je na grafe
| Prvok | Význam |
|---|---|
| Vodorovná čiara od close impulzu | úroveň **open** impulznej sviečky (cieľ návratu). Tyrkysová = čaká, zelená = návrat ✓, sivá prerušovaná = bez návratu do horizontu |
| Štítok pri čiare | TF a smer, open, gap v USD a ATR, beží/čas, bariéry v gape, otočka FTMA, G&F pri impulze; po návrate aj rozbeh a hĺbka pod open |
| `↩ FTMA` | otočka Focus Touch MA = potvrdenie pullbacku |
| ▲ modrý trojuholník + štítok `MS ▲ BUY` | signál MS modelu, živý stav TP ✓ / beží / TIMEOUT, ponor |
| Bodkované čiary pod signálom | očakávaný ponor GFX P50 (limetková) / P75 (oranžová) / P90 (červená) |
| ◆ fialový | reálny GFX MS signál |

### Tabuľky
- **Hlavná štatistika**: počty impulzov, návrat %, percentily času návratu P25/P50/P75/P90, pravdepodobnosť návratu do 1 sviečky / 4 h / 12 h / 24 h / 48 h / týždeň, rozbeh pred návratom, hĺbka pod open po návrate (možný návrat), štatistika otočky Focus Touch MA, Greed & Fear teraz, **MODEL vs GFX** (TP %, ponor P50/P75/P90, čas do TP, zisk/ponor), GFX entry na open impulzu, GFX signály podľa G&F režimu.
- **Vplyv MA / bariér / G&F / session**: pre každú zo šiestich línií návrat % a medián času podľa vzdialenosti pri impulze (za líniou, 0–1, 1–2, 2–3, > 3 ATR); to isté podľa počtu bariér v gape, G&F režimu a session uzavretia impulzu.
- **Aktívne impulzy (živé)**: open, vzdialenosť, ako dlho beží, **P(návrat) podmienená prežitím** (koľko historických impulzov v rovnakej fáze sa ešte vrátilo), ETA P50/P75/P90, stav otočky, bariéry, G&F a historická miera návratu pre rovnaké bariéry · G&F · kôš Daily Tester.

### Alerty
Nový robustný impulz · Otočka Focus Touch MA · Návrat k open impulzu · Signál MS modelu.

Popis pre publikáciu: `infinity-pullback-return-popis.md`.

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
