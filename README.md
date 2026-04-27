# Python Intermediate - Lekce 04: Barvičky

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

### 1. Barevné hello world
Implementujte funkci `hello_world_green()`, která pomocí knihovny `colorama` vypíše zeleně `Hello world`.

Při používání knihovny `colorama` můžete přímo ve funkci print používat takzvané `ANSI escape sekvence`. To jsou speciálně navržené skupiny znaků, které mění barvu pozadí a textu. Například `\033[31mČervená\033[0m` vypíše <span style="color: red">Červená</span>. Abyste ale nemuseli dohledávat kódy pro jednotlivé styly, `colorama` to řeší za vás.

Pro vypsání <span style="color: red">Červená</span> vám tak stačí jen
```py
1 | import colorama
2 |
3 | colorama.init(autoreset=True)
4 | print(colorama.Fore.RED + "Červená")
5 | 
6 | colorama.deinit()
```
Na řádku 1 importujeme knihovnu `colorama`, abychom ji mohli používat.

Na třetím řádku pak inicializujeme/spustíme překlad a vykonávání jednotlivých ANSI escape sekvencí. Argument `autoreset` pak slouží k tomu, abyste po každém zavolání nemuseli barvy resetovat, protože bez resetování by se vykreslovalo vše červeně až do další změny barvy.

Na čtvrtém řádku pak vypíšeme `Červená` spolu s "požadavkem" na červené popředí.

Na posledním řádku pak preventivně deinicializujeme/vypneme vykonávání ANSI escape sekvencí pro zamezení nežádoucích účinků. Obecně není tento krok potřeba, ale je dobrou praxí všechny alokované zdroje po ukončení práce uvolnit a pokud to nebylo záměrem, vrátit pracovní prostředí do původního stavu.

Kódy knihovny `colorama` se používají následovně:
- `colorama.Fore.KÓD_BARVY` mění barvu popředí, resp. písma (**FORE**ground)
- `colorama.Back.KÓD_BARVY` mění barvu pozadí (**BACK**ground)

Za `KÓD_BARVY` dosaďte jednu z následujících možností:
- <span style="color: red">RED</span>
- <span style="color: blue">BLUE</span>
- <span style="color: green">GREEN</span>
- <span style="color: yellow">YELLOW</span>
- <span style="color: cyan">CYAN</span>
- <span style="color: magenta">MAGENTA</span>
- <span style="color: white">WHITE</span>
- <span style="color: black">BLACK</span> (← BLACK)

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

Nemáte-li nápad, naprogramujte funkci, která 

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
