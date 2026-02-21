## Python Intermediate - L01 Úvod a opakování
Nejprve si připravíme prostředí pro vývoj. Dodržte následující kroky:
- Vstupte do složky `Dokumenty`/`Documents` a vytvořte složku s názvem ve tvaru `JménoPříjmení`. To bude vaše pracovní složka. Pokud si během tohoto tématu přesednete k jinému počítači, vytvoříte si novou složku s vlastním jménem i tam.
- Otevřete `Visual Studio Code`. Otevřete složku pomocí `Ctrl+K` a `Ctrl+O` a vyberte vaši složku.
- V levém panelu otevřete `Rozšíření`/`Extensions` a nainstalujte rozšíření `Flake8`.
- V nastavení tohoto rozšíření vepište do políčka `Flake8: Args` hodnotu `--max-line-length=120` a potvrďte.
- Pokud nejsou nainstalována rozšíření `Python`, `Pylance` a `Python Debugger`, nainstalujte je.
- Nainstalujte v příkazovém řádku modul `flake8` pomocí příkazu `pip install flake8`.

Gratuluji! To nejtěžší máte pravděpodobně dnes za sebou.
### Struktura adresáře
Budou vás zajímat jen tři soubory.
- `README.md` je soubor obsahující zadání lekce.
- `assignment.py` je soubor, do nějž budete implementovat vaše řešení.
- `run.py` je soubor obsahující testy. Spustit jej můžete v příkazovém řádku pomocí `python run.py`. Musíte se však v příkazovém řádku nacházet ve stejné složce.

### Testy
Váš postup v hodině nebudu pozorovat já sám, ale s Vaší pomocí. Strávil jsem totiž nemalé úsilí napsáním testovacího frameworku, které bude hodnotit, jak zdárně jste úlohy naprogramovali. Tento framework pravděpodobně nebude dokonalý a budu ho v průběhu lekcí upravovat na základě zjištěných chyb i Vašeho doporučení.

Testy sputíte v příkazovém řádku pomocí `python run.py`

Až testy spustíte, vypíše se vám, které testy prošly, a které ne. Vaším ultimátním cílem je do konce hodiny dokončit lekci na 100 %. Pokud budete chtít, můžete mi na konci hodiny své řešení zaslat a já Vám k němu poskytnu zpětnou vazbu.

Absolutně v žádném případě nemusíte upadat do depresí, kvůli tomu, že na Vás výsledky testů budou křičet žlutě a červeně. Testy Vám vždy řeknou, kde je chyba a pokud si nebudete ani tak vědět rady, jsem tu od toho, abych Vám pomohl.

### Pravidla pro psaní kódu
Testy se Vám ani nespustí, pokud:
- použijete globální proměnné
- vaše řešení bude nespustitelné například kvůli syntaktické chybě
- nedodržíte standard PEP 8

> Pokud se domníváte, že Váš kód splňuje výše zmíněné požadavky a ani tak jej nelze spustit, kontaktujte lektora.

**Není dovoleno využívat jazykové modely.**

## Zadání
### Vstup/Výstup
Implementujte funkci `hello_input()`, která načte ze vstupu jméno a následně vypíše `Hello <jméno>!`. Pokud je vstup prázdný nebo obsahuje jen bílé znaky, vypíše `Hello everyone!`.

`input` `print` `==`

### Ověření věku
Implementujte funkci `age_verification(limit)`, která načte ze vstupu číslo a vrátí `True`, pokud je načtená hodnota větší nebo rovna `limit`. Pokud bude číslo zadané na vstupu menší nebo jej nepůjde načíst, vraťte `False`.

`<` `>` `return` `int`

### Hod kostkou
Implementujte funkci `dice_roll()`, která vrátí náhodné celé číslo v intervalu <1, 6>.

`import`

### Detekce prvočísla
Implementujte funkci `is_prime(number)`, která vrátí `True`, pokud je `number` prvočíslo. `False` jinak. Zamyslete se, jak by tento algoritmus bylo možné optimalizovat.

`%` `for` `while` `range`