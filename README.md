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

## Gold Greed vs Fear PRO – XAUUSD (`gold-greed-fear.pine`)

TradingView indikátor (Pine Script v6) pre **XAUUSD**. Zložený oscilátor 0–100 (strach ↔ chamtivosť) rozšírený o panel prepojených trhov s mini grafmi, 30-dňovú štatistiku volatility a projekciu range pre Asia / London / New York seansu. Logika faktorov je rozpísaná v `gold-factors-analyza.md`.

### Inštalácia
1. Otvor graf **XAUUSD** (odporúčané M15 – H1 pre seansy, D1 pre makro pohľad) a dole klikni na **Pine Editor**.
2. Zmaž obsah editora a vlož celý súbor `gold-greed-fear.pine`.
3. Klikni na **Uložiť** a potom na **Pridať do grafu**. Oscilátor sa otvorí v paneli pod cenou, projekcie seáns sa kreslia priamo na cenový graf.

### Zóny skóre
| Rozsah | Zóna | Farba |
|---|---|---|
| 0 – 25 | EXTRÉMNY STRACH | červená |
| 25 – 45 | OPATRNOSŤ | oranžová |
| 45 – 55 | NEUTRÁL | sivá |
| 55 – 75 | CHAMTIVOSŤ | limetková |
| 75 – 100 | EXTRÉMNA CHAMTIVOSŤ | zelená |

### Komponenty skóre
| Komponent | Váha | Ako sa číta |
|---|---|---|
| RSI | 30 | priamo ako skóre 0–100 |
| Vzdialenosť od rýchlej / pomalej SMA | 15 + 15 | % od priemeru, z-skóre (alebo pevné %) |
| ATR režim | 15 | vysoká vol v poklese = strach, v raste = tlmená chamtivosť, kľud = drift v smere trendu |
| Sentiment (voliteľné) | 15 | ručne vložené % longov davu, alebo override skóre |
| 8 faktorových slotov | 5 – 10 | DXY ↓, US10Y ↓, US02Y ↓, EURUSD ↑, USDJPY ↓, XAGUSD ↑, SPX ~, VIX ↑ (SPX a VIX štandardne vypnuté) |

Každý faktor má: zapnutie, symbol, znamienko (`Inverse` / `Direct` / `Auto (by corr)`), váhu a jednotku zobrazenia (`%`, `pips 0.0001`, `pips 0.01`, `bp`, `pts`). Váha sa škáluje živou koreláciou so zlatom – faktor, ktorý ide proti očakávanému vzťahu, na skóre nevplýva. Komponenty s `na` sa z priemeru vypustia, skóre je vždy 0–100 a vyhladzuje sa EMA.

### Tabuľka 1 – komponenty + faktory
Pre každý faktor: **mini graf** (sparkline z posledných N barov), **Δ za N barov** v natívnych jednotkách (pipy / bp / body) aj v %, **Dnes** (zmena od denného open), **r** (korelácia so zlatom) a efektívna váha, čiastkové skóre vo farbe zóny. Riadok SKÓRE má vlastný sparkline a zmenu oproti predchádzajúcemu baru.

### Tabuľka 2 – volatilita 30 D + seansy
- **ADR** priemer / medián / σ / max z uzavretých dní (bez repaintu), realizovaná volatilita (denná a anualizovaná), 1σ denný pohyb v $.
- **Dnešný range** v $ a v % ADR, **vol scale** = ATR(14) / ATR(30) denné (0.5–2.0×), očakávaný denný range a high/low od close.
- **Seansy** Asia / London / New York: posledných 30 seáns → Ø, medián, p90, max range, Ø a max odchýlka nahor (high − open) a nadol (open − low).
- **Aktuálna seansa**: range zatiaľ, % z očakávaného range, open. Riadok sčervenie pri prekročení p90.
- **Ďalšia seansa**: očakávaný range (vol-adjusted) ± σ, očakávaný high / low od aktuálnej ceny, **maximálna odchýlka** z okna a pásmo range.

### Projekcia na cenovom grafe
Pri otvorení každej seansy sa vykreslia čiary na dĺžku seansy: open (čiarkovaná), očakávaný high / low (plné), max high / low (bodkované) + štítok s hodnotami. Farby: Asia fialová, London tyrkysová, New York oranžová. Uchovávajú sa posledné N seansy.

### Alerty
Prekríženie pod 25 / nad 75, stav pod 25 / nad 75, opustenie extrémnej zóny, **range seansy > očakávaný** a **range seansy > p90**. Pri potvrdenej sviečke sa odošle aj `alert()` s tickerom, timeframom a skóre.

### Nastavenia
1) Core dĺžky · 2) normalizácia · 3) faktory (lookback, korelácia, dĺžka mini grafu, 8 slotov) · 4) sentiment · 5) core váhy · 6) volatilita a seansy (okno, vol scale, časy a časové zóny seáns, kreslenie projekcie) · 7) vizuály (vyhladenie, pozadie, tvary, obe tabuľky a ich pozícia, veľkosť textu).

Poznámka: seansy a projekcia fungujú len na intraday grafe; denná štatistika funguje všade. Reálny výnos `FRED:DFII10` má len denné dáta – použi ho v slote len na D1 grafe.
