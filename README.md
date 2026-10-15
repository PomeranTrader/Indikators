# Indikators

## GFX MS 2026 – Trade Map (`gfx-ms-2026-trade-map.pine`)

TradingView indikátor (Pine Script v6) pre **XAUUSD**, aktuálne **v5**. Zobrazí všetkých 161 manuálnych signálov GFX Premier Club (29.12.2025 – 13.10.2026, 14.10 chýba) priamo na grafe zlata: ponor s meračom, trvanie, zisk a štatistiky. Súbor je súkromný, nepublikovať.

### Inštalácia
1. Otvor graf **XAUUSD** (najlepšie M5 – H1) a dole klikni na **Pine Editor**.
2. Zmaž obsah editora a vlož **celý** súbor `gfx-ms-2026-trade-map.pine`. Posledný riadok je `// KONIEC SÚBORU – GFX MS Trade Map v5`. Ak sa vloží iba časť, na grafe sa ukáže červené upozornenie „KÓD JE NEÚPLNÝ“.
3. Klikni na **Uložiť** a potom na **Pridať do grafu**.

### Uzavreté obchody
| Prvok | Význam |
|---|---|
| Tyrkysová zóna | entry → TP. Výška je zisk, šírka je čas od postu po TP hit. |
| Farebná zóna pod entry | **max ponor** (MAE), farba podľa triedy ponoru. |
| Merač ponoru | zvislá šípka entry → dno ponoru v strede zóny, štítok `▼ 23.78 $ · 238 pip · 0.58 %` (od 10 $, na H4+ od 30 $). Voliteľná stupnica každých 10 $ (kreslí sa od najnovších obchodov v rámci limitu 500 čiar). |
| „od postu“ | 7.–13.10 zdroj udáva ponor od ceny v čase postu. Indikátor ho prepočíta na ponor od entry (známe dno, alebo cena postu z grafu do H1); na vyšších TF ostane hodnota „od postu“ a štítok to uvádza. |
| Bodkovaná diagonála + ◆ | dráha od entry k bodu, kde padol TP |
| ● | čas vyplnenia entry (ak je známy) |
| Žltá prerušovaná čiara | prikup / layer (napr. 2.10 4168.60) |
| Hlavný štítok + tooltip | číslo, stav, entry/TP, zisk, ponor, trvanie, poznámky, prepočet na lot |

### Otvorené obchody (bez výplne)
| Prvok | Význam |
|---|---|
| Šípka entry → aktuálna cena | zelená v zisku, červená v strate |
| Živý merač vpravo od poslednej sviečky | šípka entry → cena so stupnicou každých 10 $ (pri veľkej vzdialenosti väčší krok) a spoločný štítok: P/L v $, pipoch, % a na lot, do TP, max ponor, dno a jeho čas, ako dlho beží |
| Bodkovaná čiara | najhlbší ponor, merač ponoru pri čase postu |
| Tabuľka „OTVORENÉ – MERAČ PONORU“ | P/L, pipy, poloha ceny medzi dnom ponoru a TP, do TP, max ponor, ako dlho beží |

### Farby podľa ponoru (prahy sa dajú meniť)
`ČISTÝ ≤ 5 $` zelená · `MIERNY ≤ 15 $` limetková · `VÝRAZNÝ ≤ 30 $` oranžová · `HLBOKÝ ≤ 100 $` červená · `EXTRÉM > 100 $` fialová
Otvorené obchody: ponor, P/L a trvanie sa živo dopočítavajú z grafu, a ak graf ukáže TP hit, obchod sa prepne na „TP ✓ (graf)“.
`BEZ METRÍK` sivomodrá prerušovaná čiara: TP hit len podľa postu alebo nevyhodnotený signál, entry nie je známe.

### Tabuľky
- **Prehľad**: počty, TP %, priemerný, mediánový a maximálny ponor, trvanie, Ø zisk / Ø ponor, ponor prepočítaný na lot.
- **Rozdelenie ponoru**: počet a % v každej triede, textový histogram a priemerné trvanie triedy.
- **Mesačný prehľad**: signály, TP, Ø a max ponor, Ø trvanie a počet hlbokých ponorov za mesiac.
- **TOP N najhlbších ponorov**: vrátane otvorených obchodov.
- **Otvorené – merač ponoru**: živý stav otvorených obchodov.

### Nastavenia
Filter dátumu, typy signálov, minimálny ponor, režim „zvýrazniť iba hlboké“, merač ponoru (štítok od X $, % z ceny, krok stupnice, stupnica pri uzavretých, živý merač a jeho odstup), režim štítkov (Auto / Plné / Kompaktné / Iba číslo / Skryť), veľkosti, pipy, lot pre prepočet, časová zóna, všetky farby a pozície tabuliek.

Dáta pochádzajú z `gfx.db setup_metrics` (MAE strict fill) a z doplnenia MS 30.9.–13.10.2026 (ponor od postu; 7.–13.10 ceny GC=F − 27.72, entry 12. a 13.10 približné). Symbol ✎ znamená, že čas postu bol upravený. Samotné dáta sú aj v `gfx-ms-2026-data.pine` a ako tabuľka v `gfx-ms-2026-trades.csv`.

## V_Turn2.5 (`v-turn-2.5.pine`, `v-turn-2.5-legs.pine`)

TradingView indikátor (Pine Script v6, overlay). Obraty EMA(5) ako bubliny farbené podľa seánsy, zóny okolo obratu rušené po 3 dotykoch, push štatistika COMBO (Low/Mid/High AVG, P15, AVG, P85 za 30 dní), projekcie MIDAVG/HIGHAVG, merač gapov medzi zónami a tabuľka levelov.

- `v-turn-2.5.pine` je pôvodná verzia bez zmien (základňa).
- `v-turn-2.5-legs.pine` je tá istá verzia plus **doplnok V-Nohy** pripojený na koniec súboru. Pôvodný kód sa nemenil.

### Doplnok V-Nohy (skupina nastavení „V-Nohy (doplnok)“)
Noha je cesta medzi dvoma opačnými obratmi EMA: BUY noha dno → najbližší vrch, SELL noha vrch → najbližšie dno. Celý modul sa vypína prepínačom **Zapnúť modul V-Nohy**.

| Prvok | Význam |
|---|---|
| Vyplnený box + prerušovaná spojnica | medzera medzi dnom a vrchom (zelená BUY, červená SELL) |
| Štítok v strede nohy | `▲ 14 b · 3h30 · 52.0p` = sviečky, reálny čas, posun EMA v pipoch |
| Tabuľka V-NOHY | pre BUY, SELL a SPOLU z posledných N nôh: N, Ø a mediánový počet sviečok, min, max, Ø čas, Ø a mediánové pips, rýchlosť v pipoch za hodinu |
| Riadok AKTUÁLNA NOHA | koľko sviečok a času beží od posledného obratu, pips zatiaľ, % z Ø, koľko sviečok ostáva do Ø / mediánu / P85, rozsah high-low, stav SKORÁ · V NORME · ZRELÁ · PRETIAHNUTÁ |
| Projekcia (žltá) | zvislé čiary od posledného obratu v mieste Ø, mediánu a P85 trvania nôh rovnakého smeru plus vodorovná čiara Ø pips cieľa |

Čas sa meria reálne (minúty, hodiny, dni), takže rovnaké nastavenie funguje na M15, H1 aj H4. Počet nôh N (predvolene 20, max 100) riadi štatistiku aj to, koľko nôh ostáva nakreslených.
