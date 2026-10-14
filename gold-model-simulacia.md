# Kalibrácia modelu Gold G/F PRO simuláciou (Monte Carlo)

Reálne dáta nie sú z tohto prostredia dostupné (Yahoo, Stooq aj FRED sú blokované sieťovou politikou), preto je kalibrácia postavená na **syntetických dátach**. Simulátor `sim/gold_model_sim.py` replikuje logiku Pine skriptu v Pythone a generuje H1 bary zlata, DXY, US10Y, EURUSD, USDJPY a striebra s týmito vlastnosťami:

| Vlastnosť | Nastavenie |
|---|---|
| Volatilita na H1 bar | zlato 0.22 %, DXY 0.08 %, 10Y 1.1 bp, EURUSD 0.08 %, USDJPY 0.10 %, striebro 0.40 % |
| Makro väzba zlata | β voči DXY −0.9 (normálny režim) / −0.25 (slabý režim), β voči 10Y −0.012 % na bp / −0.004 |
| Prepínanie režimov | Markov, priemerná dĺžka režimu 1 500 barov (cca 9 týždňov na H1) |
| Vol clustering | multiplikatívny faktor s pamäťou 0.90 |
| Reziduál zlata vs makro | AR(1) s φ = 0.985 (polčas cca 46 barov): zlato sa od makra vzdiali a vracia |
| Korelácia DXY ↔ 10Y | +0.30 |

**Čo simulácia vie a nevie.** Vie overiť, že škálovanie a váhy dávajú rozumné rozdelenie skóre, že regresia správne odhaduje bety a že reziduálny sub-score zachytí to, čo má. Nevie dokázať predikčnú silu na reálnom zlate, lebo mean reversion reziduálu je v simulácii zabudovaná predpokladom. Ten predpoklad je empiricky rozumný (zlato sa po odchýlke od makra vracia), ale je to predpoklad.

## Výsledky

Mriežka 81 kombinácií (zCap × normLen × betaLen × resLen), 6 ciest × 9 000 barov každá, plus váhový sweep. Kľúčové čísla:

| Parameter | Testované | Zvolené | Prečo |
|---|---|---|---|
| zCap | 1.5 / 2.0 / 2.5 | **2.0** | 1.5 dáva 13 % času v extrémoch (príliš často), 2.5 len 3 % (príliš zriedka) |
| normLen | 120 / 250 / 500 | **250** | 500 má lepšiu väzbu reziduálu, ale pomalšie reaguje na zmenu režimu volatility |
| betaLen | 60 / 120 / 250 | **120** | korelácia odhadnutej β s pravou β: 0.67 (60) → 0.75 (120) → 0.76 (250); 120 je rovnako presné a rýchlejšie |
| resLen | 10 … 120 | **60** | väzba sub-score na pravú úroveň „zlato drahé / lacné vs makro" rastie do 60 a ďalej sa nemení |
| wRes / wTail | 0/0 … 50/25 | **35 / 15** | vyššia makro váha zväčšuje rozdiel budúceho výnosu medzi zónami, nad 35 už rastie len frekvencia extrémov |

Finálne nastavenie (16 ciest × 12 000 barov):

| Metrika | Hodnota |
|---|---|
| Čas v extrémnom strachu / chamtivosti | 5.1 % / 5.3 % |
| Čas v opatrnosti / chamtivosti (25–45 / 55–75) | 32 % / 33 % |
| Smerodajná odchýlka skóre | 15.1 |
| Epizódy extrému na 1 000 barov · priemerná dĺžka | 12.5 · 8.3 bary |
| Korelácia odhadnutej β(DXY) s pravou | 0.76 |
| Korelácia reziduálneho sub-score s budúcou zmenou reziduálu (24 b) | −0.06 (mean reversion správnym smerom) |
| Priemerný výnos zlata 24 b po extrémnom strachu / chamtivosti | +0.07 % / −0.01 % (v rámci predpokladov simulácie) |

## Ako sa makro väzba počíta v skripte

1. Na každom bare: výnos zlata `rG`, výnos DXY `rD`, zmena výnosu 10Y v bp `dY`.
2. Rolling dvojrozmerná OLS regresia cez `betaLen` barov: `rG = bD·rD + bY·dY + ε`. Bety sa počítajú z rolling variancií a kovariancií v uzavretom tvare, bez maticovej inverzie.
3. Implikovaný pohyb `bD·rD + bY·dY`, reziduál `rG − implikovaný`.
4. Súčet reziduálu za `resLen` barov → z-skóre cez `normLen` → sub-score 0–100. Kladný reziduál (zlato silnejšie než makro) = chamtivosť.
5. Tailwind: záporný priemer z-skóre zmeny DXY a 10Y za `resLen` barov → sub-score. Klesajúci dolár a výnosy = tailwind.

## Spustenie

```
python3 -I sim/gold_model_sim.py
```

Výstup mriežky je v `sim/grid_results.csv`.
