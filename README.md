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
# Otevřeme soubor v módu pro zápis ("w") a pojmenujeme si ho 'file'
with open("hello_world.txt", "w", encoding="utf-8") as file:
    # Vše, co je odsazené, se děje se souborem
    file.write("Hello world")
    
# Jakmile odsazení skončí, Python soubor sám zavře a bezpečně uloží!
```
Jakmile se odskočí zpět na úroveň klíčového slova `with`, Python soubor zavře.

### 2. Cenzurování výstupu
Implementujte funkci, `censor_print(to_print, censored_words)`, která vypíše řetězec `to_print: str`, ale ještě před vypsáním v něm nahradí slova z `censored_words: list[str]` červenými hvězdičkami. Počet hvězdiček by měl odpovídat počtu písmen v jednotlivých nahrazovaných slovech. Funkce vrátí počet takto nahrazených slov.

Požadované chování:
```py
print(censor_print("Hello world", ["Hell"]))
```
Výstup:<br>
<code>
<span style="color: red">****</span>o world<br>1
</code>
___
Budete k tomu potřebovat funkce `string.replace(old, new)` a `string.count(substr)`. Funkce `replace` nahradí ve stringu všechny výskyty `old` za `new`. Funkce `count` zase vrátí počet výskytů `substr` ve stringu.

Příklad použití funkcí:
```py
my_string = "Hello world"
print(my_string.count("l"))  # 3
print(my_string.count("Hello"))  # 1

my_string = my_string.replace("Hell", "Heaven")
print(my_string)  # Heaveno world

print(my_string.count("l"))  # 1
print(my_string.count("Hello"))  # 0
```

### 3. QR kód
Implementujte funkci `print_qr(data: str)`, která vypíše do terminálu QR kód. Na vstupu dostanete data QR kódu v argumentu `data`. Ten sestává z jedniček a nul (`00010100101001110111010110...`) Tato data reprezentují QR kód.

Vaím úkolem bude tato data reprezentovat v bílých (`0`) a černých (`1`) pixelech. Zamyslete se nad tím, jak určíte velikost QR kódu.

Chcete-li, můžete si ze souboru `tests.py` vykopírovat funkci `make_qrcode()` a testovat si sami.

### 4. Volné zadání
Naprogramujte sami nějaký kraťoučký projekt, klidně jednu zajímavou či užitečnou funkci, která využívá knihovnu `colorama`.

Nemáte-li nápad, naprogramujte funkci, která vypíše na červeném podkladu bílé písmeno X o zadané velikosti.
![md_resources/cross.png](md_resources/cross.png)

---
**📦 Povolené moduly v dnešní lekci:**
* `colorama`
* `qrcode`
* `collections` *(default)* 
* `datetime` *(default)*
* `math` *(default)*
* `random` *(default)*
* `time` *(default)*
* `typing` *(default)*
