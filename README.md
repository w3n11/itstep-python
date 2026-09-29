# Python Advanced - Lekce 01: Úvod do OOP

<details>
<summary>

#### Úvodní informace

</summary>

## Struktura adresáře

Budou vás zajímat jen tři soubory:

* `README.md` – Tento soubor, který právě čtete. Obsahuje zadání lekce.
* `assignment.py` – Soubor, do kterého budete **psát svůj kód a řešení**.
* `run.py` – Testovací motor. Tento soubor neupravujte, slouží k automatickému hodnocení vaší práce.

---

## Jak fungují testy?

Váš postup v hodině nebudu kontrolovat jen já, ale pomůže nám v tom automatizovaný systém. Strávil jsem nemalé úsilí napsáním testovacího frameworku, který bude okamžitě hodnotit, jak zdárně jste úlohy naprogramovali. 

Testy spustíte v terminálu příkazem (musíte se nacházet ve složce s projektem):
`python run.py`

Až testy spustíte, vypíše se vám přehledná tabulka toho, co už funguje `[PASS]`, a co ještě ne `[FAIL]`. **Vaším ultimátním cílem je do konce hodiny dokončit lekci na 100 %.**

> [!TIP]
> Absolutně v žádném případě nemusíte upadat do depresí, pokud na vás výsledky testů budou ze začátku křičet žlutě a červeně. Programování je o dělání chyb a jejich opravování. Testy vám vždy napoví, kde je problém. Pokud si nebudete ani tak vědět rady, jsem tu od toho, abych vám pomohl.

---

## Pravidla

Aby testy vůbec prošly a uznaly vám řešení, **musíte** dodržovat následující pravidla. Pokud je porušíte, systém vás k testům ani nepustí:

1. **AI nástroje (ChatGPT, Claude, Copilot atd.):** Můžete používat na hledání chyb v kódu a jejich opravování, jako brainstorming, když vám zrovna vaše představivost a kreativita stávkují, nebo pro psaní nudných částí kódu, které jste psali už tisíckrát. Nepoužívejte AI, aby to "prostě napsala za vás." Musíte mi být schopni váš kód vysvětlit.
2. **Přísný seznam povolených modulů:** Můžete používat (importovat) pouze moduly, které jsou explicitně povolené na konci tohoto zadání. Jakýkoliv jiný `import` systém zablokuje.
3. **Žádné hackování:** Není přísně zakázáno pokoušet se pomocí kódu upravovat testovací soubor `run.py`, ale pokud vám něco v důsledku toho nebude fungovat, nebudu vám moct pomoci s opravou. Využívat kód ke škodlivým účelům je pak zakázáno.
4. **Čistota kódu:** Nepoužívejte globální proměnné. Obecně jsou považovány za nežádoucí a programátoři se jim vždy snaží vyhnout. Až bude váš kód funkční, můžete se zaměřit na doladění vašeho kódu dle standardu PEP8.
5. **Spustitelnost:** Kód nesmí obsahovat hrubé syntaktické chyby, s nimi nelze program spustit.

> [!IMPORTANT]
> *Pokud se domníváte, že váš kód splňuje všechna pravidla, a systém vás přesto odmítá pustit dál, zavolejte mě.*

</details>

<details>
<summary>

#### Jak zprovoznit testy

</summary>

Krok 1: Instalace Pythonu

Pokud ještě nemáte nainstalovaný Python, musíte jej nejprve nainstalovat:

    Windows (bez administrátorských práv): Otevřete aplikaci Microsoft Store, vyhledejte „Python 3.14“ a klikněte na Instalovat (Install/Get).

    Mac/Ostatní: Přejděte na python.org/downloads a nainstalujte si nejnovější verzi.

Krok 2: Otevření projektu ve VS Code

    Stáhněte si složku s tímto projektem a rozbalte ji (pokud je v ZIP archivu).

    Otevřete editor VS Code.

    V horním menu přejděte na File > Open Folder... (Soubor > Otevřít složku...) a vyberte složku s tímto projektem.

    Pokud se zobrazí varování „Do you trust the authors of the files in this folder?“, klikněte na modré tlačítko Yes, I trust the authors (Ano, důvěřuji autorům).

