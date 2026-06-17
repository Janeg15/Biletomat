import json
import time

# Stałe
PROMPT = "Twój wybór: "
ERROR_MSG = "Niepoprawny wybór, spróbuj ponownie."

# Funkcje
def display_menu(cart, prices):
    # 3. Wyświetl użytkownikowi menu główne
    print()
    print("Wybierz jedną z opcji:\n1 - dodaj bilet\n2 - pokaż koszyk\n3 - zapłać\n4 - zakończ program")
    
    # 4. Pobierz jeden znak od użytkownika
    option = input(PROMPT)[0]
    
    match option:
        case "1":
            add_ticket(cart, prices)
        case "2":
            display_cart(cart)
        case "3":
            register_payment(cart, prices)
        case "4":
            end_machine(cart, prices)
        case _:
            print(ERROR_MSG)

def display_cart(cart):
    # 5.2 Jeśli koszyk jest pusty pokaż komunikat z stosowną informacją
    if not cart:
        print("W koszyku nie ma jeszcze żadnych biletów.")
    # 6.2 W przeciwnym razie
    else:
        # 7.2 wypisz wszystkie bilety
        print("--- Zawartość koszyka ---")
        for i, ticket in enumerate(cart, 1):
            print(f"{i}. Bilet: {ticket['discount']} | Rodzaj: {ticket['type']} | Ważność/Obszar: {ticket['validity']} | Cena: {ticket['price']:.2f} zł")
        print("-------------------------")

def register_payment(cart, prices):
    # 5.3 Jeśli koszyk jest pusty pokaż komunikat z stosowną informacją
    if not cart:
        print("W koszyku nie ma jeszcze żadnych biletów.")
    # 6.3 W przeciwnym razie wyświetl kwotę do zapłaty
    else:
        print(get_cart_value(cart))
        # 7.3 Zapytaj o metodę płatności:
        while True:
            print("Wybierz metodę płatności:\nc - karta\ng - gotówka\nb - blik\np - powrót\nk - koniec")
            # 8.3 Pobierz jeden znak od użytkownika
            payment_method = input(PROMPT)[0]
            match payment_method:
                case "c":
                    pay_by_card()
                    break
                case "b":
                    pay_by_blik(cart, prices)
                    break
                case "g":
                    pay_by_cash(cart)
                    break
                case "p":
                    display_menu(cart, prices)
                    return
                case "k":
                    end_machine(cart, prices)
                case _:
                    print(ERROR_MSG)

        # 12.3 "Wydrukuj bilety i wyświetl komunikat „Dziękujemy za zakup”"
        print("Drukowanie biletów ...")
        time.sleep(len(cart))
        print("Dziękujemy za skorzystanie z automatu biletowego. Zapraszamy ponownie!")
        # 13.3 Wyczyść koszyk
        cart.clear()
        # 14.3 Zakończ działanie programu.
        exit()

def pay_by_card():
    input("Proszę zbliżyć kartę ...")

def pay_by_cash(cart):
    to_pay = sum(ticket["price"] for ticket in cart)
    paid = 0
    while paid < to_pay:
        print(f"Kwota do zapłaty: {(to_pay - paid):.2f} zł.")
        # 9.3.3 Poproś użytkownika o wpisanie kwoty.
        paid += float(input("Wrzuć pieniądze: "))
        # 10.3.3 Jeśli kwota > suma:
        if paid > to_pay:
            # 11.3.3 oblicz i wyświetl resztę
            print(f"Reszta: {(paid - to_pay):.2f} zł.")

def pay_by_blik(cart, prices):
    while True:
        blik = input("Podaj kod BLIK: ")
        if len(blik) == 6 and blik.isdigit():
            print("Kod BLIK zaakceptowany.")
            break
        else:
            print("Płatność nie powiodła się, spróbuj ponownie")

def get_cart_value(cart):
    return f"Wartość biletów w koszyku: {sum(ticket['price'] for ticket in cart):.2f} zł."

