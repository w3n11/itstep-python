# Python Advanced - Lekce 04: Oprava kódu

## Zadání úloh

Své řešení a opravy kódu pište do souboru assignment.py.

### 0. Než začneme: Vítejte v reálném světě
Dnes nebudete psát aplikaci na zelené louce. Nastoupili jste jako noví vývojáři do banky a dostali jste na stůl kód od vašeho předchůdce, který byl včera vyhozen, protože to celé vibecodoval. Aplikace sice *nějak* funguje a jde spustit, ale oddělení kvality k ní napsalo sadu automatických testů, které odhalily kritické nedostatky.

Dnes si vyzkoušíme TDD (**Test-Driven Development**) v praxi. Vaším hlavním nástrojem nebude jen psaní kódu, ale především čtení. Budete muset číst testy, pochopit, co se snaží ověřit, a analyzovat chybové hlášky, abyste zjistili, proč aktuální kód selhává.

### I. První spuštění a analýza škod

*1.0 - 1.1*\
Zkuste aplikaci spustit. (`assignment.py`) Zdánlivě funguje. Nyní spusťte testy. (`run.py`) Uvidíte, že ani zdaleka neprojde vše.

Váš první úkol:

* Přečtěte si názvy selhávajících testů.

* Zjistěte, na čem padá načítání databáze. Proč se testům nedaří podstrčit bance testovací soubor? Podívejte se do metody load_accounts. Jak přesně se tam otevírá soubor? Je to dynamické, nebo tam předchůdce nechal něco "natvrdo"?

### II. Oprava logických a fatálních chyb

*2.0 - 2.1*\
Testy hlásí problémy s přihlašováním.
Zjistěte z výpisu testů, s jakými údaji se testovací framework snaží přihlásit a proč to nefunguje.

* Podívejte se na to, jak kód porovnává zadané heslo s heslem v databázi.

* Proč jeden z testů padá na *nekonečné smyčce*?

### III. Bezpečnostní audit: Krádeže v přímém přenosu

*3.0 - 3.2*\
Jakmile zprovozníte přihlašování, začnou vás trápit transakce (metoda process_payment). Kód je napsaný tak nešťastně, že umožňuje uživatelům krást peníze nebo poslat banku do krachu.

Čtěte pozorně chybové hlášky testů a prozkoumejte matematiku uvnitř `process_payment`:

* Co se stane, když uživatel odešle 2000 Kč?

* Co se stane, když se uživatel rozhodne odeslat -5000 Kč?

* Co brání uživateli, který má na účtu 100 Kč, odeslat milion?

Opravte metodu `process_payment` tak, aby před samotným převodem proběhly všechny nutné kontroly. Pokud je něco špatně, vyhoďte příslušnou výjimku (`InvalidAmountError` nebo `InsufficientFundsError`), které už v kódu máte připravené.

## BONUS: Princip zachování peněz (Integrita systému)
V uzavřeném bankovním systému nesmí peníze nikdy vzniknout zničehonic, ani se nesmí vypařit. Mohou se jen přesouvat mezi účty. Pokud někdo najde skulinu v paměti a přičte si 100 000 Kč, banka to musí okamžitě poznat.

*4.0 - 4.1*\
Zaveďte do banky systém podvojné kontroly:

Upravte inicializaci třídy `Bank`. Jakmile se načtou všechny účty, spočítejte celkový součet všech peněz v bance a uložte si ho do nového atributu.

Vytvořte novou metodu `check_integrity(self) -> bool`.

Tato metoda kdykoliv znovu sečte aktuální zůstatky na všech účtech a porovná je s počátečním stavem. Pokud peníze sedí, vrátí `True`. Pokud se někde vzaly peníze navíc (nebo chybí), vrátí `False`.

Testovací framework se v bonusovém testu pokusí vaši banku hacknout a tajně si připsat peníze na jeden z účtů. Vaše metoda `check_integrity` ho musí odhalit.

---

Povolené moduly v dnešní lekci:

* collections (default)
* datetime (default)
* math (default)
* random (default)
* time (default)
* typing (default)
* database (custom read-only file)
* os