Krok 3: Automatické nastavení ve VS Code

    Sledujte pravý dolní roh obrazovky. Pokud vás VS Code vyzve k instalaci doporučených rozšíření (např. Python extension), klikněte na Install.

    Ve spodní části obrazovky se automaticky otevře terminál, který pro vás začne na pozadí vytvářet bezpečné virtuální prostředí (.venv). Nechte tento proces doběhnout do konce.

    Pojistka: Pokud na vás vyskočí okno s dotazem „A requirements.txt file was found. Would you like to create a virtual environment?“, klikněte na Yes a následně vyberte Venv.

Krok 4: Spuštění kódu

Do terminálu nic ručně nevypisujte. Pro spolehlivé a bezpečné spuštění kódu:

    V levém panelu (Průzkumník) klikněte na soubor run.py, aby se otevřel.

    Klikněte na tlačítko Přehrát (▶) v pravém horním rohu okna.

    Nebo jednoduše stiskněte klávesu F5, čímž se kód rovnou spustí.

</details>

---

## Zadání úloh

Své řešení pište do souboru `assignment.py`.

### I. Třída Human
*1.0 - 1.2*<br>
Implementujte třídu `Human`, která bude obsahovat následující atributy:
- `name: str` - jméno osoby

Její **inicializační** metoda `__init__` bude kromě samozřejmého `self` příjimat i parametr `name`.
> [!NOTE]
> Pojmenování třídy předchází slůvko `class` stejně, jako předchází funkci slovo `def`.
>
> Nezapomeňte na klíčové slovo `self`, které způsobí, že z proměnné vytvoříte atribut. Např. `self.name = name`.

<details>
<summary>Řešení</summary>

```python
class Human:
    def __init__(self, name):
        self.name = name
```
</details>

---

### II. Výchozí hodnota
*1.3*<br>
Někdy nechceme, nebo třeba nemůžeme vypisovat všechny jednotlivé atributy a ty, které se nezvládnou odvodit nebo dopočítat samy, potřebují nějakou výchozí hodnotu. Výchozí jméno pro člověka bude `John Doe`.

Toho lze docílit snadno, ne?
```python
class Human:
    def __init__(self):
        self.name = "John Doe"
```

Takhle se každý člověk bude jmenovat John Doe. A jeho jméno bych mohl měnit až posléze pomocí `Human().name = "Dvoukvítek"`. Ale co když bych chtěl mít tu **možnost**, nastavit si jméno podle sebe už při vytváření člověka? To přece není nic obtížného...

<details>
<summary>Řešení</summary>

```python
class Human:
    def __init__(self, name="John Doe"):
        self.name = name
```
</details>

---

