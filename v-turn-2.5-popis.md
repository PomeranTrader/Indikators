# V_Turn2.5 + V-Nohy + V-Scenáre – popis fungovania

Posledná verzia: `v-turn-2.5-scen.pine` (Pine Script v6, overlay, 1168 riadkov).
Vložiť celý súbor do Pine Editora v TradingView, posledný riadok musí byť
`// KONIEC SÚBORU – V_Turn2.5 + doplnok V-Nohy + doplnok V-Scenáre`.
Vhodné pre XAUUSD, forex aj crypto, časové rámce M15, H1, H4.

Skript má tri vrstvy. Každá ďalšia vrstva je doplnok pripojený na koniec, pôvodný kód sa nemenil.

---

## 1. Jadro V_Turn2.5 (pôvodný indikátor)

### Obrat EMA
- Počíta sa EMA(5) z close (dĺžka nastaviteľná).
- **BUY obrat (dno)**: EMA na sviečke [1] je nižšia než na [2] aj než na aktuálnej sviečke. EMA tvorí lokálne V.
- **SELL obrat (vrch)**: zrkadlovo, EMA na [1] je vyššia než na oboch susedoch.
- Bublina sa kreslí na sviečku [1] vo výške EMA[1]. Signál je teda potvrdený o jednu sviečku neskôr. Kým sa aktuálna sviečka formuje, bublina sa môže objaviť a zmiznúť, pevná je po zatvorení sviečky.

### Seánsy a farby
- Seánsa sa určí z hodiny sviečky [1] v zóne Europe/Bratislava: 0 až 7 Asia, 8 až 13 London, 14 až 23 NY.
- Šesť farieb pre kombinácie BUY/SELL × Asia/London/NY. Farba sa nesie do bubliny, zóny aj projekcií.

### Zóny
- Pri každom obrate vznikne box so stredom v EMA[1]. Výška podľa inštrumentu: zlato v USD, crypto v USD, forex v pipoch, inak manuálna hodnota.
- Box sa ťahá doprava. Každá sviečka, ktorej rozsah high až low sa prekryje so zónou, pripočíta dotyk. Po 3 dotykoch (nastaviteľné) sa zóna uzavrie a vypadne zo zoznamu aktívnych.

### Push štatistika COMBO
- V jednom čase je aktívny len jeden signál. Od vstupu (EMA[1] pri obrate) sa meria maximálny priaznivý posun: pre BUY high mínus entry, pre SELL entry mínus low.
- Keď príde opačný obrat, push sa zapíše do koša smer × seánsa a nový signál prevezme štafetu. Opakovaný obrat rovnakým smerom nič nezapíše ani nereštartuje entry.
- Tabuľka pre každý zo 6 košov: LowAVG (priemer spodných 15 %), MidAVG (priemer stredných 70 %), HighAVG (priemer horných 15 %), P15, AVG, P85, N. Okno posledných 30 dní.
- "Pips" = mintick × 10 pre forex, inak mintick. Pre XAUUSD sú to centy, takže 500p = 5 USD.

### Projekcie MIDAVG / HIGHAVG
- Pre posledné 2 bubliny sa z entry vynesie cieľ MidAVG a HighAVG daného koša ako čiara 80 sviečok doprava so štítkom v pipoch aj v cene.

### Merač gapov
- Medzi aktívnymi zónami zmeria medzeru (strop nižšej až dno vyššej) a 35 sviečok vpravo ju vykreslí ako zvislú čiaru so štítkom v USD a pipoch.

### Tabuľka levelov
- SELL zóny nad cenou a BUY zóny pod cenou, po 3 na každú stranu, s riadkom PRICE v strede a vzdialenosťou od ceny.

---

## 2. Modul V-Nohy (skupina nastavení „V-Nohy (doplnok)")

Otázka, na ktorú odpovedá: **ako rýchlo a ako ďaleko sa cena dostane od dna k najbližšiemu vrchu a naopak.**

### Noha
- **BUY noha** = dno EMA → najbližší vrch EMA (cena rastie).
- **SELL noha** = vrch EMA → najbližšie dno EMA (cena padá).
- Pri uzavretí nohy sa nakreslí vyplnený box od dna po vrch (zelený BUY, červený SELL), prerušovaná spojnica a štítok v strede: `▲ 14 b · 3h30 · 52.0p` = počet sviečok, reálny čas, posun EMA v pipoch.
- Rovnako ako pôvodný push automat, opakovaný obrat rovnakým smerom nohu nereštartuje.

### Tabuľka V-NOHY
Nad poslednými N nohami (predvolene 20, max 100), pre BUY, SELL a SPOLU:

| Stĺpec | Význam |
|---|---|
| N | počet nôh vo vzorke |
| Ø bary, Med bary | priemerný a mediánový počet sviečok |
| Min, Max | najkratšia a najdlhšia noha |
| Ø čas | priemerné reálne trvanie (m, h, d) |
| Ø pips, Med pips | priemerný a mediánový posun EMA |
| Rýchlosť | pips za hodinu |

### Riadok AKTUÁLNA NOHA
Živý stav bežiacej nohy od posledného obratu: sviečky, čas, pips zatiaľ, % z priemeru, koľko sviečok ostáva do Ø / Med / P85, rozsah high–low a stav:
- **SKORÁ** pod 50 % priemerného trvania
- **V NORME** 50 až 100 %
- **ZRELÁ** nad priemerom, ale do P85
- **PRETIAHNUTÁ** nad P85

### Projekcia
Žlté zvislé čiary od posledného obratu v mieste Ø, mediánu a P85 trvania nôh rovnakého smeru, plus vodorovná čiara priemerného cieľa v pipoch. Vzniká „očakávaný rám" nohy.

