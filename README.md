# Python Intermediate - Lekce 05: Soubory

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
3. **Žádné hackování:** Je přísně zakázáno pokoušet se pomocí kódu upravovat testovací soubor `run.py`, obcházet testy nebo využívat kód ke škodlivým účelům.
4. **Čistota kódu:** Nepoužívejte globální proměnné. Obecně jsou považovány za nežádoucí a programátoři se jim vždy snaží vyhnout. Až bude váš kód funkční, můžete se zaměřit na doladění vašeho kódu dle standardu.
5. **Spustitelnost:** Kód nesmí obsahovat hrubé syntaktické chyby, s nimi nelze program spustit.

> *Pokud se domníváte, že váš kód splňuje všechna pravidla, a systém vás přesto odmítá pustit dál, zavolejte mě.*

---

## 🛠️ Zadání úloh

Svá řešení pište do souboru `assignment.py`.

### 1. Hello world v souboru
Implementujte funkci `hello_world_to_file()`, která zapíše do souboru `hello_world.txt` řetězec `Hello world`.

Práce se soubory je vcelku přímočará. Pomocí funkce `open()` získáte objekt souboru. Nutné jsou ale tři parametry:
- `file`
- `mode`
- `encoding`

`file` je cesta k souboru. Pokud budete chtít vytvořit soubor `hello_world.txt` ve stejném adresáři, stačí samotný název. Pokud jej budete chtít vytvořit v podsložce, musíte napsat `jmeno_slozky/hello_world.txt`.

Pomocí parametru `mode` říkáme operačnímu systému, jak nám má soubor otevřít, případně pomocí `b` navíc Pythonu, že budeme číst/zapisovat bajty. Máte šest základních možností:
- `"r"` - otevřít pro čtení v textovém režimu
- `"w"` - otevřít pro zápis v textovém režimu
- `"a"` - otevřít pro zápis na konec souboru v textovém režimu
- `"rb"` - otevřít pro čtení bajtů
- `"wb"` - otevřít pro zápis bajtů
- `"ab"` - otevřít pro zápis bajtů na konec souboru

Nakonec pomocí parametru `encoding` nastaveném na hodnotu `"utf-8"` zajistíme kompatibilitu souborů napříč systémy. Tato volba je nutná pouze v textovém režimu. Ona vlastně není ani tak nutná, ale silně doporučená.

> Je to proto, že počítače znají jen jedničky a nuly - v počítači je všechno vyjádřeno číslem. Proto existují kódování (endoding). Můžete si to představit jako takové "překladové slovníky" z čísel na znaky.

Jak na to v kódu? Pomocí nám nové konstrukce `with/as`:
```py
# Otevřeme soubor v módu pro zápis ("w") a uložíme do proměnné 'file'.
with open("hello_world.txt", "w", encoding="utf-8") as file:
    # Vše, co je odsazené, se děje se souborem
    file.write("Hello world")
    
# Jakmile odsazení skončí, Python soubor sám zavře a bezpečně uloží.
# Po skončení odsazení už neexistuje proměnná 'file'.
```
Jakmile se odskočí zpět na úroveň klíčového slova `with`, Python soubor zavře.

### 2. Čtení a číslování řádků

Implementujte funkci `read_and_order(filename: str) -> None`, která otevře soubor, jehož název dostane v parametru, a vypíše jeho obsah do terminálu tak, že každý řádek očísluje (od jedničky).

Příklad výstupu:
```pt
1. První řádek
2. Druhý řádek
3. Třetí řádek
```

💡 **Nápověda:** Soubor otevřete v režimu pro čtení (`"r"`). Abyste získali jednotlivé řádky, můžete načíst celý obsah pomocí `file.read()` a ten následně rozdělit do seznamu pomocí metody `.splitlines()`. Přes tento seznam pak můžete iterovat pomocí cyklu `for` a funkce `range()`.

### 3. Náhodná čísla do souboru

Implementujte funkci `random_numbers_to_file(count: int)`, která do souboru `random_numbers.txt` vygeneruje a zapíše zadaný počet (`count`) náhodných čísel od 1 do 100. Každé číslo bude na novém řádku.

💡 **Nápověda**: Co se stane, když funkci zavoláte dvakrát po sobě? V režimu `"w"` se existující soubor vždy promaže a přepíše. Pokud byste chtěli obsah přidávat na konec (režim `"a"` - append), musíte nejprve zajistit promazání souboru ze starého testu.

### 4. Unikátní náhodná čísla

Implementujte funkci `unique_random_numbers_to_file(count: int)`, která funguje velmi podobně jako předchozí úkol. Bude ale zapisovat do souboru `unique_random_numbers.txt` a čísla se nesmí opakovat.

💡 **Nápověda:**
Vytvořte si prázdný seznam pomocnou proměnnou, ve které si budete ukládat již vygenerovaná čísla. Při každém novém losování zkontrolujte, zda náhodou už nebylo použito. Pokud ano, losujte znovu. (Tohle je extrémně neefektivní implementace, ale cílem tohoto cvičení je procvičit si práci s pomocnou proměnnou.)
Aby se vám program nezacyklil v případě, že budete chtít vygenerovat 200 unikátních čísel z rozsahu 1-100, nastavte horní hranici losování dynamicky tak, aby nedošlo k zacyklení. (K zacyklení by došlo, kdybychom chtěli vygenerovat více než 100 čísel.)

## 🌟 Bonusové úlohy

Následující úlohy simulují reálný systém pro ukládání hesel. **NIKDY** však neukládejte reálná hesla v nešifrované podobě, jak je cílem v úlohách níže!

### B1. Přihlašovací systém (Login)

Implementujte funkci `simple_login(database: str = "accounts.txt") -> bool`.

Funkce se zeptá uživatele na uživatelské jméno (pomocí `input()`) a heslo. Pro bezpečné zadání hesla použijte funkci `getpass("Password: ")` z importovaného modulu `getpass` – díky tomu nepůjdou znaky při psaní do terminálu vidět.

Následně funkce otevře soubor database a ověří, zda v něm existuje odpovídající záznam.

- Soubor obsahuje na každém řádku záznam ve formátu `uživatelské_jméno;heslo`. (Pro rozdělení řádku použijte `line.split(";", 1)`).

- Pokud najdete shodu, vypište `Logged in.` a vraťte `True`.

- Pokud projdete celý soubor a shoda se nenajde, vypište `Invalid credentials.` a vraťte `False`.

### B2. Registrační systém (Register)

Implementujte funkci `simple_register(database: str = "accounts.txt") -> bool`.

Funkce požádá o `username` přes běžný input, a následně dvakrát o `password`  přes `getpass()`.

- Kontrola hesel: Pokud se obě zadaná hesla neshodují, vypište `Passwords do not match.` a vraťte `False`.

- Kontrola duplicity: Otevřete soubor pro čtení (`"r"`). Pokud již uživatelské jméno v databázi existuje, vypište `Username already exists.` a vraťte `False`.

- Zápis: Pokud je vše v pořádku, otevřete soubor pro přidávání (`"a"`) a na nový řádek zapište jméno a heslo oddělené středníkem (`jmeno;heslo\n`). Vypište `Account created.` a vraťte `True`.

---
**📦 Povolené moduly v dnešní lekci:**
* `getpass`
* `collections` *(default)* 
* `datetime` *(default)*
* `math` *(default)*
* `random` *(default)*
* `time` *(default)*
* `typing` *(default)*
