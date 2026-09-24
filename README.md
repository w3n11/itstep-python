# Python Advanced - Lekce 01: Úvod do OOP

## 📂 Struktura adresáře
Budou vás zajímat jen tři soubory:
* `README.md` – Tento soubor, který právě čtete. Obsahuje zadání lekce.
* `assignment.py` – Soubor, do kterého budete **psát svůj kód a řešení**.
* `run.py` – Testovací motor. Tento soubor neupravujte, slouží k automatickému hodnocení vaší práce.

---

## 🎮 Jak fungují testy?
Váš postup v hodině nebudu kontrolovat jen já, ale pomůže nám v tom automatizovaný systém. Strávil jsem nemalé úsilí napsáním testovacího frameworku, který bude okamžitě hodnotit, jak zdárně jste úlohy naprogramovali. 

Testy spustíte v terminálu příkazem (musíte se nacházet ve složce s projektem):
`python run.py`

Až testy spustíte, vypíše se vám přehledná tabulka toho, co už funguje `[PASS]`, a co ještě ne `[FAIL]`. **Vaším ultimátním cílem je do konce hodiny dokončit lekci na 100 %.**

💡 **Důležité:** Absolutně v žádném případě nemusíte upadat do depresí, pokud na vás výsledky testů budou ze začátku křičet žlutě a červeně. Programování je o dělání chyb a jejich opravování. Testy vám vždy napoví, kde je problém. Pokud si nebudete ani tak vědět rady, jsem tu od toho, abych vám pomohl.

---

## ⚖️ Pravidla

Aby testy vůbec prošly a uznaly vám řešení, **musíte** dodržovat následující pravidla. Pokud je porušíte, systém vás k testům ani nepustí:

1. **AI nástroje (ChatGPT, Claude, Copilot atd.):** Můžete používat na hledání chyb v kódu a jejich opravování, jako brainstorming, když vám zrovna vaše představivost a kreativita stávkují, nebo pro psaní nudných částí kódu, které jste psali už tisíckrát. Nepoužívejte AI, aby to "prostě napsala za vás." Musíte mi být schopni váš kód vysvětlit.
2. **Přísný seznam povolených modulů:** Můžete používat (importovat) pouze moduly, které jsou explicitně povolené na konci tohoto zadání. Jakýkoliv jiný `import` systém zablokuje.
3. **Žádné hackování:** Není přísně zakázáno pokoušet se pomocí kódu upravovat testovací soubor `run.py`, ale pokud vám něco v důsledku toho nebude fungovat, nebudu vám moct pomoci s opravou. Využívat kód ke škodlivým účelům je pak zakázáno.
4. **Čistota kódu:** Nepoužívejte globální proměnné. Obecně jsou považovány za nežádoucí a programátoři se jim vždy snaží vyhnout. Až bude váš kód funkční, můžete se zaměřit na doladění vašeho kódu dle standardu PEP8.
5. **Spustitelnost:** Kód nesmí obsahovat hrubé syntaktické chyby, s nimi nelze program spustit.

> *Pokud se domníváte, že váš kód splňuje všechna pravidla, a systém vás přesto odmítá pustit dál, zavolejte mě.*

---

## 🛠️ Zadání úloh

Svá řešení pište do souboru `assignment.py`.

### 1. Mazlíček
Implementujte třídu `Pet`, která bude obsahovat následující atributy:
- `name (str)`: jméno mazlíčka
- `energy (int)`: energie mazlíčka, výchozí hodnota = 5
- `happiness (int)`: radost mazlíčka, výchozí hodnota = 5

Funkce `__init__` bude kromě samozřejmého `self` příjimat i parametr `name`

> 💡 *Nezapomeňte na klíčové slovo `self`, které způsobí, že z proměnné vytvoříte atribut. Např. `self.name = name`.*

### 2. Metody mazlíčka
Implementujte do třídy `Pet` metody `play` a `sleep`.

- `sleep` zvýší `energy` o `5`.
- `play` zvýší `happiness` o `1`, ale sníží `energy` o `2`.

Pokud by `energy` nebo `happiness` mělo být vyšší než `10` nebo menší než `0`, nic se nestane a **metoda** nic neudělá.

## 🌟 BONUS
V rámci bonusu se vám odemkne 0 úloh navíc.


---
**📦 Povolené moduly v dnešní lekci:**
* `collections` *(default)* 
* `datetime` *(default)*
* `math` *(default)*
* `random` *(default)*
* `time` *(default)*
* `typing` *(default)*
