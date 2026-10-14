# Zlato a prepojené trhy – faktorová analýza pre model Gold G/F PRO

Cieľ: vybrať faktory, ktoré reálne hýbu XAUUSD, určiť očakávaný smer vzťahu a spôsob, akým ich model váži. Živé čísla (korelácie, zmeny, skóre) počíta indikátor priamo na grafe; tento dokument vysvetľuje logiku.

## 1. Mapa vzťahov

| Faktor | Symbol (TV) | Očakávaný vzťah k zlatu | Typická sila (denné výnosy) | Mechanizmus |
|---|---|---|---|---|
| Reálne výnosy US 10Y | `FRED:DFII10` (len D) | **inverzný** | silný, r ≈ −0.4 až −0.7 na úrovniach | zlato nenesie úrok; rastúci reálny výnos zvyšuje náklad držania |
| Nominálny US 10Y | `TVC:US10Y` | **inverzný** | stredný, r ≈ −0.2 až −0.5 | proxy reálneho výnosu; v inflačných šokoch vzťah slabne |
| US 2Y (Fed očakávania) | `TVC:US02Y` | **inverzný** | stredný | rýchlejšie reaguje na repricing Fedu než 10Y |
| DXY | `TVC:DXY` | **inverzný** | stredný až silný, r ≈ −0.3 až −0.6 | zlato je kótované v USD; silnejší dolár = drahšie zlato pre zvyšok sveta |
| EURUSD | `FX:EURUSD` | **priamy** | stredný, zrkadlo DXY (EUR má ~57 % váhu v DXY) | cez USD kanál; vhodný pre pipový pohľad |
| USDJPY | `FX:USDJPY` | **inverzný / slabý** | slabý až stredný | USD sila + risk-off (JPY posilňuje v panike, zlato tiež) |
| Striebro | `OANDA:XAGUSD` | **priamy** | silný, r ≈ +0.7 až +0.85 | rovnaký monetárny faktor, vyššia beta (≈1.3–1.8×) |
| S&P 500 | `SP:SPX` | **nejednoznačný** | slabý, mení znamienko | risk-on fáza: likviditná korelácia +; krízy: safe-haven − |
| VIX | `TVC:VIX` | **priamy / šokový** | slabý mimo šokov | zlato ako poistka pri raste strachu; ale pri margin-call likvidácii padá spolu so všetkým |
| Ropa (WTI) | `TVC:USOIL` | slabo priamy | slabý | inflačné očakávania → breakeven → reálny výnos |
| Bitcoin | `BITSTAMP:BTCUSD` | nestabilný | slabý | „digitálne zlato" naratív prichádza a odchádza |

Poznámka k režimom: v rokoch 2022–2024 sa vzťah zlato ↔ reálne výnosy výrazne oslabil (nákupy centrálnych bánk, de-dolarizácia). Preto model **neverí fixnému znamienku naslepo** – každý faktor má mód `Inverse` / `Direct` / `Auto (by corr)` a jeho váha sa škáluje živou koreláciou. Ak sa vzťah rozpadne, faktor automaticky stratí vplyv na skóre.

## 1b. Makro väzba: DXY a dlhopisy ako spoločný pohyb

Samostatný faktor „DXY klesá" alebo „výnosy klesajú" nestačí, zlato reaguje na **kombináciu**. Model preto beží rolling dvojrozmernú regresiu výnosov zlata na výnos DXY a zmenu výnosu 10Y (okno 120 barov) a z nej počíta **makrom implikovaný pohyb zlata**. Rozdiel medzi skutočným a implikovaným pohybom za 60 barov je reziduál:

- reziduál > 0: zlato rastie viac, než by malo podľa dolára a výnosov (alebo padá menej). Dopyt mimo makra: centrálne banky, geopolitika, retail. Čím vyššie, tým viac chamtivosti a tým väčšie riziko návratu.
- reziduál < 0: zlato je slabšie než makro. Likvidácia, margin cally, rotácia. Strach.

Druhá časť je **tailwind**: priemer z-skóre zmeny DXY a 10Y za rovnaké okno so záporným znamienkom. Hovorí, či makro prostredie zlatu práve pomáha alebo prekáža, nezávisle od toho, čo zlato urobilo.

Kalibrácia (simulácia, `gold-model-simulacia.md`): beta okno 120, okno reziduálu 60, váhy 35 (reziduál) a 15 (tailwind). Tieto dve zložky majú spolu 50 zo 175 bodov váhy, k tomu DXY a US10Y ako samostatné sloty s ďalšími 20 bodmi. Makro je tak zhruba 40 % modelu.

## 2. Ako model faktory používa

