# P_A_project_3_Elections_scraper
Python Academy project 3 - Elections scraper - závěrečný projekt na Python akademii od Engeta.

## Popis projektu
Tento projekt slouží k extrahování výsledků z parlamentních voleb 2017. Odkaz k prohlédnutí [zde](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).

## Instalace knihoven
Knihovny, které jsou použity v kódu, jsou uloženy v souboru `requirements.txt`. Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spusti následovně:
```python
$ pip3 --version                    # overim verzi manazeru
$ pip3 install -r requirements.txt  # nainstaluji knihovny
```
## Spuštění projektu
Spuštění projektu `main1.py` v rámci příkazového řádku potřebuje dva povinné argumenty.
```python
python main1.py <odkaz-uzemniho-celku> <vysledny-soubor>
```
Název výseldného souboru musí být zadán i spříponou `.csv`, ve kterém budou výsledky následně uloženy.

## Ukázka projektu
Výsledky hlasování pro okres Prostějov:
  1. argument: `https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103`
  2. argument: `vysledky_Prostejov.csv`
SPuštění programu:
```python
python main1.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_Prostejov.csv
```
Průběh stahování:
```python
STAHUJI DATA Z VYBRANEHO URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
UKLADAM DO SOUBORU: vysledky_Prostejov.csv
UKONCUJI PROGRAM.
```
Částečný výstup:
```
code;location;registered;envelopes;valid;
506761;Alojzov;205;145;144;29;0;0;9;0;5;17;4;1;1;0;0;18;0;5;32;0;0;6;0;0;1;1;15;0
589268;Bedihošť;834;527;524;51;0;0;28;1;13;123;2;2;14;1;0;34;0;6;140;0;0;26;0;0;0;0;82;1
```
