# Indikators

## Candle Size Scanner (`candle-size-scanner.pine`)

TradingView indikátor (Pine Script v6), ktorý vyhľadá sviečky podľa **zadaných veľkostí** (štandardne pásma od 20 / 30 / 50 / 100 / 150 / 200 USD), farebne ich označí a spočíta v tabuľke. Funguje na **aktuálnom timeframe** aj na **vyšších timeframoch** naraz (napr. na M5 grafe vidíš aj veľké sviečky M15, H1, H4 a D1).

### Inštalácia
1. Otvor graf (napr. **XAUUSD** M5 – H1) a dole klikni na **Pine Editor**.
2. Zmaž obsah editora a vlož celý súbor `candle-size-scanner.pine`.
3. Klikni na **Uložiť** a potom na **Pridať do grafu**.

### Čo je na grafe
| Prvok | Význam |
|---|---|
| Zafarbená sviečka | sviečka aktuálneho timeframu spadla do zapnutého pásma (veľké pásma, **bez obmedzenia spätne**) |
| Rámček okolo sviečky | **malé pásmo** (prah pod 50): zobrazí sa iba **posledných 10** výskytov na pásmo |
| Štítok ▲ / ▼ + číslo | smer a veľkosť sviečky (USD, pipy alebo %) – tooltip má dátum, pásmo a detail |
| Prerušovaný rámček s textom `H1 ▲ 62.4` | sviečka **vyššieho timeframu** v pásme, roztiahnutá cez celý jej čas na aktuálnom grafe |

### Pásma veľkostí
- Každé pásmo je interval **od svojho prahu po nasledujúci vyšší prah**, posledné pásmo je bez hornej hranice. Prahy sa zadávajú vzostupne, ale indikátor si ich zoradí sám.
- **Vypnuté pásmo = sviečky tej veľkosti sa nezobrazia** (nepadnú do nižšieho pásma). Pásmo vypneš zaškrtávacím políčkom v Nastaveniach → *② Veľkosti sviečok*; tabuľka ukazuje stav `✔ ZAP` / `✖ VYP`. Pine tabuľky nie sú klikateľné, preto sa prepína v nastaveniach.
- **Malé pásma** (prah pod hodnotou *Malé pásmo = prah pod*, štandardne 50) ukazujú iba posledných N výskytov (štandardne 10) – na každé pásmo a každý timeframe zvlášť. Voliteľne sa dajú aj malé sviečky farbiť po celej histórii.
- Meranie: **rozsah** (high − low) alebo **telo** (|close − open|). Jednotka: **USD**, **pipy** (1 USD = 10 pip) alebo **%**. Filter smeru: obe / iba rastúce / iba klesajúce.

### Tabuľka
Riadok pre každé pásmo: stav, rozsah pásma, počet sviečok na grafovom timeframe a na každom vyššom timeframe (tooltip = posledný výskyt), dátum a veľkosť poslednej sviečky. Päta ukazuje celkový počet zo všetkých načítaných sviečok. Vyšší timeframe, ktorý nie je vyšší ako timeframe grafu, je označený `✖` a preskočený.

### Štatistika „kedy vznikajú“ – kontext kĺzavých priemerov
Druhá tabuľka (štandardne vľavo hore) rozdelí sviečky každého pásma podľa stavu troch kĺzavých priemerov (rýchla / stredná / pomalá, štandardne EMA 20 / 50 / 200, typ a dĺžky sa dajú meniť). Každá bunka je `počet (% z pásma)`, stĺpec *Spolu* zhrnie zapnuté pásma:
- **Usporiadanie MA**: bullish (F > M > S), bearish (F < M < S), zmiešané.
- **Close vs MA**: nad všetkými, pod všetkými, medzi.
- **Smer sviečky vs trend MA**: s trendom, proti trendu, bez trendu.
- **Telo sviečky preťalo MA**: rýchlu, strednú, pomalú (MA leží medzi open a close).
- **Čerstvý kríž** rýchlej a strednej MA do N sviečok (štandardne 10).
- **Sklon rýchlej MA**: stúpa / klesá oproti hodnote pred N sviečkami.
- **Vzdialenosť close od pomalej MA**: priemer so znamienkom a absolútny priemer (natiahnutie) v zvolenej jednotke.
- **Session** podľa času Europe/Prague: Ázia 00–09, Londýn 09–15, Londýn + NY 15–18, New York 18–24.

Tooltip štítku každej sviečky ukazuje jej konkrétny MA kontext. Štatistika sa počíta iba pre sviečky aktuálneho timeframu; percentá sú z počtu sviečok, pri ktorých už boli MA vypočítané (prvých ~200 sviečok histórie sa pri EMA 200 nepočíta). MA sa dajú kresliť na graf alebo skryť.

### Upozornenia
Po zatvorení sviečky v zapnutom pásme (na grafe aj na vyšších timeframoch) indikátor volá `alert()`: v TradingView vytvor alert na indikátor s voľbou *Any alert() function call*.

### Limity TradingView
Na grafe môže byť naraz max. 500 štítkov a 500 rámčekov – staršie TradingView maže automaticky. Farbenie sviečok limit nemá. Počty v tabuľke sa počítajú z celej histórie načítanej na grafe.


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
