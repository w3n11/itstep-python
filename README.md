# Python Intermediate - Lekce 01: Úvod a opakování

Vítejte v první lekci! Nejprve si připravíme prostředí pro vývoj. Dodržte prosím následující kroky:

1. Vstupte do složky `Dokumenty` (`Documents`) a vytvořte si složku s názvem ve tvaru `JmenoPrijmeni`. To bude vaše pracovní složka. *(Pokud si během tohoto kurzu přesednete k jinému počítači, vytvoříte si novou složku se svým jménem i tam).*
2. Otevřete program **Visual Studio Code**. Otevřete svou složku pomocí zkratky `Ctrl+K` a následně `Ctrl+O`.
3. V levém panelu otevřete `Rozšíření` (`Extensions`) a nainstalujte rozšíření **Flake8**.
4. V nastavení tohoto rozšíření vepište do políčka `Flake8: Args` hodnotu `--max-line-length=120` a potvrďte.
5. Pokud nemáte nainstalována rozšíření **Python**, **Pylance** a **Python Debugger**, nainstalujte je.
6. Otevřete terminál (příkazový řádek) ve VS Code a nainstalujte potřebné kontrolní moduly pomocí příkazu:
   `pip install -r requirements.txt`

🎉 **Gratuluji! To nejtěžší (nastavení prostředí) máte pravděpodobně dnes za sebou.**

---

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

## ⚖️ Pravidla hry (Zákony frameworku)

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

### 1. Vstup a Výstup
Implementujte funkci `hello()`, která načte ze vstupu jméno uživatele a následně vypíše `Hello <jméno>!`. Pokud je vstup prázdný nebo obsahuje jen bílé (prázdné) znaky, vypíše univerzální `Hello everyone!`.
> **Koncepty k zamyšlení:** `input()`, `print()`, `==`, odstraňování mezer...

### 2. Ověření věku
Implementujte funkci `age_verification(limit)`, která se zeptá uživatele na jeho věk (načte ze vstupu číslo) a vrátí `True`, pokud je zadaná hodnota větší nebo rovna parametru `limit`. Pokud bude číslo zadané na vstupu menší, **nebo pokud uživatel zadá text, který nelze na číslo převést**, vraťte `False`.
> **Koncepty k zamyšlení:** `>`, `<`, `return`, převod přes `int()`, zachytávání výjimek...

### 3. Hod kostkou
Implementujte funkci `dice_roll()`, která po zavolání vrátí náhodné celé číslo v intervalu od 1 do 6 (včetně).
> **Koncepty k zamyšlení:** `import`, modul `random`...

### 4. Detekce prvočísla
Implementujte funkci `is_prime(n)`, která vrátí `True`, pokud je předané číslo `n` prvočíslo. V opačném případě vrátí `False`. 
*Bonusová výzva: Zamyslete se nad tím, jak by tento algoritmus bylo možné matematicky optimalizovat, aby zvládl bleskově ověřit i obrovská čísla. Obyčejný cyklus vám u velkých čísel může narazit na časový limit!*
> **Koncepty k zamyšlení:** operátor modulo `%`, cykly `for` / `while`, `range()`...

---
**📦 Povolené moduly v dnešní lekci:**
* `random`