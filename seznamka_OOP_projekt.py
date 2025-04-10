"""Humorná seznamka - psáno pro naučení se základů OOP programování."""
from datetime import datetime
import json
import os
import random

# Cesta k souboru seznamka.json
file_path = os.path.join(os.getcwd(), "seznamka.json")


def find_match():
    """Doporučí vhodný profil na základě preferencí uživatele.

    Hledá protějšek s opačnou preferencí podle zadaného ID.
    """
    print("\n💘 Hledání spřízněné duše 💘")

    while True:
        user_id = input(
            "Zadejte své uživatelské ID nebo napište 'zpět' pro návrat do hlavního menu: ")

        if user_id.lower() == "zpět":
            print("\n🔙 Návrat do hlavního menu...")
            return

        if user_id not in RegisterUser.users:
            print("\n❌ Uživatelské ID nebylo nalezeno. Zkuste to znovu nebo napište 'zpět'.")
            continue

        # Získáme profil uživatele
        current_user = RegisterUser.users[user_id]
        looking_for = current_user.looking_for

        # Filtrování uživatelů podle hledaného pohlaví a opačného zájmu
        matches = []
        for potential_user in RegisterUser.users.values():
            if (
                potential_user.gender == looking_for and
                looking_for == current_user.gender and
                potential_user.id != user_id
            ):
                matches.append(potential_user)


        if matches:
            # Náhodný výběr z nalezených profilů
            match = random.choice(matches)
            print("\n💞 Našli jsme spřízněnou duši! 💞")
            print(f"""
                🎉 Pro uživatele:
                🏷️   Jméno: {current_user.name}
                ⚤   Pohlaví: {current_user.gender}
                🎂  Věk: {current_user.age}
                🔎  Hledá: {current_user.looking_for}

                💞 Spřízněná duše:
                🏷️   Jméno: {match.name}
                ⚤   Pohlaví: {match.gender}
                🎂  Věk: {match.age}
                🔎  Hledá: {match.looking_for}
                """)
        else:
            print("\n😢 Žádná spřízněná duše nebyla nalezena. Zkuste později.")
        break

# Uložení uživatelů do souboru JSON
def save_users_to_file():
    """Uloží všechny profily uživatelů do JSON souboru."""
    # Vytvoříme seznam slovníků pro zápis do JSON
    users_data = []
    for profile in RegisterUser.users.values():
        users_data.append({
            "id": profile.user_id,
            "name": profile.name,
            "age": profile.age,
            "gender": profile.gender,
            "looking_for": profile.looking_for,
        })

    # Zapíšeme uživatele zpět do souboru
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(users_data, file, ensure_ascii=False, indent=4)


