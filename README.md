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

### 1. Caesarova šifra
Implementujte funkci `caesar(alphabet, message, key)`, která bude vracet řetězec modifikovaný následovně: Každé písmeno v `message`, které se vyskytuje v `alphabet`, bude ve výsledném textu nahrazeno znakem, který je v `alphabet` o `key` pozic vpravo. Při přetečení `alphabet` se vraťte na začátek. Není-li znak z `message` v `alphabet`, nijak ho neměňte. 
> **Může se hodit:** `for` `if` `else` `return` `not`

### 2. Vernamova šifra
Implementujte funkci `vernam(alphabet, message, key)`, která bude implementovat variaci potenciálně nesilnější šifry na světě.
> **Může se hodit:** `>`, `<`, `return`,`int()`, `try`, `except`

### 3. Erastothenovo síto
Implementujte funkci `dice_roll()`, která po zavolání vrátí náhodné celé číslo v intervalu od 1 do 6 (včetně).
> **Může se hodit:** `import`, `random`...

### 4. Detekce prvočísla
Implementujte funkci `is_prime(n)`, která vrátí `True`, pokud je předané číslo `n` prvočíslo. V opačném případě vrátí `False`. 
*Bonusová výzva: Zamyslete se nad tím, jak by tento algoritmus bylo možné matematicky optimalizovat, aby zvládl bleskově ověřit i obrovská čísla. Obyčejný cyklus vám u velkých čísel může narazit na časový limit!*
> **Může se hodit:** `%`, `for` / `while`, `range()`...

---
**📦 Povolené moduly v dnešní lekci:**
* `random`