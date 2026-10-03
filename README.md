# Python Advanced - Lekce 02: Dědičnost

## Zadání úloh

Své řešení pište do souboru `assignment.py`.

### I. Co takhle autobus?

*1.0 - 1.2*\
Implementujte třídu `Bus`, která bude obsahovat následující atributy:

* `seats: int` - počet míst
* `passengers: list[Human | None]` - obsazená místa

> Pojmenování třídy předchází slůvko `class` stejně, jako předchází funkci slovo `def`.
> Nezapomeňte na klíčové slovo `self`, které způsobí, že z proměnné vytvoříte atribut. Např. `self.name = name`.

Klikni *[zde](solutions/task_1.py)* pro řešení.

---

### II. Nejsou ty dvě třídy stejné?

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