### III. Speciální metody
*1.4*<br>
Pomocí specilních metod jsme schopni upravit chování objektu/třídy v různých situacích. Pro hlubší zkoumání doporučuji [tento odkaz](https://docs.python.org/3/reference/datamodel.html#special-method-names). Nám dnes postačí pouze změnit chování metody `__str__`, která se na objektu volá například při vložení objektu jako parametru do funkce `print()`, nebo při použití v f-stringu: `f"This is a string representation of my object: {my_object}"`

Hlavním cílem metody `__str__` je, aby byla čitelná pro člověka. Funkce samotná nic nevypisuje, vždy jen **vrací** `str`. Vaším úkolem je teď naprogramovat tuto metodu tak, aby vracela jméno dané osoby a nic víc.

<details>
<summary>Řešení</summary>

```python
    def __str__(self):
        return self.name
```
</details>

---

### IV. Druhá třída? Magie?
*2.0 - 2.3*<br>
Ne, tak docela to magie není, ale umožňuje to dělat pomocí kódu spoustu zajímavých věcí, které bychom bez tříd simulovali jen obtížně.

Vytvořte třídu `Car` s těmito atributy:
- `brand: str` - značka auta
- `seats: int` - počet míst v autě (výchozí hodnota: `5`)
- `passengers: list[Human | None]` - obsazení jednotlivých míst, seznam dlouhý přesně jako počet míst
  - pokud je na daném indexu `None`, místo je volné
  - pokud je na daném indexu objekt třídy `Human`, místo je tímto obsazené a nikdo jiný si tam sednout nemůže

> [!NOTE]
> Všimněte si, že typ atributu `passengers` je `list[Human | None]`. To napovídá vám i linteru, co v něm má očekávat.

<details>
<summary>Řešení</summary>

```python
class Car:
    def __init__(self, brand, seats=5):
        self.brand = brand
        self.seats = seats
        self.passengers = [None] * self.seats
```
</details>

---

## V. Nastupovat!
*2.4 - 2.5*<br>
Tak... Teď máme člověka i auto. Teď naprogramujeme možnost, aby si člověk sedl.

Implementujte metodu `add_passenger(self, name: str)` do třídy `Car`, která přijme jméno osoby, která si chce sednout a posadí ji na první volné místo.

Metoda vrátí `True` pokud si osoba sednula do auta, jinak `False`.

> [!NOTE]
> Parametr `name` je typu `str`, ale náš atribut `passengers` je typu `list[Human | None]`. To znamená, že budete muset nejdříve objekt třídy `Human` inicializovat s pomocí daného jména.

<details>
<summary>Řešení</summary>

```python
    def add_passenger(self, passenger_name):
        for i in range(len(self.passengers)):
            if self.passengers[i] is None:
                self.passengers[i] = Human(passenger_name)
                return True
        return False
```
</details>

---

## VI. Vybíraví pasažéři.
Možná jste někdy chtěli sedět u okýnka. Nebo uprostřed, nebo na místě spolujezdce. Proč tuto možnost nenabídnout i našim pasažérům?

Přidejte volitelný parametr typu `int` (index) metodě `add_passenger`, který specifikuje, na které místo si chce daná osoba sednout.

Opět, pokud místo není volné, vraťte `False`. Pokud se pasažér pokusil sednout si mimo dostupná místa, rovněž vraťte `False`. Pokud se podařilo pasažérovi posadit, vraťte `True`.

> [!NOTE]
> První místo má index roven `0`, poslední místo má index roven `<počet míst> - 1`.

<details>
<summary>Řešení</summary>

```python
    def add_passenger(self, passenger_name, seat = None):
        if seat is None:
            for i in range(len(self.passengers)):
                if self.passengers[i] is None:
                    self.passengers[i] = Human(passenger_name)
                    return True
            return False

        try:
            if self.passengers[seat] is None:
                self.passengers[seat] = Human(passenger_name)
                return True
            return False
        except IndexError:
            return False
```
</details>

---

## BONUS

Přidejte výpis do stringu. Když se nějaká proměnná převádí na `str` (řetězec), volá se její interní metoda `__str__`, která přijímá pouze parametr `self`.

Přidejte takovou proměnnou, která bude vypisovat následujícím způsobem:

Pro auto značky **BMW** o obsazených třech místech ze čtyř.
```
BMW
  - Mrakoplaš
  - Dvoukvítek
  - Lasička
  - (empty seat)
```
Pro auto značky **Lamborghini** o obsazených dvou místech ze dvou.
```
Lamborghini
  - Mrakoplaš
  - Dvoukvítek
```
Pro auto značky **Mazda**, ve kterém nesedí žádný pasažér.
```
Mazda
  (the car is empty)
```

> [!IMPORTANT]
> Je třeba dodržet správný počet mezer.

---
**📦 Povolené moduly v dnešní lekci:**
* `collections` *(default)* 
* `datetime` *(default)*
* `math` *(default)*
* `random` *(default)*
* `time` *(default)*
* `typing` *(default)*
