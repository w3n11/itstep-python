# Python Advanced - Lekce 02: Dědičnost

## Zadání úloh

Své řešení pište do souboru `assignment.py`.

### I. Kdo vlastně jezdí v autě? (Polymorfismus)

Zatím naše vozidla vozila jen lidi (`Human`). Co když ale budeme chtít převézt psa? Náš stávající kód je svazující, protože natvrdo vytváří pouze lidi. Pojďme kód upravit tak, aby přijímal kohokoliv, kdo je "Cestující".

**1.0 - 1.1 Třída Passenger**\
Vytvořte novou třídu `Passenger`. Přesuňte do ní metodu `__init__` (která nastavuje `self.name`) ze stávající třídy `Human`.
Napište nebo upravte metodu `__str__` tak, aby přesně vracela jméno a v závorce název aktuální třídy:

```python
def __str__(self) -> str:
    return self.name + f" ({self.__class__.__name__})"
```

**1.2 - 1.3 Human a Dog**\
Upravte třídu Human tak, aby dědila z Passenger. Smažte z ní všechny metody (tělo třídy bude obsahovat jen klíčové slovo pass).
Vytvořte novou třídu Dog, která bude také dědit z Passenger a bude rovněž prázdná.

### II. Nejsou ta vozidla nakonec stejná? (Nadtřída Vehicle)

Abychom mohli otestovat funkčnost aut i autobusů, potřebujeme mít společný základ.

**2.0 Nadtřída Vehicle**\
Vytvořte obecnou rodičovskou třídu `Vehicle`. Zkopírujte do její metody `__init__` veškerou inicializaci atributů `brand`, `seats` a vytváření pole `passengers`. Třída `Vehicle` nemá žádné výchozí počty míst (počet jí musí být vždy explicitně předán).
Přesuňte do ní také metodu `__str__` a `add_passenger`.

**Chytřejší `add_passenger`**

Místo aby metoda v parametrech přijímala `passenger_name: str` a sama si z něj vytvářela objekt, bude nově přijímat už hotový objekt typu `Passenger`.

Upravte kód uvnitř (už nebudete volat `Human(...)`, ale uložíte přímo přijatý objekt) a upravte datové typy u pole passengers na `list[Passenger | None]`.

### III. Dědičnost a deduplikace (Car a Bus)

**3.0 - 3.1 Dědičnost**\
Upravte třídu `Car` tak, aby dědila ze třídy `Vehicle`.
Vytvořte novou třídu `Bus`, která bude také dědit ze třídy `Vehicle`. Třída `Bus` bude mít výchozí počet míst (`seats`) nastavený na `40`.

**3.2 - 3.7 Deduplikace kódu a funkčnost**\
V metodách `__init__` tříd `Car` a `Bus` využijte volání rodičovského konstruktoru pomocí funkce `super()`. Odstraňte u potomků zbytečné vytváření atributů (`self.brand = ...` atd.), které už zařizuje rodič.\
Auto i autobus si samozřejmě stále musí zachovat své výchozí počty míst v parametrech svého `__init__`.

> Vaše auto i autobus by po těchto krocích měly normálně fungovat a usazovat nové objekty pasažérů.

### IV. Co umí autobus navíc? (Rozšiřování potomků)

Dědičnost neslouží jen ke sdílení stejného kódu, ale i k tomu, aby se potomci mohli lišit. Autobusy (na rozdíl od aut) vybírají od cestujících peníze.

**Lístky na autobus**\
Přidejte třídě `Bus` do `__init__` nový volitelný parametr `ticket_price: int = 20`. Vytvořte z něj nový atribut třídy.

**4.0 - 4.3 Výběr jízdného**\
Vytvořte pouze pro třídu `Bus` novou metodu `collect_fares(self) -> int`. Metoda projde všechny aktuálně sedící pasažéry v autobuse (pozor na prázdná místa `None`) a vrátí celkovou částku, kterou autobus vybral na jízdném.

## BONUS

Přidejte do autobusu metodu `board_group(self, group: list[Passenger]) -> int`, která přijme seznam čekajících pasažérů. Metoda se pokusí posadit co nejvíce z nich na první volná sedadla v autobuse. Metoda vrátí číslo udávající, kolik pasažérů se do autobusu nevešlo (kapacita byla vyčerpána). Pokud si sedli všichni, vrátí `0`.

---

Povolené moduly v dnešní lekci:

* collections (default)
* datetime (default)
* math (default)
* random (default)
* time (default)
* typing (default)
