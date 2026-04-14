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


---
**📦 Povolené moduly v dnešní lekci:**
* `collections` *(default)*
* `datetime` *(default)*
* `math` *(default)*
* `random` *(default)*
* `time` *(default)*
* `typing` *(default)*