Čas sa meria reálne, takže rovnaké nastavenie funguje na M15, H1 aj H4.

---

## 3. Modul V-Scenáre (skupina nastavení „V-Scenáre (doplnok)")

Otázka, na ktorú odpovedá: **kam môže ísť ďalší pohyb a s akou pravdepodobnosťou, podľa podobných situácií v histórii.**

### Logika trhu, ktorú modul kóduje
Cena kmitá medzi BUY (dno) a SELL (vrch) obratmi EMA.
- **Rast** potrebuje vyššie dno než predošlé **a** prieraz horného SELL obratu.
- **Pokles** potrebuje nižší vrch než predošlý **a** prieraz dolného BUY obratu.

### Čo si modul ukladá
Striedajúce sa obraty (dno, vrch, dno, …). Ak prídu dva rovnaké za sebou, ponechá extrémnejší (nižšie dno / vyšší vrch). Pre každú dokončenú nohu zapíše:
- štruktúru na štarte: vyššie/nižšie dno, vyšší/nižší vrch → UPTREND, DOWNTREND, kompresia, expanzia
- veľkosť dvoch predošlých nôh (tvar situácie)
- veľkosť nohy v pipoch a sviečkach
- o koľko prerazila predošlý opačný obrat (alebo koľko chýbalo)
- či nasledujúce dno/vrch držalo (vyššie dno / nižší vrch)
- hĺbku návratu (nasledujúca protinoha / táto noha)

Potrebuje aspoň 7 uložených obratov, kým začne zapisovať. Dovtedy tabuľka píše „zbieram históriu".

### Výber podobných nôh
Pri bežiacej nohe vezme historické nohy rovnakého smeru s rovnakou štruktúrou a z nich N najpodobnejších podľa veľkosti posledných dvoch nôh (predvolene 30). Ak je zhodných menej než minimum (predvolene 8), vezme všetky nohy smeru a tabuľka to označí ako slabú vzorku.

### Pravdepodobnosť
Podmienená doterajším postupom nohy: počíta sa len z nôh, ktoré došli aspoň tam, kde je už aktuálna noha. Preto sa percentá počas nohy menia.

### Varianty (max 10, predvolene 6 najpravdepodobnejších)

| Variant | Cieľ | Pravdepodobnosť |
|---|---|---|
| Test horného SELL / dolného BUY obratu | T1 = posledný opačný obrat | podiel podobných nôh, ktoré došli aspoň k T1 |
| Prieraz → ďalší obrat | T2 = ďalší uložený obrat za T1 | podiel nôh, ktoré došli aspoň k T2 |
| Rýchly cieľ P25 | štart + 25. percentil veľkosti | ~75 % |
| Mediánový cieľ P50 | štart + medián | ~50 % |
| Silný cieľ P75 | štart + 75. percentil | ~25 % |
| Extrém P85 | štart + 85. percentil | ~15 % |
| Návrat → vyššie dno / nižší vrch | cez medián späť o mediánový návrat | podiel nôh, po ktorých dno/vrch držalo |
| Zlyhanie → nižšie dno / vyšší vrch | najbližší uložený obrat za štartom | podiel nôh, po ktorých dno/vrch nedržalo |

### Vejár na grafe
Od aktuálnej ceny vedú čiary k cieľom. Farba zelená → červená podľa pravdepodobnosti, hrúbka podľa pravdepodobnosti. Návrat je dvojúsek (plná čiara k mediánu, prerušovaná späť), zlyhanie bodkované. Štítok: číslo variantu, názov, cieľ, pips od ceny, percento, odhad sviečok z mediánovej rýchlosti podobných nôh.

### Tabuľka V-SCENÁRE
1. **Smer a štruktúra**: BUY/SELL noha, štart, sviečky, postup v pipoch, UPTREND / DOWNTREND / kompresia / expanzia.
2. **Vzorka**: počet podobných nôh, historická miera prierazu T1, miera držania dna/vrchu, medián nohy a návratu.
3. **Podmienka 1**: vyššie dno / nižší vrch než predošlé, ✓ alebo ✗.
4. **Podmienka 2**: horný SELL / dolný BUY obrat T1 prerazený ✓, alebo drží ✗ s počtom chýbajúcich pipov.
5. **Varianty V1 až V10**: scenár, cieľ, pips od ceny, pravdepodobnosť, odhad sviečok, poznámka.

---

## Nastavenia, ktoré sa oplatí ladiť

| Nastavenie | Predvolené | Vplyv |
|---|---|---|
| EMA Dĺžka | 5 | citlivosť obratov, viac = menej a väčších nôh |
| Počet sviečok na prerušenie | 3 | ako rýchlo sa rušia zóny |
| Počet posledných nôh (V-Nohy) | 20 | okno štatistiky a počet nakreslených nôh |
| Max počet variantov | 6 | koľko čiar vejára sa kreslí |
| Počet najpodobnejších nôh | 30 | menšie = presnejšia, ale šumovejšia vzorka |
| Min. vzorka pre zhodnú štruktúru | 8 | pod touto hodnotou sa berú všetky nohy smeru |
| Max uložených historických nôh | 300 | hĺbka pamäte modulu |

Každý modul má vlastný hlavný prepínač „Zapnúť modul …", takže sa dá testovať zvlášť.

## Obmedzenia
- Kód neprešiel kompilátorom TradingView v prostredí, kde vznikal. Pri chybe poslať hlášku s číslom riadku.
- Limity kreslenia 500 boxov, čiar a štítkov sú spoločné pre celý skript. Moduly pridávajú najviac ~100 boxov a ~130 čiar, najstaršie zóny jadra môžu zmiznúť skôr.
- Pravdepodobnosti sú historické frekvencie z malej vzorky, nie predpoveď. Slúžia na porovnanie variantov medzi sebou.
