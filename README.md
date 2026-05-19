# Python Intermediate - Lekce 07: Kreativní okénko

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

### 1. Vaše vlastní šifrování
Programování není jen o dodržování postupu. Občas je potřeba ten postup vymyslet. Proto bude vaším dnešním úkolem implementovat funkci `my_encrypt(plaintext: str, key: int) -> str`, která přijme řetězec a "zašifruje" ho a nový "zašifrovaný" řetězec vrátí.

Slovo "zašifrovaný" je v uvozovkách schválně. Neočekávám, že implementujete šifrování odpovídající kryptografickým standardům - to by bylo nejspíš nemožné.

Můžete k "zašifrování" využít prakticky jakoukoliv operaci, ale nezapomeňte, že musí jít i dešifrovat. Jako klíč k šifrování můžete využít parametr `key` buď přímo jako číselnou hodnotu, nebo jako semínko náhodného generátoru pro generování klíče. Klíč bude při testech náhodně zvolen z rozsahu `0 - 4294967295`. Obyčejný `int` se může zdát limitující, ale pomocí knihovny `random` z něj můžete vytvořit například řetězec či seznam booleanů. Fantazii se meze nekladou.

Můžete se spolehnout na to, že během testů budou použita jen malá písmena anglické abecedy a mezery.

> 💡 *Pro inspiraci, můžete využít klasického posunu písmen o identické číslo pro všechna písmena (Caesarova šifra), nabo posouvání každého písmena o různý počet kroků (Vigenérova šifra), můžete taky vygenerovat klíč identicky dlouhý se šifrovaným textem (Vernamova šifra), měřit vzdálenost mezi písmeny (C - A = 2) a podobně...*

### 2. A nyní dešifrování
Implementujte funkci `my_decrypt(ciphertext: str, key: int) -> str`, která vrátí "dešifrovaný" řetězec.

### 3. Co takhle zašifrovat soubor?
Implementujte funkci `my_encrypt_file(filename: str, key: int) -> None`, která přečte soubor `filename` a zašifruje jeho obsah do nového souboru, který vytvoří. Nový soubor bude mít příponu `.enc`.

> 💡 *Není třeba, abyste implementovali celou metodu šifrování znovu, využijte funkcí, které máte již hotové. Nezapomeňte na encoding.*

### 4. A nakonec dešifrování souboru
Implementujte funkci `my_decrypt_file(filename: str, key: int) -> None`, která přečte soubor `filename.enc` (příponu `.enc` musíte dodat sami) a dešifruje jeho obsah do souboru `filename` (bez `.enc`).

## 🌟 BONUS
V rámci bonusu se vám otevřou další tři testy, které ověří, jestli je vaše šifra dostatečně silná. (Tohle je čistě bonusová část, kterou nemusíte dělat, neboť jsem vám na začátku cvičení slíbil, že vaše šifra nemusí být tolik silná. V rámci procvičení je to ale cenná zkušenost.)

Testy budou zkoumat tři vlastnosti šifrovacích algoritmů:
- Nejprve **LAVINOVÝ EFEKT**. To znamená, že pokud se změní ve výchozím textu jediné písmenko, měla by se změna projevit i ve zbytku textu, nikoliv jen na tom jednom písmenku. Je to velmi cenná vlastnost šifrovacích algoritmů, která výrazně ztěžuje násilné prolomení zašifrovaných dat. Můžete spoléhat na to, že změněné písmeno v textu bude na začátku, nemusíte tedy zpětně iterovat podruhé od konce.
- Dále **ODOLNOST PROTI FREKVENČNÍ ANALÝZE**. Tato vlastnost je poměrně přímočará. Zajišťuje, aby byla distribuce znaků v zašifrovaném textu cca rovnoměrná, aby nešla přímo vypozorovat jednotlivá písmena.
- A nakonec **ÚNIK METAINFORMACÍ**. Nesnažíte se zašifrovat jen samotný text, ale i jeho podobu. Únik nechtěnných informací může vést k dešifrování celého vašeho textu. Proto je vhodné nezměnit jen písmenka, ale rovněž zajistit, aby nešlo například vyčíst, jak je zpráva dlouhá, kolik má slov a kolik mají jednotlivá slova písmen, apod. Tento test kontroluje jen a pouze to, zdali byly šifrováním zastřeny pozice mezer a tudíž délky slov.

> *Jak byste implementovali vlastnost, která by znamenala, že by nešla vyčíst délka zprávy?*


---
**📦 Povolené moduly v dnešní lekci:**
* `difflib`
* `collections` *(default)* 
* `datetime` *(default)*
* `math` *(default)*
* `random` *(default)*
* `time` *(default)*
* `typing` *(default)*