1. **Zmena faktora** za `macroLen` barov (štandardne 20) na timeframe grafu – v % a v natívnych jednotkách (pipy pre FX, bp pre výnosy, body pre VIX).
2. **Normalizácia** z-skóre na `normLen` barov (250) → mapovanie 0–100 cez `zCap`.
3. **Znamienko**: inverzný faktor sa otočí (100 − skóre), priamy ostáva, Auto berie znamienko aktuálnej korelácie.
4. **Efektívna váha** = nastavená váha × zarovnanie korelácie:
   - Inverse: `max(0, −r)`; Direct: `max(0, +r)`; Auto: `|r|`.
   - Ak je korelácia proti očakávaniu, váha je 0 a faktor na skóre nevplýva.
5. Vážený priemer všetkých dostupných komponentov (RSI, SMA vzdialenosti, ATR režim, sentiment, faktory) → EMA vyhladenie.

Mini graf v tabuľke je sparkline z posledných `sparkLen` barov faktora (min–max normalizovaný). Stĺpec „Dnes" je zmena od denného open faktora.

## 3. Volatilita – čo sa meria (posledných 30 dní)

Z denných dát XAUUSD (vždy z **uzavretých** dní, bez repaintu):

| Metrika | Použitie |
|---|---|
| ADR priemer / medián / σ / max | základ pre očakávaný denný range |
| Realizovaná volatilita (σ denných log výnosov, anualizovaná) | 1σ denný pohyb v USD = close × σ |
| ATR(14) / ATR(30) denné | **vol scale** – zrýchľuje alebo brzdí projekciu (0.5–2.0×) |
| Dnešný range vs ADR | koľko % „normálneho" dňa je už odohraných |

## 4. Seansy – projekcia range a maximálne odchýlky

Pre každú seansu (Asia 09:00–15:00 Tokyo, London 08:00–16:30 London, New York 08:30–17:00 NY – nastaviteľné) indikátor ukladá posledných 30 uzavretých seáns:

- **range** = high − low seansy,
- **up excursion** = high − open seansy (max pohyb nahor od otvorenia),
- **down excursion** = open − low.

Z nich: priemer, medián, σ, p90, max. Projekcia ďalšej seansy:

- **Očakávaný range** = priemer range × vol scale, pásmo ± σ, p90 a 30-dňové maximum ako „stresové" hranice.
- **Očakávaný high / low** = referenčná cena + Ø up × vol scale / − Ø down × vol scale.
- **Maximálna odchýlka** = max up / max down z okna (najhorší prípad za 30 seáns).

Na cenovom grafe sa pri otvorení seansy vykreslia čiary: open (čiarkovaná), očakávaný high/low (plné) a max high/low (bodkované) + štítok. Pred otvorením sa projekcia počíta od aktuálnej ceny v tabuľke.

## 4b. Cesta v čase – profil seansy

Range seansy nie je jedno číslo, ale krivka v čase. Model preto pre každú seansu ukladá **odchýlku od open v každom 30-minútovom úseku** (max nahor = high − open, max nadol = open − low, kumulatívne). Z posledných 30 seáns vznikne matica 30 × počet úsekov a z nej:

- **typická krivka** = priemer stĺpca v danom čase (× vol scale),
- **p90 krivka** = 90. percentil stĺpca (bez škálovania, „stresová" hranica),
- **typický čas high / low** = najčastejší úsek, v ktorom seansa urobila svoj high / low.

Na grafe je to kužeľ: po otvorení je úzky, s časom sa rozširuje podľa toho, ako rýchlo trh v tej seanse zvyčajne „dýcha". London typicky zrýchli v prvých 90 minútach a znova pri otvorení NY, New York má najväčší prírastok okolo 14:30–16:00 London (makro dáta, otvorenie akcií). Kužeľ sa opiera o reálne čísla z grafu, nie o tieto všeobecné pravidlá.

Čítanie: cena na hornej typickej hranici = seansa už odohrala svoj priemer v tomto čase, ďalší pohyb nahor je „nadpriemer". Cena mimo p90 = ide o výnimočnú seansu (1 z 10), typicky makro udalosť. Vtedy platí štatistika chvosta, nie priemer.

## 5. Praktické čítanie

- Skóre < 25 + faktory potvrdzujú (DXY a výnosy klesajú, striebro drží) → sell-off je pravdepodobne „umytý", hľadaj obrat.
- Skóre > 75 + Dnešný range > 100 % ADR + seansa prekročila p90 → trh je natiahnutý, nehnať sa za pohybom.
- Ak sa live korelácia DXY otočí na kladnú, váha DXY klesne na 0 – sleduj tabuľku, nie prednastavené pravdy.
- Projekcia je štatistika, nie predpoveď: pri makro udalostiach (FOMC, NFP, CPI) rátaj s p90 až max, nie s priemerom.
