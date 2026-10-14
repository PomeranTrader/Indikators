# Infinity Pullback Return – Buy the Dip

*An Infinity Original · © 2026 Infinity*

**PREHĽAD**

Nástroj na meranie pullbacku po silnej sviečke. Každá robustná sviečka na impulznom timeframe otvorí jednu otázku: kedy sa cena vráti na jej open a zavrie gap, ktorý sviečka vytvorila. Indikátor túto otázku sleduje bar po bare, výsledok uloží a z celej histórie grafu skladá percentilové odpovede: ako často sa návrat stane, ako dlho trvá, koľko cena ešte ubehne, než sa otočí, a ako hlboko pod open po návrate siahne.

Žiadne vzorce, žiadne naháňanie signálov. Jedna úroveň na sviečku, meraná rovnako stále dokola, a štatistika, ktorá hovorí, čo sa pri nej historicky dialo.

**ČO VYKRESĽUJE**

• **Úroveň návratu**: open impulznej sviečky, vedená od close sviečky až po návrat ceny alebo po uplynutie horizontu. Farba hovorí stav: čaká, návrat dosiahnutý, bez návratu.
• **Štítok impulzu**: smer, veľkosť gapu, čas, počet línií stacku vnútri gapu, stav otočky Focus Touch MA a režim Greed & Fear v čase impulzu.
• **MMA stack**: Focus Touch MA, Daily Tester MA, First / Second / Third Trend Tester a Last Barricade, s voliteľným markerom dotyku Focus Touch MA.
• **Otočka Focus Touch MA**: značka na sviečke, ktorá potvrdila pullback.
• **Signál MS modelu**: trojuholník so štítkom, pod ním tri bodkované čiary očakávaného ponoru podľa reálnej štatistiky GFX MS 2026.
• **Značky GFX MS 2026**: reálne postnuté signály, pre porovnanie s modelom.

**PREPÍSANIE TIMEFRAMU**

Impulzná sviečka sa hľadá na zvolenom timeframe, meranie návratu beží na timeframe grafu. Tak sa dá zachovať štvorhodinový kontext a merať návrat s presnosťou pätnásťminútovej sviečky. Správanie povedané na rovinu:

• Impulz sa registruje až po uzavretí sviečky vyššieho timeframu. Historické hodnoty sa nedopočítavajú dopredu, takže úroveň sa nikdy neprekreslí.
• Línie stacku s vlastným timeframom sa na živej sviečke aktualizujú, kým sa sviečka vyššieho timeframu neuzavrie. Je to očakávané správanie, nie chyba.
• Impulzný timeframe nižší ako graf nedáva zmysel. Indikátor v takom prípade zobrazí varovanie v hlavičke tabuľky.

**ROBUSTNÁ SVIEČKA**

Sviečka je robustná, keď jej telo prevýši bežnú volatilitu impulzného timeframu alebo horný percentil tiel za posledné obdobie, a zároveň telo tvorí podstatnú časť celého rozsahu. Dlhé knôty teda nevyhovujú. Smer sa dá obmedziť na býčie impulzy, kde návrat k open znamená buy the dip, alebo na medvedie, kde ide o sell the rally.

**NÁVRAT K OPEN A JEHO ŠTATISTIKA**

Od uzavretia impulzu sa meria päť vecí:

• **Či** sa cena do zvoleného horizontu vrátila na open.
• **Kedy**, ako percentily času P25 / P50 / P75 / P90 a ako pravdepodobnosť návratu do jednej sviečky, štyroch, dvanástich, dvadsiatich štyroch, štyridsiatich ôsmich hodín a týždňa.
• **Rozbeh pred návratom**: koľko cena ešte ušla za close impulzu, než sa otočila. Toľko sa „zmešká", keď sa čaká na návrat.
• **Hĺbka pod open po návrate**: ako ďaleko pod open cena siahla v okne po návrate. Pre buy the dip je to očakávaný ponor pri vstupe presne na open.
• **Prežitie**: pre impulz, ktorý beží už určitý čas, podiel historických impulzov v rovnakej fáze, ktoré sa napokon vrátili, a zostávajúci čas P50 / P75 / P90.

**VZDIALENOSŤ OD STACKU A BARIÉRY**

Pri každom impulze sa uloží vzdialenosť ceny od všetkých šiestich línií v jednotkách volatility a smere impulzu. Štatistika ich triedi do košov: za líniou, do jednej, do dvoch, do troch a nad tri jednotky. Pre každú líniu a kôš je k dispozícii miera návratu a medián času.