# Načítání uživatelů ze souboru JSON
def load_users_from_file():
    """Načte profily uživatelů ze souboru a obnoví jejich instance."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            users_data = json.load(file)  # Načteme data ze souboru JSON
            max_id_number = 0  # Zde budeme ukládat nejvyšší ID

            for user_data in users_data:
                loaded_user_id = user_data.get("id")
                name = user_data.get("name")
                age = user_data.get("age")
                gender = user_data.get("gender")
                looking_for = user_data.get("looking_for")

                # Extrahujeme číslo z ID a hledáme nejvyšší
                if loaded_user_id.startswith("user"):
                    try:
                        id_number = int(loaded_user_id[4:])
                        max_id_number = max(max_id_number, id_number)

                    except ValueError:
                        print(f"Chyba při čtení ID: {loaded_user_id}")

                # Vytvoříme novou instanci s ID
                RegisterUser(loaded_user_id, name, age, gender, looking_for)

            # Nastavíme počet uživatelů na nejvyšší ID
            RegisterUser.users_count = max_id_number

    except FileNotFoundError:
        print("Žádní uživatelé nebyli nalezeni."
              "Vytvořte první profil a zahajte svou cestu za láskou!")

    except json.JSONDecodeError:
        print("Soubor obsahuje neplatná data JSON.")


class RegisterUser:
    """
    Třída pro vytvoření uživatelského profilu.

    Uchovává informace o uživateli (user_id, jméno, věk, pohlaví, preference) 
    a ukládá je do společného slovníku všech uživatelů.

    Atributy:
        user_id (str): Jedinečný identifikátor uživatele.
        name (str): Jméno uživatele.
        age (int): Věk uživatele.
        gender (str): Pohlaví uživatele.
        looking_for (str): Koho uživatel hledá.

    Třída uchovává:
        users (dict): Slovník všech instancí podle user_id.
        users_count (int): Celkový počet vytvořených uživatelů.
    """
    # Slovník pro uložení instancí
    users = {}
    users_count = 0  # Slovník pro uchování hodnoty

    def __init__(self, user_id, name, age, gender, looking_for):
        """Inicializuje nového uživatele a uloží jej do slovníku uživatelů."""
        self.user_id = user_id
        self.gender = gender
        self.name = name
        self.age = age
        self.looking_for = looking_for
        RegisterUser.users_count += 1  # Zvýšení počtu uživatelů
        RegisterUser.users[self.user_id] = self

    @classmethod
    def create_new_user(cls, name, age, gender, looking_for):
        """Vytvoří nového uživatele s automaticky generovaným user_id."""
        cls.users_count += 1
        user_id = f"user{cls.users_count}"
        return cls(user_id, name, age, gender, looking_for)

    def __str__(self):
        return f"""
            {self.name}
            pohlaví: {self.gender},
            věk: {self.age},
            hledám: {self.looking_for}
            """

# Načteme uživatele při spuštění programu
load_users_from_file()

# Test: V podstatě log, který potvrdí načtení uživatelů ze souboru JSON
if RegisterUser.users:
    print("\n\t❤️\tAmor hlásí plný toulec! Na lásku čeká spousta dalších duší.\t💘")
else:
    print("\n\t💔\tZatím tu není nikdo, kdo by čekal na svou šanci. \t😢")
    print("\n\t🌟\tZaložte první profil a dejte lásce šanci!")


def get_birth_date():
    """Získá a ověří datum narození od uživatele (formát DD.MM.RRRR)."""
    while True:
        user_input = input("\nDatum narození (ve formátu DD.MM.RRRR): ")
        try:
            return datetime.strptime(user_input, "%d.%m.%Y")
        except ValueError:
            # Pokud formát neodpovídá, zobrazí chybu
            print(
                "\n"
                "  💬 Ups! Vypadá to, že Amor nezvládá číst vaše datum. 📅\n"
                "  🛠️ Zkuste to znovu a zadejte datum ve formátu DD.MM.RRRR\n"
                "     – i láska si zaslouží přesnost! ❤️"
            )



def calculate_age(birth_date):
    """Spočítá věk na základě data narození."""
    # Aktuální datum
    today = datetime.today()
    # Výpočet věku
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )
    return age


def add_new_user():
    """Získá údaje od uživatele a vytvoří nový profil."""
    name = input("\nJméno: ")
    birth_date = get_birth_date()
    age = calculate_age(birth_date)

    print("""
        ⚤ Jaké je vaše pohlaví? Vyberte číslo:
        1️⃣  Muž
        2️⃣  Žena
        3️⃣  Jiné
    """)
    while True:
        gender_choice = input("👉 Vaše volba: ")
        if gender_choice == "1":
            gender = "muž"
            break
        elif gender_choice == "2":
            gender = "žena"
            break
        elif gender_choice == "3":
            gender = "jiné"
            break
        print("❗ Neplatná volba. Zkuste to znovu.")

    print("""
        🔎 Koho hledáte? Vyberte číslo:
        1️⃣  Muž
        2️⃣  Žena
        3️⃣  Jiné
    """)
    while True:
        looking_for_choice = input("👉 Vaše volba: ")
        if looking_for_choice == "1":
            looking_for = "muž"
            break
        elif looking_for_choice == "2":
            looking_for = "žena"
            break
        elif looking_for_choice == "3":
            looking_for = "jiné"
            break
        print("❗ Neplatná volba. Zkuste to znovu.")
        new_user = RegisterUser.create_new_user(name, age, gender, looking_for)

    print(f"\n\t🌟 Profil vytvořen! Vaše ID: {new_user.user_id} 🌟")
    print("\n\t Poznamenejte si své ID, bez něj nebude možné profil později smazat.")
    print("\n\t🌟 Vaše šance na lásku právě vzrostla o 100%! 🌟")

    # Uložení nové databáze do souboru
    save_users_to_file()


# Načteme uživatele při spuštění programu
load_users_from_file()

if RegisterUser.users:
    print("\n\t❤️\tAmor hlásí plný toulec! Na lásku čeká spousta dalších duší.\t💘")
else:
    print("\n\t💔\tZatím tu není nikdo, kdo by čekal na svou šanci. \t😢")
    print("\n\t🌟\tZaložte první profil a dejte lásce šanci!")


# Hlavní smyčka programu
while True:
    action = input(
        """
    
    💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔
                   
                     Vítejte na seznamce 💑 💌 POSLEDNÍ ŠANCE 💌 💑! 
                   ☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️️☁️☁️☁️☁️☁️☁️☁️☁️☁️
                
                Ještě pořád je čas najít toho pravého nebo tu pravou. 😊
                    Osud čeká jen na vás, tak co podniknete dál?

    💔 Vaše možnosti:
        1️⃣  ZALOŽIT PROFIL 🌟
        2️⃣  SMAZAT PROFIL 🗑️
        3️⃣  VYHLEDAT spřízněnou duši 🔍
        4️⃣  PROHLÉDNOUT všechny profily 📂
        5️⃣  ODEJÍT 🚪

    👉 Napište číslo své volby a dejte šanci osudu: 
                   
    💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔
                                        """
    )

    if action == "1":
        add_new_user()
        # Nejprve načteme existující data, pokud soubor existuje
    elif action == "2":
        while True:
            to_delete = input(
                """
                💔 Rozloučení s láskou? 💔
                Amor si zapíše, že jste mu dali kopačky.
                Prosím, zadejte své uživatelské ID nebo napište "zpět" pro návrat do hlavního menu: 🏹😢
                """
            )
            if to_delete.lower() == "zpět":
                print("\n🔙 Návrat do hlavního menu...")
                break

            elif to_delete in RegisterUser.users:
                print("\n\t😢 Váš profil byl smazán. Amor má slzy na krajíčku. 😢")
                del RegisterUser.users[to_delete]  # ✅ Správný způsob mazání uživatele ze slovníku
                save_users_to_file()
                break
            print("\n\t❌ Uživatelské ID nebylo nalezeno. Zkuste to znovu nebo napište 'zpět'.")

    elif action == "3":
        print("\n\t🔍 Hledáme spřízněnou duši... držte si klobouky! 🎯")
        find_match()

    elif action == "4":
        for user in RegisterUser.users.values():
            print(
                f"""
                    ________________________________________________
                    
                    🏷️  {user.name}

                    ------------------------------------------------

                    ⚤   Pohlaví: {user.gender}
                    🎂  Věk: {user.age}
                    🔎  Hledá: {user.looking_for}
                    ________________________________________________ 

                    💔 🔎 💔 🔎 💔 🔎 💔 🔎 💔 🔎 💔 🔎 💔 🔎 💔 🔎"""
            )
        print("\n\t📂 Prohlížíme profily – kdo ví, koho dnes objevíte! 😊")

    elif action == "5":
        print("\n\t🚪 Odcházíte? láska čeká na každého, tak snad počká i na Vás! 💞")
        break
    else:
        print("\n\t❓ Neplatná volba – možná Amor spletl šíp? Zkuste to znovu. 🎯")
