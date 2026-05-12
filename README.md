# Python Intermediate - Lekce 06: Pokročilejší práce se soubory

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

### 1. Želví instrukce ze souboru

Implementujte funkci `turtle_from_file(filepath: str) -> None`, která přečte speciální soubor s vykreslovacími příkazy a pomocí modulu turtle je vykreslí na obrazovku.

Náš nový formát souborů má příponu `.turtledraw`. Každý řádek v tomto souboru představuje instrukce pro jednu samostatnou želvu (pro každý řádek v souboru tedy vytvořte novou instanci `t = turtle.Turtle()`).

Postup a pravidla:

- Validace formátu: Hned na začátku zkontrolujte, zda parametr filepath končí na příponu .turtledraw. Pokud ne, vyvolejte výjimku pomocí příkazu `raise Value Error("Invalid file format.")`.

- Načtení dat: Otevřete soubor pro čtení a získejte jednotlivé řádky.

- Zpracování řádků: Příkazy pro želvu jsou na každém řádku odděleny svislítkem `|` (tzv. pipe). Příklad jednoho řádku: `F100|R90|U|F50|D|C30|S50`.

- Interpretace příkazu: Každý příkaz se skládá z jednoho písmene (akce) a volitelně z čísla (hodnoty). Hodnotu nezapomeňte převést na desetinné číslo (`float`).

Podporované příkazy:

- `F`, `B`, `L`, `R`, `C` – Základní pohyby želvy (`forward`, `backward`, `left`, `right`, `circle`) o danou hodnotu.

- `U`, `D` – Zvednutí pera (`penup`) a položení pera (`pendown`). Tyto příkazy za sebou nemají žádné číslo.

- `S` – Vykreslí čtverec (Square), jehož délka strany odpovídá dané hodnotě. Tento příkaz želva nativně neumí, musíte ho naprogramovat pomocí cyklu (4x jdi dopředu a zahni o 90 stupňů).

💡 Nápovědy k implementaci:

- Abyste nemuseli psát nekonečně dlouhou sérii podmínek if/elif pro každý jeden příkaz, můžete využít slovník (`dict`). Do slovníku si totiž můžete uložit přímo samotné funkce (bez závorek)!
```python
commands_dict = {
    "F": t.forward,
    "L": t.left
}
# A poté funkci zavolat jednoduše takto:
commands_dict["F"](100)  # Uvede do pohybu funkci t.forward s argumentem 100
```
- Pro rozdělení příkazu na písmeno a číslo využijte slicing řetězců. První znak získáte jako `command[0]` a zbytek do konce řetězce získáte jako `command[1:]`. (Proměnná `command` zde představuje jeden příkaz, např. `F150`).

- Pokud narazíte na prázdný příkaz (například pokud by za sebou byla dvě svislítka `||`), jednoduše ho přeskočte např. klíčovým slovem `continue`.

### ❔ Nehodnocená úloha: Kódování obrázku
Zvládli byste v tuto chvíli už zakódovat obrázek do souboru, klidně v textové podobě?

---
**📦 Povolené moduly v dnešní lekci:**
* `turtle`
* `collections` *(default)* 
* `datetime` *(default)*
* `math` *(default)*
* `random` *(default)*
* `time` *(default)*
* `typing` *(default)*
