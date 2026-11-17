# Pokyny pre prácu v tomto repe

## Všeobecné
- Kód sa do TradingView vkladá cez GitHub Raw odkaz na súbor vo vetve. Na konci každej odpovede o indikátore uviesť Raw odkaz. Náhľad v chate sa orezáva pri cca 16 000 znakoch, preto každý skript končí riadkom `// KONIEC SÚBORU – …`, podľa ktorého používateľ overí, že sa vložilo všetko.
- Pine Script v6. Texty v tabuľkách a štítkoch po slovensky, názvy premenných po anglicky.
- Pine kompilátor v prostredí nie je. Kód prechádzať ručne, držať sa vzorov z existujúceho skriptu. Pri chybe z TradingView používateľ pošle hlášku s číslom riadku.
- Nikdy nepoužívať názvy premenných, ktoré kolidujú so vstavanými priestormi Pine (`order`, `line`, `label`, `box`, `table`, `array`, `color`, `str`, `math`).

## V_Turn2.5 (súbory `v-turn-2.5*.pine`)
Vrstvený vývoj. Každý ďalší súbor je predošlý súbor plus nový modul pripojený na koniec. Pôvodný kód sa nikdy nemení, len sa dopĺňa.

| Súbor | Obsah |
|---|---|
| `v-turn-2.5.pine` | pôvodný indikátor V_Turn2.5 (493 riadkov), základňa, nemeniť |
| `v-turn-2.5-legs.pine` | základňa + modul **V-Nohy** (noha = cesta medzi dvoma opačnými obratmi EMA, štatistika trvania a veľkosti, projekcia Ø / Med / P85) |
| `v-turn-2.5-scen.pine` | legs + modul **V-Scenáre** (podobnostná analýza, max 10 variantov odkiaľ kam s pravdepodobnosťou, vejár od ceny, živá kontrola podmienok vyššie dno / prieraz T1) |

Pravidlá pre ďalšie moduly:
- Nový modul = nový súbor `v-turn-2.5-<názov>.pine` skopírovaný z posledného, modul pripojený za posledný blok, pred riadok `// KONIEC SÚBORU`.
- Každý modul má vlastnú skupinu vstupov `"<Názov> (doplnok)"` a hlavný prepínač `Zapnúť modul …`, aby sa dal celý vypnúť.
- Moduly z pôvodného kódu iba čítajú: `emaValue`, `isBullTurn`, `isBearTurn`, `get_pip_size()`, `get_size()`, `get_table_pos()`, `avg_arr()`, `percentile_arr()`. Z modulu V-Nohy sa dá použiť `fmt_dur()`, `fmt_num()`, `median_arr()`.
- Pred commitom overiť diffom, že predošlá časť súboru je bajt po bajte zhodná: `diff <(head -N nový.pine) <(head -N predošlý.pine)`.
- Po každom module doplniť sekciu do README.md.

Kľúčové fakty o pôvodnom kóde:
- Obrat = lokálne dno alebo vrchol EMA(5) na sviečke [1], potvrdený aktuálnou sviečkou. Bublina sa kreslí na `bar_index[1]`, `emaValue[1]`.
- Seánsa z hodiny v Europe/Bratislava: 0–7 Asia, 8–13 London, 14–23 NY.
- "Pips" = `syminfo.mintick * 10` pre forex, inak `mintick`. Pre XAUUSD sú to centy.
- Push automat drží jeden aktívny signál, opakovaný obrat rovnakým smerom ho nereštartuje. Modul V-Nohy to kopíruje, modul V-Scenáre pri opakovanom obrate ponechá extrémnejší (nižšie dno / vyšší vrch).
- Limity kreslenia 500 boxov, čiar a štítkov sú spoločné pre celý skript.

## Ostatné indikátory
Ďalšie indikátory (GFX MS Trade Map, Session Zone Map, Candle Size Scanner, Gold Greed/Fear, Infinity Pullback Return, SARUJA Trade Map) žijú vo vlastných vetvách `claude/*`. Táto vetva obsahuje len V_Turn a spoločný GFX základ.