def end_machine(cart, prices):
    choice = input("Czy na pewno chcesz porzucić koszyk (t - tak)? ")[0]
    if choice == "t":
        # 5.4 Zakończ działanie programu.
        exit()
    else: 
        display_menu(cart, prices)

def add_ticket(cart, prices):
    ticket = {}
    # Wywołujemy funkcje pomocnicze przekazując im koszyk i cennik
    choose_discount(ticket, cart, prices) 
    choose_type(ticket, cart, prices)
    
    # Odczytujemy cenę na podstawie wprowadzonych wyborów
    ticket["price"] = prices[ticket["discount"]][ticket["type"]][ticket["validity"]]
    cart.append(ticket)
    print(f"Dodano do koszyka bilet {ticket['discount']} {ticket['type']} {ticket['validity']} za cenę {ticket['price']:.2f} zł")

def choose_discount(ticket, cart, prices):
    while True:
        print("Wybierz typ biletu:\nn - normalny\nu - ulgowy\np - powrót\nk - koniec")
        ch = input(PROMPT)[0]
        if ch == "n":
            ticket["discount"] = "normalny"
            return
        elif ch == "u":
            ticket["discount"] = "ulgowy"
            return
        elif ch == "p":
            display_menu(cart, prices)
            return
        elif ch == "k":
            end_machine(cart, prices)
        else:
            print(ERROR_MSG)

def choose_validity_from_map(ticket, prompt_text, options_map, cart, prices):
    while True:
        print(prompt_text)
        ch = input(PROMPT)[0]
        
        if ch in options_map:
            ticket["validity"] = options_map[ch]
            return
        elif ch == "p":
            display_menu(cart, prices)
            return
        elif ch == "k":
            end_machine(cart, prices)
        else:
            print(ERROR_MSG)

def choose_type(ticket, cart, prices):
    while True:
        # 8.1. Wyświetl rodzaj biletu
        print("Wybierz typ biletu:\no - okresowy\nc - czasowy\nj - jednorazowy\np - powrót\nk - koniec")
        ch = input(PROMPT)[0]

        if ch == "o":
            ticket["type"] = "okresowy"
            # Tutaj przekazujemy poprawne 5 argumentów do funkcji wyboru ważności
            choose_validity_from_map(
                ticket,
                "Wybierz okres ważności biletu:\n1 - półroczny\n2 - miesięczny\n3 - tygodniowy\n4 - jednodniowy\np - powrót\nk - koniec",
                {"1": "półroczny", "2": "miesięczny", "3": "tygodniowy", "4": "jednodniowy"},
                cart,
                prices
            )
            return

        elif ch == "c":
            ticket["type"] = "czasowy"
            # Tutaj również przekazujemy poprawne 5 argumentów
            choose_validity_from_map(
                ticket,
                "Wybierz okres ważności biletu:\n1 - 60 minut\n2 - 30 minut\n3 - 10 minut\np - powrót\nk - koniec",
                {"1": "60 - minutowy", "2": "30 - minutowy", "3": "10 - minutowy"},
                cart,
                prices
            )
            return

        elif ch == "j":
            ticket["type"] = "jednorazowy"
            # Tutaj również przekazujemy poprawne 5 argumentów
            choose_validity_from_map(
                ticket,
                "Wybierz obszar ważności biletu:\n1 - miejski\n2 - aglomeracyjny\np - powrót\nk - koniec",
                {"1": "miejski", "2": "aglomeracyjny"},
                cart,
                prices
            )
            return

        elif ch == "p":
            display_menu(cart, prices)
            return
        elif ch == "k":
            end_machine(cart, prices)
        else:
            print(ERROR_MSG)

if __name__ == "__main__":
    cart = []
    # Wczytanie cennika z pliku prices.json
    try:
        with open('prices.json', 'r', encoding='utf-8') as f:
            prices = json.load(f)
    except FileNotFoundError:
        print("Błąd: Nie znaleziono pliku prices.json!")
        exit()
        
    while True:
        display_menu(cart, prices)