"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie - Elections scraper
author: Marek Sýkora
email: MarekSykora78@seznam.cz
discord: Wassenego#1875
"""

import sys
import csv

import requests
import bs4

# vytvoření slovníku, ve kterém jsou čísla krajů jako klíče a k nim přiřazeny číselné hodnoty okresů
district_codes = {  "1":("1100",),
                    "2":("2101", "2102", "2103", "2104", "2105", "2106", "2107", "2108", "2109", "2110", "2111", "2112"),
                    "3":("3101", "3102", "3103", "3104", "3105", "3106", "3107"),
                    "4":("3201", "3202", "3203", "3204", "3205", "3206", "3207"),
                    "5":("4101", "4102", "4103"),
                    "6":("4201", "4202", "4203", "4204", "4205", "4206" , "4207"),
                    "7":("5101", "5102", "5103", "5104"),
                    "8":("5201", "5202", "5203", "5204", "5205"),
                    "9":("5301", "5302", "6303", "5304"),
                    "10":("6101", "6102", "6103", "6104", "6105"),
                    "11":("6201", "6202", "6203", "6204", "6205", "6206", "6207"),
                    "12":("7101", "7102", "7103", "7104", "7105"),
                    "13":("7201", "7202", "7203", "7204"),
                    "14":("8101", "8102", "8103", "8104", "8105", "8106")}

def slice_url_address(arg1):
    """
    Rozděl vložený argument na indexu 1 na jednotlivé části, aby šly porovnat, a vlož je do seznamu.
    """
    opening = arg1[:52]
    center = arg1[-14:-4]
    district_number = arg1[-4:]
    region_number = arg1[52:][:-14]
    sliced_address = [opening, region_number, center, district_number]
    return sliced_address

def verify_url_address(address: list) -> bool:
    """
    Zkontroluj seznam, zda vyhovuje všem podmínkám pro správnou url adresu
    """
    if not address[0] == "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=":
        return False
    elif not address[2] == "&xnumnuts=":
        return False
    elif not address[1] in district_codes.keys():
        return False
    elif not address[3] in district_codes[address[1]]:
        return False
    else:
        return True

def send_get_demand(url: str) -> str:
    """
    Vrať odpověd serveru na požadavek typu GET.
    """
    response = requests.get(url)
    return response.text

def get_pars_answer(response: str) -> bs4.BeautifulSoup:
    """
    Získej rozdělenou odpověď na požadavek typu GET.
    """
    return bs4.BeautifulSoup(response, features="html.parser")

def get_td_tags_names(server_response: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    """
    Ze zdrojového kódu stránky vyber všechny tagy "td" s atributem "class": "overflow_name".
    """
    return server_response.find_all("td", {"class": "overflow_name"})

def get_td_tags_codes(server_response: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    """
    Ze zdrojového kódu stránky vyber všechny tagy "td" s atributem "class": "cislo" - Kódy obcí.
    """
    return server_response.find_all("td", {"class": "cislo"})

def get_td_tags_votes(server_response: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    """
    Ze zdrojového kódu stránky vyber tag "td" s atributem "headers": "t1sa2 t1sb3" a "t2sa2 t2sb3" - Platné hlasy - celkem.
    """
    return server_response.find_all("td", {"headers": "t1sa2 t1sb3"}) + server_response.find_all("td", {"headers": "t2sa2 t2sb3"})

def get_td_tag_registered(server_response: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    """
    Ze zdrojového kódu stránky vyber tag "td" s atributem "headers": "sa2" - Voliči v seznamu.
    """
    return server_response.find("td", {"headers": "sa2"}).get_text()

def get_td_tag_envelopes(server_response: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    """
    Ze zdrojového kódu stránky vyber tag "td" s atributem "headers": "sa5" - Odevzdané obálky.
    """
    return server_response.find("td", {"headers": "sa5"}).get_text()

def get_td_tag_valid(server_response: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    """
    Ze zdrojového kódu stránky vyber tag "td" s atributem "headers": "sa6" - Platné hlasy.
    """
    return server_response.find("td", {"headers": "sa6"}).get_text()

def get_municipality_names(tds: bs4.element.ResultSet) -> list:
    """
    Ze zdrojového kódu stránky vyber všechny jména obcí
    """
    names = [name.text for name in tds]
    return names

def get_municipality_codes(tds: bs4.element.ResultSet) -> list:
    """
    Ze zdrojového kódu stránky vyber všechny kódy obcí
    """
    codes = [code.text for code in tds]
    return codes

def get_parties_names(tds: bs4.element.ResultSet) -> list:
    """
    Ze zdrojového kódu stránky vyber všechny jména politických stran
    """
    parties = [party.text for party in tds]
    return parties

def get_votes(tds: bs4.element.ResultSet) -> list:
    """
    Ze zdrojového kódu stránky vyber platné hlasy jednotlivých stran
    """
    votes = [vote.text for vote in tds]
    return votes[:25]

def make_municipality_url(url: str, numbers: list) -> list:
    """
    Vytvoř seznam url adres pro všechny obce ve vybraném okrese
    """
    return [url.replace("ps32?", "ps311?").replace("numnuts",f"obec={code}&xvyber") for code in numbers]

def control_arguments(args):
    """
    Zkontroluj zadané argumenty vepsané do příkazové řádky
    """   
    if len(sys.argv) != 3:
        print(f"PRO SPUSTENI SOUBORU POTREBUJETE DVA POVINNE ARGUMENTY: 'ODKAZ UZEMNIHO CELKU' A 'JMENO VYSLEDNEHO SOUBORU S PRIPONOU .csv'")
        sys.exit(1)
    elif verify_url_address(slice_url_address(sys.argv[1])) == False:
        print(f"ADRESA {sys.argv[1]} NEMA SPRAVNY TVAR NEBO NEODKAZUJE NA SPRAVNE STRANKY!")
        sys.exit(1)
    elif not sys.argv[2].endswith(".csv"):
        print(f"SOUBOR '{sys.argv[2]}' NEMA POZADOVANY TVAR!")
        sys.exit(1)
    else:
        print(f"STAHUJI DATA Z VYBRANEHO URL: {sys.argv[1]}")

def write_to_file(file_name: str, first_row: list, rows: list) -> None:
    """
    Vypiš stažená data do souboru
    """ 
    with open(file_name, mode="w", newline="") as new_csv:
        writer_tool = csv.writer(new_csv, delimiter=";")
        writer_tool.writerow(first_row)
        writer_tool.writerows(rows)

if __name__ == "__main__":
    control_arguments(sys.argv)

    # vytvoření dílčích seznamů z různých stránek na webu
    demand1 = send_get_demand(sys.argv[1])
    answer = get_pars_answer(demand1)
    names = get_td_tags_names(answer)
    codes = get_td_tags_codes(answer)
    municipality_names = get_municipality_names(names)
    municipality_codes = get_municipality_codes(codes)
    municipality_urls = make_municipality_url(sys.argv[1], municipality_codes)
    demand2 = send_get_demand(municipality_urls[0])
    answers = get_pars_answer(demand2)
    td = get_td_tags_names(answers)
    parties_names = get_parties_names(td)

    registered = [get_td_tag_registered(get_pars_answer(send_get_demand(url))) for url in municipality_urls]
    envelopes = [get_td_tag_envelopes(get_pars_answer(send_get_demand(url))) for url in municipality_urls]
    valid = [get_td_tag_valid(get_pars_answer(send_get_demand(url))) for url in municipality_urls]

    parties_votes = [get_votes(get_td_tags_votes(get_pars_answer(send_get_demand(url)))) for url in municipality_urls]

    # vytvoření hlavičky
    header = ["code", "location", "registered", "envelopes", "valid"] + parties_names

    # vytvoření seznamu se seznamy výsledků jednotlivých obcí
    data = []
    for i in range(len(municipality_codes)):
        row = []
        row.append(municipality_codes[i])
        row.append(municipality_names[i])
        row.append(registered[i])
        row.append(envelopes[i])
        row.append(valid[i])
        data.append(row + parties_votes[i])
      
    print(F"UKLADAM DO SOUBORU: {sys.argv[2]}")

    write_to_file(sys.argv[2], header, data)

    print(f"UKONCUJI PROGRAM.")
