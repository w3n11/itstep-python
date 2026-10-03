# Python Advanced - Lekce 02: Dědičnost

## Zadání úloh

Své řešení pište do souboru `assignment.py`.

### I. Co takhle autobus?

*1.0 - 1.2*\
Implementujte třídu `Bus`, která bude obsahovat následující atributy:

* `brand: str` - značka autobusu
* `seats: int` - počet míst
* `passengers: list[Human | None]` - obsazená místa

Zkopírujte logiku inicializace a metody `add_passenger` ze třídy `Car`. 
> Všimněte si, že je třída `Bus` velmi podobná (respektive úplně stejná) jako třída `Car`. Zkopírovat to bylo sice rychlé, ale co kdybychom teď chtěli upravit to, jak cestující nastupují? Museli bychom to měnit na dvou místech. Pojďme to vylepšit.

---

### II. Nejsou ty dvě třídy stejné? (Protože jsou.)

*2.0* **Nadtřída `Vehicle`**\
Vytvořte obecnou rodičovskou třídu `Vehicle`. Přesuňte do její metody `__init__` veškerou inicializaci atributů `brand`, `seats` a vytváření pole `passengers`. Pozor, třída `Vehicle` nemá žádné výchozí počty míst (neočekává ani 5, ani 40, počet jí musí být vždy explicitně předán).

*2.1 - 2.2* **Dědičnost**\
Upravte třídy `Car` a `Bus` tak, aby dědily ze třídy `Vehicle`.
V jejich metodách `__init__` odstraňte vytváření atributů (`self.brand = ...` atd.) a místo toho využijte volání rodičovského konstruktoru pomocí funkce `super()`.
Nápověda: Auto i autobus si stále musí zachovat své výchozí počty míst v parametrech svého `__init__`.

*2.3 - 2.5* **Deduplikace kódu**\
Přesuňte metody `add_passenger` a `__str__` z tříd `Car` a `Bus` výše, přímo do třídy `Vehicle`.
Smažte je z potomků. Zkontrolujte (třeba vlastním testem na konci souboru), že vaše auto i autobus stále fungují a umí přidávat pasažéry, i když teď tyto metody "jen" dědí.

---

### III. Kdo vlastně jezdí v autě?

Zatím naše vozidla vozí jen lidi (`Human`). Co když ale budeme chtít převézt psa? Náš stávající kód `self.passengers[i] = Human(passenger_name)` je hodně svazující, protože natvrdo vytváří lidi. Pojďme kód upravit tak, aby přijímal kohokoliv, kdo je "Cestující".

*3.0* **Polymorfismus**\
Vytvořte novou třídu `Passenger`. Přesuňte do ní metodu `__init__` (která nastavuje `self.name`) a metodu `__str__` ze třídy `Human`.

*3.1* **`Human` a `Dog`**\
Upravte třídu `Human` tak, aby dědila z `Passenger`. Smažte z ní všechny metody (tělo třídy bude obsahovat jen klíčové slovo `pass`).
Vytvořte novou třídu `Dog`, která bude také dědit z `Passenger` a bude také prázdná.
(O výpisy jmen s názvem třídy v závorce se díky dědičnosti postará metoda `__str__` v rodiči).

*3.2* **Chytřejší `add_passenger`**\
Upravte metodu `add_passenger` ve třídě `Vehicle`. Místo aby v parametrech přijímala `passenger_name: str` a sama si z něj vytvářela objekt, bude nově přijímat už hotový objekt typu `Passenger`.\
Upravte podle toho kód uvnitř metody (už nebudete volat `Human(...)`, ale rovnou uložíte přijatý objekt do pole) a nezapomeňte upravit i datové typy u samotného pole passengers.

---

### IV. Co umí autobus navíc? (Rozšiřování potomků)

Dědičnost neslouží jen ke sdílení stejného kódu, ale i k tomu, aby se potomci mohli lišit. Autobusy (na rozdíl od aut) vybírají od cestujících peníze.

*4.0* **Lístky na autobus**\
Přidejte třídě `Bus` do `__init__` nový volitelný parametr `ticket_price: int = 20`. Vytvořte z něj nový atribut třídy.

*4.1* **Výběr jízdného**\
Vytvořte pouze pro třídu `Bus` novou metodu `collect_fares(self) -> int`. Metoda projde všechny aktuálně sedící pasažéry v autobuse (pozor na prázdná místa `None`) a vrátí celkovou částku, kterou autobus vybral na jízdném.

---

## BONUS

Přidejte do autobusu metodu `board_group(self, group: list[Passenger]) -> int`, která přijme seznam čekajících pasažérů. Metoda se pokusí posadit co nejvíce z nich na první volná sedadla v autobuse. Metoda vrátí číslo udávající, kolik pasažérů se do autobusu nevešlo (kapacita byla vyčerpána). Pokud si sedli všichni, vrátí `0`.

---
**Povolené moduly v dnešní lekci:**
* `collections` *(default)* 
* `datetime` *(default)*
* `math` *(default)*
* `random` *(default)*
* `time` *(default)*
* `typing` *(default)*
