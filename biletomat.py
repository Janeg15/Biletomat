import json
import time
import os

# Stałe
PROMPT = "Twój wybór: "
ERROR_MSG = "Niepoprawny wybór, spróbuj ponownie."

# Funkcje
def display_cart():
    # 5.2 Jeśli koszyk jest pusty pokaż komunikat z stosowną informacją
    if not cart:
        print("W koszyku nie ma jeszcze żadnych biletów.")
    # 6.2 W przeciwnym razie
    else:
        # 7.2 wypisz wszystkie bilety
        print("Zawartość koszyka")
        print()
        print("Lp. |  Cena   | Bilet")
        for index, ticket in enumerate(cart):
            print(f"{index:3} | {ticket['price']:7.2f} zł | Bilet {ticket['discount']} {ticket['type']} {ticket['validity']}")
        print()
        # 8.2 pokaż sumę
        print(get_cart_value())

def register_payment():
    pass

def pay_by_card():
    pass

def pay_by_cash():
    pass

def pay_by_blik():
    pass

def get_cart_value():
    return f"Wartość biletów w koszyku: {sum(ticket['price'] for ticket in cart):5.2f} zł."

def end_machine():
    print("Czy na pewno chcesz porzucić koszyk? (t - tak)")
    choice = input(PROMPT)[0]
    if choice == "t":
        # 5.4 Zakończ działanie programu.
        exit()
    if choice == "n":
        pass
    else:
        print(ERROR_MSG)

# 1. Wczytaj dane z pliku prices.json i zapisz je do zmiennej jako słownik/dictionary.
# Używamy ścieżki względnej ./ zgodnie ze screenami
with open("./prices.json", "r", encoding="UTF-8") as jf:
    prices = json.load(jf)

cart = []
end = False

while not end:
    print("Wybierz jedną z opcji:\n1 - dodaj bilet\n2 - pokaż koszyk\n3 - zapłać\n4 - zakończ program")

    user_input = input(PROMPT)
    if not user_input:
        continue
    option = user_input[0]

    match option:
        case "1":
            ticket = {}
            while True:
                print("Wybierz typ biletu:\nn - normalny\nu - ulgowy\np - powrót\nk - koniec")
                
                t1_input = input(PROMPT)
                if not t1_input: continue
                ticket1 = t1_input[0]

                if ticket1 == "n":
                    ticket["discount"] = "normalny"
                    break
                elif ticket1 == "u":
                    ticket["discount"] = "ulgowy"
                    break
                elif ticket1 == "p":
                    break
                elif ticket1 == "k":
                    exit()
                else:
                    print(ERROR_MSG)

            if not ticket or ticket1 == "p":
                continue

            cont = True
            while True:
                print("Wybierz typ biletu:\no - okresowy\nc - czasowy\nj - jednorazowy\np - powrót\nk - koniec")
                t2_input = input(PROMPT)
                if not t2_input: continue
                ticket2 = t2_input[0]

                if ticket2 == "o":
                    ticket["type"] = "okresowy"
                    while True:
                        # 10.1.1 Wyświetl dostępne opcje z pliku JSON
                        print("Wybierz okres ważności biletu:\n1 - półroczny\n2 - miesięczny\n3 - tygodniowy\n4 - jednodniowy\np - powrót\nk - koniec")
                        # 11.1.1 Pobierz jeden znak od użytkownika
                        t3_input = input(PROMPT)
                        if not t3_input: continue
                        ticket3 = t3_input[0]
                        match ticket3:
                            case "1": ticket["validity"] = "półroczny"; break
                            case "2": ticket["validity"] = "miesięczny"; break
                            case "3": ticket["validity"] = "tygodniowy"; break
                            case "4": ticket["validity"] = "jednodniowy"; break
                            case "p": cont = False; break
                            case "k": exit()
                            case _: print(ERROR_MSG)
                    if not cont: break
                    break

                elif ticket2 == "c":
                    ticket["type"] = "czasowy"
                    while True:
                        print("Wybierz okres ważności biletu:\n1 - 60 minut\n2 - 30 minut\n3 - 10 minut\np - powrót\nk - koniec")
                        t3_input = input(PROMPT)
                        if not t3_input: continue
                        ticket3 = t3_input[0]
                        match ticket3:
                            case "1": ticket["validity"] = "60 - minutowy"; break
                            case "2": ticket["validity"] = "30 - minutowy"; break
                            case "3": ticket["validity"] = "10 - minutowy"; break
                            case "p": cont = False; break
                            case "k": exit()
                            case _: print(ERROR_MSG)
                    if not cont: break
                    break

                elif ticket2 == "j":
                    ticket["type"] = "jednorazowy"
                    while True:
                        print("Wybierz obszar ważności biletu:\n1 - miejski\n2 - aglomeracyjny\np - powrót\nk - koniec")
                        t3_input = input(PROMPT)
                        if not t3_input: continue
                        ticket3 = t3_input[0]
                        match ticket3:
                            case "1": ticket["validity"] = "miejski"; break
                            case "2": ticket["validity"] = "aglomeracyjny"; break
                            case "p": cont = False; break
                            case "k": exit()
                            case _: print(ERROR_MSG)
                    if not cont: break
                    break
                
                elif ticket2 == "p":
                    cont = False
                    break
                elif ticket2 == "k":
                    exit()
                else:
                    print(ERROR_MSG)
            
            if not cont or "validity" not in ticket:
                continue

            ticket["price"] = prices[ticket["discount"]][ticket["type"]][ticket["validity"]]
            cart.append(ticket)
            print(f"Dodano do koszyka bilet {ticket['discount']} {ticket['type']} {ticket['validity']} za cenę {ticket['price']}")

        case "2":
            display_cart()

        case "3":
            if not cart:
                print("W koszyku nie ma jeszcze żadnych biletów.")
            else:
                print(f"Do zapłaty: {sum(t['price'] for t in cart):.2f} zł.")
                
                while True:
                    print("Wybierz metodę płatności:\nk - karta\ng - gotówka\nb - blik\np - powrót\nk - koniec")
                    m_input = input(PROMPT)
                    if not m_input: continue
                    payment_method = m_input[0]
                    cont = True

                    match payment_method:
                        case "k":
                            pay_by_card()
                            input("Proszę zbliżyć kartę ...")
                            break
                        case "b":
                            pay_by_blik()
                            blik = input("Podaj kod BLIK: ")
                            if len(blik) != 6:
                                print("Płatność nie powiodła się, spróbuj ponownie")
                                continue
                            break
                        case "g":
                            pay_by_cash()
                            to_pay = sum(t["price"] for t in cart)
                            paid = 0
                            while paid < to_pay:
                                try:
                                    paid += float(input("Wrzuć pieniądze: "))
                                except ValueError:
                                    print("Podaj poprawną kwotę.")
                            if paid > to_pay:
                                print(f"Reszta: {(paid - to_pay):.2f} zł.")
                            break
                        case "p":
                            cont = False
                            break
                        case "k":
                            exit()
                        case _:
                            print(ERROR_MSG)
                    
                if not cont:
                    continue

                print("Drukowanie biletów ...")
                time.sleep(len(cart))
                print("Dziękujemy za skorzystanie z automatu biletowego. Zapraszamy ponownie!")
                cart = []

        case "4":
            end_machine()
                
        case _:
            print(ERROR_MSG)