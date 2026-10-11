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

## Gold Greed vs Fear – XAUUSD (`gold-greed-fear.pine`)

TradingView indikátor (Pine Script v6) pre **XAUUSD**. Zložený oscilátor 0–100, ktorý v samostatnom paneli ukazuje, či je zlato v režime strachu alebo chamtivosti. Nižšie = strach, vyššie = chamtivosť.

### Inštalácia
1. Otvor graf **XAUUSD** (odporúčané H1 – D1) a dole klikni na **Pine Editor**.
2. Zmaž obsah editora a vlož celý súbor `gold-greed-fear.pine`.
3. Klikni na **Uložiť** a potom na **Pridať do grafu** (panel sa otvorí pod cenou).

### Zóny skóre
| Rozsah | Zóna | Farba |
|---|---|---|
| 0 – 25 | EXTRÉMNY STRACH | červená |
| 25 – 45 | OPATRNOSŤ | oranžová |
| 45 – 55 | NEUTRÁL | sivá |
| 55 – 75 | CHAMTIVOSŤ | limetková |
| 75 – 100 | EXTRÉMNA CHAMTIVOSŤ | zelená |

### Z čoho sa skóre skladá (váhy sú nastaviteľné)
| Komponent | Váha | Ako sa číta |
|---|---|---|
| RSI | 30 | priamo ako skóre 0–100 |
| Vzdialenosť od rýchlej SMA | 15 | % od priemeru, normalizované z-skóre (alebo pevné %) |
| Vzdialenosť od pomalej SMA | 15 | to isté pre dlhodobý priemer |
| ATR režim | 15 | vysoká volatilita v poklese = strach, v raste = tlmená chamtivosť, kľud = drift v smere trendu |
| DXY (voliteľné) | 10 | inverzne k zlatu, váha sa škáluje podľa živej zápornej korelácie |
| US10Y (voliteľné) | 10 | inverzne k zlatu, rovnako škálovaná váha |
| Sentiment (voliteľné) | 15 | ručne vložené % longov davu, alebo úplný override skóre |

Komponenty s hodnotou `na` (napr. vypnuté makro) sa z váženého priemeru vypustia, takže skóre je vždy 0–100. Výsledok sa vyhladzuje EMA (štandardne 3, hodnota 1 = vypnuté).

### Na grafe
- Hlavná krivka skóre vo farbe zóny, vyplnené pásma zón a podfarbenie pozadia v extrémoch.
- Trojuholníky pri prekrížení 25 a 75 (vstup/výstup z extrémnej zóny).
- Tabuľka komponentov: hodnota a čiastkové skóre každého komponentu, celkové skóre a názov zóny.
- Čiastkové skóre sú dostupné aj v Data Window.

### Alerty
Prekríženie pod 25 / nad 75, stav pod 25 / nad 75 a opustenie extrémnej zóny. Pri potvrdenej sviečke sa odošle aj `alert()` s tickerom, timeframom a skóre.

### Nastavenia
Dĺžky RSI, SMA, ATR a smerovej EMA; normalizácia (z-skóre s lookbackom a capom, alebo pevné %); makro symboly DXY a US10Y s korelačným škálovaním; sentiment (blend / override); váhy; vyhladenie, pozadie, tvary, tabuľka a jej pozícia.