Línie ležiace vnútri gapu, medzi open a close impulzu, sú **bariéry**: podpora na ceste späť. Nula bariér pri cene ďaleko nad stackom je natiahnutý trh, kde návrat býva rýchlejší. Viac bariér návrat spomalí alebo zastaví, čo štatistika ukáže samostatným riadkom podľa počtu bariér.

**OTOČKA FOCUS TOUCH MA**

Pullback je potvrdený, keď close zavrie pod Focus Touch MA pri býčom impulze, alebo nad ňou pri medveďom. Voliteľne sa vyžaduje aj otočený sklon línie. Štatistika hovorí, aký podiel návratov otočka predchádzala, ako dlho po impulze prichádza a ako dlho od otočky trvá dosiahnutie open. Je to filter pre načasovanie, nie signál sám osebe.

**GREED & FEAR**

Index 0 až 100 zložený z relatívnej sily, natiahnutia ceny od Daily Tester MA a First Trend Tester, momentum, dĺžky série sviečok bez dotyku Focus Touch MA a podielu býčích sviečok. Päť režimov od extrémneho strachu po extrémnu chamtivosť. Režim sa uloží ku každému impulzu, takže tabuľka ukáže, v ktorom režime sa návraty darili a v ktorom nie. Váhy zložiek sú nastaviteľné.

**MS MODEL A POROVNANIE S GFX MS 2026**

Model vygeneruje signál, keď sa cena dotkne open aktívneho impulzu, otočka Focus Touch MA je potvrdená, cena drží správnu stranu Last Barricade a Greed & Fear nie je v extréme proti smeru obchodu. Každý signál sa hneď spätne testuje: take profit v USD, maximálny ponor a čas do dosiahnutia. Výsledky stoja vedľa reálnej štatistiky 158 signálov GFX MS 2026: podiel dosiahnutých TP, percentily ponoru P50 / P75 / P90, medián času a pomer zisku k ponoru. Samostatný riadok hovorí, koľko reálnych GFX entry ležalo na úrovni open aktívneho impulzu, a v akom režime Greed & Fear boli postnuté.

**AKO TO POUŽÍVAŤ**

• **Čakanie na dip**: po robustnej býčej sviečke neskákať do trhu. Úroveň návratu a tabuľka aktívnych impulzov povedia, aká je šanca, že cena open ešte navštívi, a dokedy.
• **Čítanie natiahnutia**: čím ďalej je cena od stacku a čím menej bariér má v gape, tým skôr sa návrat historicky dostavil. Riadky vzdialenosti a bariér to dávajú v číslach pre konkrétny graf.
• **Potvrdenie**: vstup až po otočke Focus Touch MA skracuje čakanie a zvyšuje podiel návratov, ktoré prídu. Tabuľka ukáže, o koľko.
• **Očakávaný ponor**: pri signáli modelu sú pod vstupom tri úrovne podľa GFX štatistiky. Stop loss pod P75 alebo P90 je stop loss postavený na dátach, nie na odhade.
• **Režim trhu**: v extrémnej chamtivosti model BUY signály nedáva. Greed & Fear v hlavičke tabuľky hovorí, kde trh práve je.
• **Session**: riadok podľa session ukáže, po ktorej časti dňa impulzy najčastejšie nedokončia návrat.
• **Kalibrácia**: s rastúcou históriou grafu sa percentily spresňujú. Sivé bunky majú málo vzoriek a neslúžia na rozhodovanie.

**NASTAVENIA**

Impulzná sviečka: timeframe, kritérium robustnosti, podiel tela na rozsahu, minimálny gap, smer, horizont návratu, okno pre hĺbku pod open.
MMA stack: timeframe línií, viditeľnosť a farba každej línie, marker dotyku.
Potvrdenie pullbacku: definícia otočky, značka na grafe.
MS model: zapnutie, požadované filtre, tolerancia dotyku, take profit, timeout, kreslenie očakávaného ponoru, smer signálov.
Greed & Fear: váhy šiestich zložiek.
GFX MS 2026: značky na grafe, tolerancia pre zhodu entry s open impulzu.
Vizuál a tabuľky: limity kreslenia, veľkosti, pozície tabuliek, smer štatistiky, minimálny počet vzoriek, časová zóna, farby.

**POZNÁMKY**

Je to vizualizačný a merací nástroj. Signály MS modelu sú štatistická simulácia na porovnanie s reálnou stratégiou, nie odporúčanie na obchod. Alerty len oznamujú udalosti, ktoré indikátor meria. Interpretácia, veľkosť pozície a riadenie rizika zostávajú plne na používateľovi. Jednoduché dizajnom, užitočné disciplínou.
