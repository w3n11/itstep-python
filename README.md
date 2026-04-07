# Python Intermediate - Lekce 02: The Real Deal

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
3. **Žádné hackování:** Je přísně zakázáno pokoušet se pomocí kódu upravovat testovací soubor `run.py`, obcházet testy nebo využívat kód ke škodlivým účelům. Hrajeme fair-play.
4. **Čistota kódu:** Zákaz používání globálních proměnných. Dodržujte standard PEP 8 (na který dohlíží Flake8) a nebuďte laxní v typování proměnných.
5. **Spustitelnost:** Kód nesmí obsahovat hrubé syntaktické chyby.

> *Pokud se domníváte, že váš kód splňuje všechna pravidla, a systém vás přesto odmítá pustit dál, zavolejte mě.*

---

## 🛠️ Zadání úloh

Svá řešení pište do souboru `assignment.py`. Pod každým zadáním najdete klíčová slova a koncepty, které by se vám mohly při řešení hodit.

### 1. Vypsání nabídky
Implementujte funkci `print_menu(options: list[str])`, která vypíše nabídku menu ve formátu:
```
[1] Možnost 1
[2] Možnost 2
[3] Možnost 3
[0] Možnost 4
```
Tudíž při zavolání `print_menu(["Hello", "World", "Exit"])` bude výstup vypadat takto:
```
[1] Hello
[2] World
[0] Exit
```

### 2. Ošetření vstupu
Implementujte funkci `get_user_input(allowed: list[int])`, která od uživatele vyžádá hodnotu.
Funkce vyžaduje od uživatele vstup do té doby, než zadá hodnotu ze seznamu `allowed`.
Ošetřete chyby pomocí struktury:
```py
try:
    # V tomto bloku kódu může nastat chyba,
    # která způsobí pád programu. Např.:
    number: int = int("one")
except ValueError:
    # Kus kódu, který nastane, pokud v bloku
    # TRY nastane výjimka ValueError.
```

### 3. Můj první program
Sestavte program `dumb_menu()`, který vypíše nabídku alespoň tří kategorií zboží obchodníka v RPG (např. zbraně, zbroj, lektvary). Každá z možností povede na další nabídku o dvou možnostech (u zbraní například na dálku, na blízko).

Můžete si pro vizualizaci přidat výstup: `print(f"Chosen option {i}.")`.

Pokud uživatel zadá na vstupu `0`, a nachází se v našem hlavním seznamu o třech položkách, program se ukončí a vrátí posloupnost platných vstupů zadaných uživatelem v seznamu. Pokud uživatel zadá `0` v kterékoli vložené nabídce, vrátí se o úroveň výš.

Pokud se vám nelíbí téma fantasy RPG, můžete si vymyslet jiné, jméno funkce však ponechejte.

## Bonusové úlohy

Pokud jste vyřešili výše uvedené úlohy správně, můžete řešit níže uvedené bonusové úlohy.

### 1. Pokročilé házení kostkou
Implementujte funkci `dice_roll(dice_str: str) -> int`, která dostane na vstupu string ve tvaru `AdB+CdD`, kde `A`, `B`, `C` a `D` jsou celá kladná čísla, reprezentující sadu kostek a vrátí výsledek hodu těmito kostkami. Například pro string `2d6+1d12` házíme dvěma šestistěnnými kostkami a jednou dvanáctistěnnou kostkou.

---
**📦 Povolené moduly v dnešní lekci:**
* `collections` *(default)*
* `datetime` *(default)*
* `math` *(default)*
* `random` *(default)*
* `time` *(default)*
* `typing` *(default)*
