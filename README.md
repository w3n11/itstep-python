# Python Intermediate - Lekce 03: Bublinkové třídění

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

1. **Zákaz AI nástrojů (ChatGPT, Claude, Copilot atd.):** V jiných částech výuky vám možná AI povolím, ale tady se učíme naprosté základy logiky. Pokud za vás kód napíše jazykový model, ochudíte se o ten důležitý moment pochopení a naučíte se *prd*. Pište to sami.
2. **Přísný seznam povolených modulů:** Můžete používat (importovat) pouze moduly, které jsou explicitně povolené na konci tohoto zadání. Jakýkoliv jiný `import` systém zablokuje.
3. **Žádné hackování:** Je přísně zakázáno pokoušet se pomocí kódu upravovat testovací soubor `run.py`, obcházet testy nebo využívat kód ke škodlivým účelům.
4. **Čistota kódu:** Nepoužívejte globální proměnné. Obecně jsou považovány za nežádoucí a programátoři se jim vždy snaží vyhnout. Až bude váš kód funkční, můžete se zaměřit na doladění vašeho kódu dle standardu.
5. **Spustitelnost:** Kód nesmí obsahovat hrubé syntaktické chyby, s nimi nelze program spustit.

> *Pokud se domníváte, že váš kód splňuje všechna pravidla, a systém vás přesto odmítá pustit dál, zavolejte mě.*

---

## 🛠️ Zadání úloh

Svá řešení pište do souboru `assignment.py`.

### 1. Bubble sort
Implementujte funkci `bubble_sort(assorted_list: list[int])`, která vrátí setřízený seznam. Původní seznam **musí zůstat nezměněn**!

V programování je často potřeba něco setřídit. Proto existují třídící algoritmy - a my si jeden takový dnes naprogramujeme. Jmenuje se bubble sort (bublinkové třídění.) Funguje na velmi jednoduchém principu:

```
Pokud A > B a zároveň je A nalevo od B, prohoď A a B.
```

**Jak prohodíme obsahy dvou proměnných?**<br>Máte v zásadě dva jednoduché způsoby:
```py
var_a = 1
var_b = 2

temp = var_a
var_a = var_b
var_b = temp

print(f"var_a: {var_a}, var_b: {var_b}")
```
vypíše:
```
var_a: 2, var_b: 1
```

To je sice způsob správný a zaručený, ale Python má přeci jenom něco navíc, a to jednoduché prohození obsahu dvou proměnných pomocí:
```py
var_a, var_b = var_b, var_a
```

Zamyslete se nad tím, jak by šel tento algoritmus optimalizovat.


## Bonusové úlohy

Pokud jste splnili všechny povinné úlohy správně, můžete se pustit do vypracování bonusu.

### 1. Linear search
Implementujte funkci `linear_search(to_search, target)`, která prohledá seznam **lineárně** (jeden po druhém) a vrátí `True`, pokud je hodnota `target` v seznamu `to_search`. Jinak `False`.

### 2. Binary search
Implementujte funkci `binary_search(to_search, target)`, která prohledá seznam **binárně** (metodou půlení intervalů) a vrátí `True`, pokud je hodnota `target` v seznamu `to_search`. Jinak `False`.

Metoda půlení intervalů funguje takto:

Představte si, že hledáte `7` v seznamu čísel `2, 3, 4, 5, 6, 7, 8, 9, 10`.

1. Zvolíte prostřední prvek. Tím rozdělíte seznam na dvě poloviny, na tu, která obsahuje hodnoty menší než ta, která je uprostřed, a na tu druhou, kde jsou hodnoty větší.
2. Porovnáte příslušnou hodnotu: `6 (prostřední hodnota) < 7 (náš cíl)`. Šest je menší než sedm, proto se přesuneme do horní poloviny, protože nás nižší hodnoty nezajímají.
3. Nyní prohledáváme už jen `6, 7, 8, 9, 10`. Stejný případ s prostřední `8`. Ta je tentokrát větší, než `7`, proto se přesuneme do dolní poloviny.
4. Nyní prohledáváme `6, 7, 8`. Prostřední hodnota je náhodou ta, kterou hledáme. Našli jsme `7`.

```
2 3 4 5 6 7 8 9 10
        6 7 8 9 10
        6 7 8
          7       stačily nám čtyři kroky, abychom našli 7
```
Jaké má tento přístup nevýhody?

---
**📦 Povolené moduly v dnešní lekci:**
* `collections` *(default)*
* `datetime` *(default)*
* `math` *(default)*
* `random` *(default)*
* `time` *(default)*
* `typing` *(default)*
