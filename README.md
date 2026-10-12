# Python Advanced - Lekce 03: Výjimky a ošetření chyb

## Zadání úloh

Své řešení pište do souboru `assignment.py`.

### 0. Než začneme...
Při programování už jste se určitě setkali s nějakou **VÝJIMKOU**. Je to způsob, jak programátorovi říct, že se stala v kódu chyba. Ne vždy jsou ale chyby nechtěné. Programátor s nimi může počítat a napsat program tak, aby s chybou počítal a zotavil se z ní.

Každý importovaný modul může definovat vlastní výjimky. Nám budou pro dnešek stačit jen ty z výchozího modulu 
```
BaseException
 ├── BaseExceptionGroup
 ├── GeneratorExit
 ├── KeyboardInterrupt
 ├── SystemExit
 └── Exception
      ├── ArithmeticError
      │    ├── FloatingPointError
      │    ├── OverflowError
      │    └── ZeroDivisionError
      ├── AssertionError
      ├── AttributeError
      ├── BufferError
      ├── EOFError
      ├── ExceptionGroup [BaseExceptionGroup]
      ├── ImportError
      │    └── ImportCycleError
      │    └── ModuleNotFoundError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── MemoryError
      ├── NameError
      │    └── UnboundLocalError
      ├── OSError
      │    ├── BlockingIOError
      │    ├── ChildProcessError
      │    ├── ConnectionError
      │    │    ├── BrokenPipeError
      │    │    ├── ConnectionAbortedError
      │    │    ├── ConnectionRefusedError
      │    │    └── ConnectionResetError
      │    ├── FileExistsError
      │    ├── FileNotFoundError
      │    ├── InterruptedError
      │    ├── IsADirectoryError
      │    ├── NotADirectoryError
      │    ├── PermissionError
      │    ├── ProcessLookupError
      │    └── TimeoutError
      ├── ReferenceError
      ├── RuntimeError
      │    ├── NotImplementedError
      │    ├── PythonFinalizationError
      │    └── RecursionError
      ├── StopAsyncIteration
      ├── StopIteration
      ├── SyntaxError
      │    └── IndentationError
      │         └── TabError
      ├── SystemError
      ├── TypeError
      ├── ValueError
      │    └── UnicodeError
      │         ├── UnicodeDecodeError
      │         ├── UnicodeEncodeError
      │         └── UnicodeTranslateError
      └── Warning
           ├── BytesWarning
           ├── DeprecationWarning
           ├── EncodingWarning
           ├── FutureWarning
           ├── ImportWarning
           ├── PendingDeprecationWarning
           ├── ResourceWarning
           ├── RuntimeWarning
           ├── SyntaxWarning
           ├── UnicodeWarning
           └── UserWarning
```
> Všimněte si, že zde probíhá **dědičnost**, např. `KeyboardInterrupt` je potomkem `BaseException`, nebo `UserWarning` je potomkem `Warning`, které je potomkem `Exception`, která je potomkem `Exception`.

### I. Když to nejde hacknout, tak to aspoň shodíme...

*1.0 - 1.7*\
Vytvořte třídu `ExceptionRaiser`. Přidejte do ní následující metody (nepotřebují žádné parametry kromě ;`self`). Každá metoda musí svým kódem vyvolat přesně tu výjimku, kterou má v názvu:

* `arithmetic_error(self) -> None` – Zkuste provést nějakou neplatnou matematickou operaci (např. dělení nulou vyvolá `ZeroDivisionError`, což je potomek `ArithmeticError`).
* `attribute_error(self) -> None` – Zkuste přistoupit k vlastnosti (atributu), kterou daný objekt vůbec nemá.
* `lookup_error(self) -> None` – Zkuste sáhnout pro data, která neexistují (např. mimo rozsah seznamu nebo na neexistující klíč ve slovníku – obojí vyvolá potomka `LookupError`).
* `os_error(self) -> None` – Zkuste například otevřít kód ke čtení souboru, který na disku prokazatelně neexistuje.
* `runtime_error(self) -> None` – Vyvolejte chybu běhu (například nekonečnou rekurzí – funkce bude volat sama sebe, dokud nedojde k vyčerpání paměti).
* `value_error(self) -> None` – Zkuste převést nevhodný datový typ na jiný (např. string `"number"` na celé číslo `int`).

> Zatím nepoužívejte klíčové slovo `raise`.

### II. Nejlepší obrana je obrana

*2.0*\
Vytvořte třídu `Server`, jejíž **konstruktor** (``__init__``) nepříjímá žádný parametr, a která bude mít jediný atribut `self.firewall_enabled` typu `bool` nastavený na `False`. Rovněž implementujte metodu `enable_firewall(self) -> None`, která nastaví tento atribut na hodnotu `True`. Tuto metodu budeme potřebovat později.

