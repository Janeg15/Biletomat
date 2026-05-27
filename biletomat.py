import json
import time
import os

# Stałe
PROMPT = "Twój wybór: "
ERROR_MSG = "Niepoprawny wybór, spróbuj ponownie."

# Funkcje pomocnicze
def display_menu():
    print("Wybierz jedną z opcji:\n1 - dodaj bilet\n2 - pokaż koszyk\n3 - zapłać\n4 - zakończ program")

def display_cart():
    if not cart:
        print("W koszyku nie ma jeszcze żadnych biletów.")
    else:
        print("Zawartość koszyka")
        print()
        print("Lp. |  Cena   | Bilet")
        for index, ticket in enumerate(cart):
            print(f"{index:3} | {ticket['price']:7.2f} zł | Bilet {ticket['discount']} {ticket['type']} {ticket['validity']}")
        print()
        print(get_cart_value())

def get_cart_value():
    return f"Wartość biletów w koszyku: {sum(ticket['price'] for ticket in cart):5.2f} zł."

def end_machine():
    print("Czy na pewno chcesz porzucić koszyk? (t - tak)")
    choice = input(PROMPT)
    if choice and choice[0] == "t":
        exit()
    else:
        # Jeśli użytkownik nie wyjdzie, wracamy do menu głównego
        return

# --- NOWA FUNKCJA add_ticket ---
def add_ticket():
    ticket = {}
    
    def choose_discount():
        while True:
            # 5.1. Wyświetl typ biletu
            print("Wybierz typ biletu:\nn – normalny\nu – ulgowy\np - powrót\nk - koniec")
            # 6.1. Pobierz jeden znak od użytkownika
            u_input = input(PROMPT)
            if not u_input: continue
            ch = u_input[0]
            
            if ch == "n":
                ticket["discount"] = "normalny"
                return True
            elif ch == "u":
                ticket["discount"] = "ulgowy"
                return True
            elif ch == "p":
                return False # Powrót do menu
            elif ch == "k":
                end_machine()
                return False
            else:
                print(ERROR_MSG)

    def choose_validity_from_map(prompt_text, options_map):
        while True:
            print(prompt_text)
            u_input = input(PROMPT)
            if not u_input: continue
            ch = u_input[0]
            
            if ch in options_map:
                ticket["validity"] = options_map[ch]
                return True
            elif ch == "p":
                return False
            elif ch == "k":
                end_machine()
                return False
            else:
                print(ERROR_MSG)

    def choose_type():
        while True:
            # 8.1. Wyświetl rodzaj biletu
            print("Wybierz typ biletu:\no – okresowy\nc – czasowy\nj – jednorazowy\np - powrót\nk - koniec")
            u_input = input(PROMPT)
            if not u_input: continue
            ch = u_input[0]
            
            if ch == "o":
                ticket["type"] = "okresowy"
                if choose_validity_from_map(
                    "Wybierz okres ważnosci biletu:\n1 – półroczny\n2 – miesięczny\n3 – tygodniowy\n4 – jednodniowy\np - powrót\nk - koniec",
                    {"1": "półroczny", "2": "miesięczny", "3": "tygodniowy", "4": "jednodniowy"},
                ): return True
                else: continue # Jeśli wybrano 'p' w podmenu, wróć do wyboru typu
            elif ch == "c":
                ticket["type"] = "czasowy"
                if choose_validity_from_map(
                    "Wybierz okres ważnosci biletu:\n1 – 60 minut\n2 – 30 minut\n3 – 10 minut\np - powrót\nk - koniec",
                    {"1": "60 - minutowy", "2": "30 - minutowy", "3": "10 - minutowy"},
                ): return True
                else: continue
            elif ch == "j":
                ticket["type"] = "jednorazowy"
                if choose_validity_from_map(
                    "Wybierz obszar ważnosci biletu:\n1 – miejski\n2 – aglomeracyjny\np - powrót\nk - koniec",
                    {"1": "miejski", "2": "aglomeracyjny"},
                ): return True
                else: continue
            elif ch == "p":
                return False
            elif ch == "k":
                end_machine()
                return False
            else:
                print(ERROR_MSG)

    # Logika sekwencyjna dodawania biletu
    if choose_discount():
        if choose_type():
            # 12.1 Na podstawie wyboru odczytaj cenę z cennika
            ticket["price"] = prices[ticket["discount"]][ticket["type"]][ticket["validity"]]
            # 13.1 Dodaj bilet do listy koszyk.
            cart.append(ticket)
            # 14.1 Wyświetl komunikat o dodaniu biletu do koszyka
            print(f"Dodano do koszyka bilet {ticket['discount']} {ticket['type']} {ticket['validity']} za cenę {ticket['price']}")

# --- INICJALIZACJA I PĘTLA GŁÓWNA ---
with open("./prices.json", "r", encoding="UTF-8") as jf:
    prices = json.load(jf)

cart = []
end = False

while not end:
    display_menu()
    user_input = input(PROMPT)
    if not user_input:
        continue
    option = user_input[0]

    match option:
        case "1":
            add_ticket() # Wywołanie wklejonej funkcji
        case "2":
            display_cart()
        case "3":
            if not cart:
                print("W koszyku nie ma jeszcze żadnych biletów.")
            else:
                total_to_pay = sum(t["price"] for t in cart)
                print(f"Do zapłaty: {total_to_pay:.2f} zł.")
                # Logika płatności (uproszczona na potrzeby przykładu)
                print("Wybierz metodę płatności: k - karta, g - gotówka, b - blik")
                input(PROMPT)
                print("Drukowanie biletów ...")
                time.sleep(1)
                cart = []
        case "4":
            end_machine()
        case _:
            print(ERROR_MSG)