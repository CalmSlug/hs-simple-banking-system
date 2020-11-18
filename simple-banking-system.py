import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS card
               (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);''')
conn.commit()

lg = ""
pw = ""
card_two = ""
money_to_card_two = ""


def main():
    screen = "main"

    while True:

        if screen == "main":
            print("1. Create an account")
            print("2. Log into account")
            print("0. Exit")
            main_input = input()

            if main_input == "1":
                new_card()

            elif main_input == "2":
                global lg
                global pw
                print()
                print("Enter your card number:")
                lg = input()
                print("Enter your PIN:")
                pw = input()
                print()
                cur.execute("SELECT * FROM card WHERE number = ? AND pin = ?", (lg, pw))
                card_check = cur.fetchone()

                if card_check:
                    screen = "sub"
                    print("You have successfully logged in!")
                    print()

                else:
                    print("Wrong card number or PIN!")
                    print()

            elif main_input == "0":
                print()
                print("Bye!")
                conn.close()
                break

        elif screen == "sub":
            print("1. Balance")
            print("2. Add income")
            print("3. Do transfer")
            print("4. Close account")
            print("5. Log out")
            print("0. Exit")
            user_input = input()

            if user_input == "1":
                cur.execute("SELECT * FROM card WHERE number = ? AND pin = ?", (lg, pw))
                card_check = cur.fetchone()
                print()
                print("Balance:", card_check[3])
                print()

            elif user_input == "2":
                print()
                print("Enter income:")
                add_money = input()
                cur.execute("SELECT * FROM card WHERE number = ? AND pin = ?", (lg, pw))
                card_check = cur.fetchone()
                new_balance = card_check[3] + int(add_money)
                cur.execute("UPDATE card SET balance = ? WHERE number = ? AND pin = ?", (new_balance, lg, pw))
                conn.commit()
                print("Income was added!")
                print()

            elif user_input == "3":
                global card_two
                print()
                print("Transfer")
                print("Enter card number:")
                card_two = input()
                card_inspection()

            elif user_input == "4":
                cur.execute("DELETE FROM card WHERE number = ? AND pin = ?", (lg, pw))
                conn.commit()
                screen = "main"
                print()
                print("The account has been closed!")
                print()

            elif user_input == "5":
                screen = "main"
                print()
                print("You have successfully logged out!")
                print()

            elif user_input == "0":
                print()
                print("Bye!")
                conn.close()
                break


def new_card():
    global lg
    global pw
    lg = random.randint(400000000000000, 400000999999999)
    lg_temp = []

    for number in str(lg):
        lg_temp.append(int(number))

    lg_temp_2 = lg_temp
    lg_temp_2[0] = lg_temp_2[0] * 2
    lg_temp_2[2] = lg_temp_2[2] * 2
    lg_temp_2[4] = lg_temp_2[4] * 2
    lg_temp_2[6] = lg_temp_2[6] * 2
    lg_temp_2[8] = lg_temp_2[8] * 2
    lg_temp_2[10] = lg_temp_2[10] * 2
    lg_temp_2[12] = lg_temp_2[12] * 2
    lg_temp_2[14] = lg_temp_2[14] * 2

    lg_temp_9 = []

    for number in lg_temp_2:

        if number > 9:
            lg_temp_9.append(number - 9)

        else:
            lg_temp_9.append(number)

    lg = str(lg) + str((sum(lg_temp_9) * 9 % 10))

    pw = random.randint(0, 9999)
    pw = str(pw).zfill(4)

    cur.execute("INSERT INTO card (number, pin) VALUES (?, ?)", (lg, pw))
    conn.commit()

    print()
    print("Your card has been created")
    print("Your card number:")
    print(lg)
    print("Your card PIN:")
    print(pw)
    print()


def card_inspection():
    cur.execute("SELECT * FROM card WHERE number = ?", (card_two,))
    card_check = cur.fetchone()

    card_two_temp = []

    for number in card_two:
        card_two_temp.append(int(number))

    card_two_temp.pop()

    card_two_temp_2 = card_two_temp
    card_two_temp_2[0] = card_two_temp_2[0] * 2
    card_two_temp_2[2] = card_two_temp_2[2] * 2
    card_two_temp_2[4] = card_two_temp_2[4] * 2
    card_two_temp_2[6] = card_two_temp_2[6] * 2
    card_two_temp_2[8] = card_two_temp_2[8] * 2
    card_two_temp_2[10] = card_two_temp_2[10] * 2
    card_two_temp_2[12] = card_two_temp_2[12] * 2
    card_two_temp_2[14] = card_two_temp_2[14] * 2

    card_two_temp_9 = []

    for number in card_two_temp_2:

        if number > 9:
            card_two_temp_9.append(number - 9)

        else:
            card_two_temp_9.append(number)

    sep = ""
    card_15 = []

    for number in card_two:
        card_15.append(number)

    card_15.pop()

    card_two_luhn = sep.join(card_15) + str((sum(card_two_temp_9) * 9 % 10))

    if card_two == lg:
        print("You can't transfer money to the same account!")
        print()

    elif card_two_luhn != card_two:
        print("Probably you made a mistake in the card number. Please try again!")
        print()

    elif card_check == None:
        print("Such a card does not exist.")
        print()

    else:
        global money_to_card_two
        print("Enter how much money you want to transfer:")
        money_to_card_two = input()
        money_inspection()


def money_inspection():
    cur.execute("SELECT * FROM card WHERE number = ? AND pin = ?", (lg, pw))
    card_check = cur.fetchone()

    if int(money_to_card_two) > card_check[3]:
        print("Not enough money!")
        print()

    else:
        new_balance = card_check[3] - int(money_to_card_two)
        cur.execute("UPDATE card SET balance = ? WHERE number = ? AND pin = ?", (new_balance, lg, pw))
        cur.execute("SELECT * FROM card WHERE number = ?", (card_two,))
        card_two_data = cur.fetchone()
        new_balance = card_two_data[3] + int(money_to_card_two)
        cur.execute("UPDATE card SET balance = ? WHERE number = ?", (new_balance, card_two))
        conn.commit()
        print("Success!")
        print()


main()
