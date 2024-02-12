# Projekt - zadání 3. části

**Cílem této části projektu je vyzkoušet si využití webových stránek jako zdroje dat, konkrétně pro automatizované získání:**
* Odkazů (seznamu URL) z dynamických webových stránek
* Konkrétních informací z většího množství webových stránek

#### Pokyny k řešení:
1. Zvolte si vhodný e-shop nabízející libovolné produkty
    * Pokud možno zahraniční.
    * K produktům musí být uvedeny nějaké doplňující parametry (např. u telefonů model procesoru, velikost paměti, rozlišení fotoaparátu, u jízdních kol materiál rámu, hmotnost, apod.), ideálně ve formě tabulky.
    * Vyhněte se nejběžnějším e-shopům (alza.cz, amazon.com, apod.), snažte se svojí volbou minimalizovat šanci, že si jiný tým zvolí stejný e-shop. Nesdělujte volbu e-shopu mimo tým. Předejdete tím komplikacím způsobeným např. přílišným zatížením serverů e-shopu provozem z FIT (viz poznámky níže).
2. Implementujte program (skript), který automatizovaně získá **seznam URL alespoň 100 srovnatelných produktů** dostupných na e-shopu.
    * Ideální je např. zpracovat stránku nebo stránky věnované nějaké konkrétní kategorii produktů, které mají alespoň některé parametry společné pro více položek.
3. Implementujte program (skript), který bude mít na vstupu seznam URL produktů a pro každý takový produkt získá z příslušné cílové stránky **název produktu, aktuálně platnou cenu a hodnoty minimálně tří doplňujících parametrů**.
    * Parametry zvolte tak, aby byly společné pro většinu produktů na seznamu, ale uvažujte i situaci, že hodnota některých parametrů nebude u některého produktu uvedena.
    * Výstup skriptu bude mít formát TSV: na každém řádku URL produktu (pro identifikaci), název produktu, aktuální prodejní cenu a hodnoty jednotlivých parametrů oddělené tabulátory (znak TAB), minimálně tedy 6 sloupců, pro všechna URL ze seznamu. Názvy sloupců (záhlaví) nevypisujte, význam sloupců prosím zdokumentujte v README (viz níže).
    * Se všemi extrahovanými hodnotami zacházejte jako s řetězci a hodnoty ukládejte v podobě, v jaké jsou uvedeny (tzn. není třeba normalizovat jednotky, převádět na čísla apod.)

#### Způsob implementace:
* Řešení musí být **spustitelné na serveru merlin**. Pokud by tento server byl pro vaše záměry příliš omezující, je možné se individuálně domluvit na výjimkách v předstihu (do konce listopadu). Ověřte si předem, co je na serveru merlin k dispozici.
* Implementované programy vypisují svoje výsledky (seznam URL u prvního skriptu a tabulka parametrů u druhého skriptu) **na standardní výstup** (stdout). Uložení výsledku do souborů požadovaných níže se realizuje přesměrováním při spuštění z příkazové řádky.
* Můžete využít libovolnou implementační platformu (Python, JavaScript, Java, bash, ...), program ale musí běžet lokálně (na serveru merlin) a nesmí využívat online služby třetích stran.
* Využití libovolných volně dostupných knihoven (jako např. puppeteer, BeautifulSoup, apod.) je povoleno. Příklady vhodných knihoven budou uvedeny v rámci přednášek.
* Je možno zpracovávat jak HTML kód stránek, tak i vložená strukturovaná data (např. JSON-LD, RDFa, apod.), podle toho, co se bude zdát jednodušší.
* Oba skripty (bod 2 a 3 zadání) musí umožnit opakované spuštění, které dá výsledek odpovídající zadání. Tento výsledek ale může být pokaždé jiný (vyberou se jiné produkty, změní se cena, apod.)


#### Způsob odevzdání (požadované výstupy):
Výsledné řešení (jeden zip archiv) odevzdá pouze vedoucí týmu prostřednictvím IS VUT. Archiv bude obsahovat:
* Soubor `urls.txt` obsahující ukázkový výstup k bodu 2 zadání, na každém řádku 1 URL.
* Soubor `data.tsv` obsahující ukázkový výstup k bodu 3 zadání ve formátu TSV, min. 100 řádků.
* Implementaci obou programů.
Skript `build.sh`, který zajistí případný překlad, instalaci závislostí a další úkony tak, aby programy bylo možné spustit. Pokud žádná speciální příprava není nutná, bude tento skript prázdný.
* Testovací skript `run.sh`, který spustí skript pro získání seznamu URL produktů, uloží je do souboru `url_test.txt` a následně pro prvních 10 URL z tohoto seznamu spustí druhý skript, který získá informace o produktech a vypíše je na **standardní výstup** (stdout).
* Soubor `README`, který bude obsahovat
    * Název týmu a seznam řešitelů
    * URL a název e-shopu, který jste zvolili
    * Význam sloupců ve výstupu TSV
    * Případné poznámky, pouze pokud je k něčemu třeba speciální vysvětlení.
* **Neodevzdávejte knihovny třetích stran, přeložený kód, adresáře se závislostmi (node_modules apod.) ani další soubory, které je možno získat automaticky sestavením projektu.**

#### Poznámky:
Chovejte se ohleduplně k cizím serverům a nezatěžujte je velkým množstvím dotazů. Vyvíjejte a testujte na malém množství stránek, případně na lokálně uložených kopiích HTML dokumentů. Finální datovou sadu (100 produktů) není nutné získat naráz, můžete spuštění rozdělit např. čtvrtiny a spouštět s časovým odstupem.
