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

## Session Zone Map (`session-zone-map.pine`)

TradingView indikátor (Pine Script v6), ktorý automaticky napodobňuje rozloženie z referenčného grafu XAUUSD M30: session boxy, Buy/Sell zóny s popisom, plán obchodu (entry → TP / SL) a sivé úrovne s trendline. Nič sa nekreslí ručne, všetko vzniká z ceny.

### Inštalácia
1. Otvor graf (XAUUSD M15 – H1) a dole klikni na **Pine Editor**.
2. Zmaž obsah editora a vlož celý súbor `session-zone-map.pine`.
3. Klikni na **Uložiť** a potom na **Pridať do grafu**.

### Čo je na grafe
| Prvok | Význam |
|---|---|
| Prerušovaný rámec Tokyo / London / New York | rozsah session (high – low), názov nad rámcom, bodka na otvorení |
| Svetlá výplň v rámci | telo session (open – close) |
| Zelená zóna „Buy“ | dopyt zo swing low, z ktorého cena odišla; žije, kým ju close neprerazí |
| Červená zóna „Sell“ | ponuka zo swing high, symetricky |
| Prerušovaná stredová čiara | stred zóny |
| Tyrkysový box | plán: entry na hrane najbližšej zóny → TP (R × riziko) |
| Červený box | plán: entry → SL (za zónou + rezerva v ATR) |
| Štítky vpravo | ceny TP / entry / SL, tooltip s rizikom, ziskom a R |
| Sivé čiary | väčšie swing high / low, predĺžené doprava |
| Sivá trendline | spája posledné dva swing high (klesajúca) alebo swing low (rastúca) |
| „H“ / „L“ na okraji rámca + čiara doprava | high a low posledných 3 sessions (Ázia → Londýn → NY, 6 hodnôt); pri štarte ďalšej session sa najstaršia zmaže |
| Tabuľka v rohu | tie isté sessions: high, low, rozsah a kde je cena voči rozsahu (● = session beží) |

### Nastavenia
- **Sessions**: časová zóna, tri sessions (názov, čas HHMM-HHMM, farba), rámec / telo / názov / bodka, priehľadnosť, história.
- **Zóny**: Buy / Sell zapnúť, farba, text, citlivosť swingu, výška zóny (telo sviečky alebo ATR), predĺženie, max. počet, správanie po prerazení.
- **Plán obchodu**: počet zón, pomer zisk : riziko, rezerva SL, šírka a medzera boxov, štítky, farby.
- **Úrovne a trendline**: citlivosť swingu, max. počet, predĺženie, správanie po prerazení, farby.
- **High / Low sessions**: počet sessions v okne, hodnota na okraji rámca, čiara doprava a jej dĺžka a štýl, tabuľka a jej pozícia, veľkosť textu.

### Alerty
Cena vstúpila do Buy / Sell zóny, nová Buy / Sell zóna.

Plán obchodu je iba vizuál, nie signál. Červené šípky z referenčného grafu (projekcia cesty ceny) sú ručná kresba a indikátor ich nekreslí.

## Session Zone Strategy (`session-zone-strategy.pine`)

Testovacia stratégia (Pine Script v6, `strategy()`) postavená na rovnakých sessions a Buy/Sell zónach ako Session Zone Map. Vlož ju rovnako cez Pine Editor a dole otvor **Strategy Tester**.

### Logika obchodu
| Krok | Pravidlo |
|---|---|
| Vstup | limit na hrane najbližšej zóny (Buy pod cenou, Sell nad cenou) alebo market pri dotyku zóny; voliteľne iba vo zvolených sessions a v dátumovom rozsahu |
| Stop loss | pevný: za zónou + rezerva v ATR, alebo pevný počet bodov; nikdy sa nehýbe proti obchodu |
| Cieľ TP | R × riziko (predvolene 3) |
| Trail | keď cena prejde zvolené % cesty k TP (predvolene 50 %), stop ide za cenou v odstupe × riziko, × ATR alebo v bodoch |
| Voliteľné | pevný TP ako strop, posun SL na BE pri aktivácii trailu, max. 1 obchod na zónu |

Na grafe sú čiary entry / stop (červený = pevný SL, oranžový = trail) / TP, úroveň aktivácie trailu a výplň zisku a rizika. Pri výstupe sa zobrazí štítok s výsledkom v R a typom výstupu (SL / Trail / TP). Tabuľka v rohu: obchody, úspešnosť, výstupy podľa typu, súčet a priemer R, profit factor, čistý zisk.

Veľkosť pozície je predvolene 1 kontrakt (na OANDA XAUUSD 1 oz), takže zisk v USD = pohyb ceny. Lot a poplatky nastav v Properties.