*2.1 - 2.8*\
Náš server bude přijímat data z internetu pomocí metody `receive_payload(self, payload: str) -> str`, kterou teď naimplementujte.

Server však přijme jen ta data, která jsou v pořádku. Pokud `payload` z nějakého důvodu v pořádku není, vyhodíte specifickou výjimku s pomocí `raise Exception()`

**Platný** `payload` vypadá například takto: `0x08DEADDROP`.
* Zkontrolujte, zda je payload text (`str`). Pokud ne, vyhoďte `TypeError`.
* Zkontrolujte, zda začíná hlavičkou `"0x"`. Pokud ne, vyhoďte `ValueError`.
* Další dva znaky payloadu (např. `"08"` z `"0x08DEADDROP"`) určují délku zbytku zprávy. Převeďte je na číslo a zkontrolujte, že zbytek textu je přesně takto dlouhý (délka celého textu musí být `číslo + 4`). Pokud délka nesedí, vyhoďte `ValueError`. (Poznámka: už samotný převod písmen na číslo pomocí `int()` může sám vyhodit `ValueError`, nebraňte mu v tom).
* Pokud je vše v pořádku, odřízněte první 4 znaky a vraťte čistou zprávu.

*3.0 - 3.9*\
Vestavěné chyby nám nestačí pro bezpečnostní logování.

Vytvořte si vlastní třídu výjimky jménem `SecurityError`, která bude dědit z `Exception` (tělo nechte prázdné).

Pomocí bloku TRY-EXCEPT, je-li zapnutý firewall, zajistěte, aby při chybě metoda `receive_payload` vyhodila `SecurityError`.
```py
try:
    # kód, v němž se může stát chyba
except ValueError:
    # pokud nastane ValueError, skočí se sem, jako by se blok TRY
    # vůbec nevykonal (kromě interakcí s externími zdroji)
except Exception as e:
    # pokud nastane jiná výjimka, můžeme ji odchytit takto a uložit
    # do proměnné e a dále s ní pracovat
finally:
    # tento kus kódu se vykoná vždy, ať výjimka nastane, nebo ne
```

> NIKDY nepoužívejte holé `except`. Pak ošetříte i to, co nechcete, a váš kód nebude fungovat správně, a vy o tom nebudete mít ani ponětí.

Toho dosáhnete tím, že:

1. celý kód v metodě `receive_payload` obalíte do bloku `try`.
2. k němu přidáte `except Exception as e:`, který zachytí jakoukoli chybu, ať už vyvolanou vámi nebo kódem implicitně.
3. Uvnitř bloku `except` zkontrolujete, jestli je zapnutý firewall. Pokud ano, vyhodíte `SecurityError`. Pokud ne, vyhodíte tu chybu, kterou byste vyhodili bez zapnutého firewallu.

## BONUS: Bezpečné odpojení (Blok Finally)

V bloku `try-except` existuje ještě třetí, velmi mocné slovo: `finally`. Kód uvnitř `finally` se provede **VŽDY**, bez ohledu na to, zda v bloku `try` nastala chyba, nebo kód doběhl úspěšně. Slouží k takzvanému "úklidu" – například k uzavření souboru, uvolnění paměti nebo odpojení od sítě. Hacker nesmí nechat otevřená zadní vrátka, když jeho útok selže, a server naopak nesmí nechat viset spojení, když spadne!

*4.0 - 4.1*\
Upravte konstruktor (`__init__`) vaší třídy `Server` a přidejte mu nový atribut `self.is_connected = False`.

Napište do třídy `Server` novou metodu `execute_command(self, command: str) -> None`. V této metodě udělejte následující:
1. Nastavte `self.is_connected = True` (simulace otevření citlivého spojení do databáze).
2. Otevřete blok `try`. Pokud je příkaz (`command`) roven slovu `"CRASH"`, simulujte fatální selhání serveru tím, že vyhodíte `SystemError()`.
3. Nepoužívejte `except` (nechceme chybu chytat, chceme, aby systém opravdu spadl a chyba proletěla ven, aby si jí všiml administrátor). 
4. Namísto toho přidejte blok `finally`, ve kterém **vždy** (ať už systém spadl, nebo příkaz proběhl v pořádku) nastavíte `self.is_connected = False`, abyste bezpečně ukončili spojení.

---

Povolené moduly v dnešní lekci:

* collections (default)
* datetime (default)
* math (default)
* random (default)
* time (default)
* typing (default)
