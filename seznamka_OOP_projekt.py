from datetime import datetime
import json
import os
import random

# SEZNAMKA = seznamka.json
file_path = os.path.join(os.getcwd(), "seznamka.json")


def find_match():
    print("\n💘 Hledání spřízněné duše 💘")

    while True:
        user_id = input("Zadejte své uživatelské ID nebo napište 'zpět' pro návrat do hlavního menu: ")

        if user_id.lower() == "zpět":
            print("\n🔙 Návrat do hlavního menu...")
            return

        if user_id not in Register_user.users:
            print("\n❌ Uživatelské ID nebylo nalezeno. Zkuste to znovu nebo napište 'zpět'.")
            continue

        # Získáme profil uživatele
        current_user = Register_user.users[user_id]
        looking_for = current_user.looking_for

        # Filtrování uživatelů podle hledaného pohlaví a opačného zájmu
        matches = [
            user for user in Register_user.users.values()
            if user.gender == looking_for and user.looking_for == current_user.gender and user.id != user_id
        ]


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
    # Vytvoříme seznam slovníků pro zápis do JSON
    users_data = []
    for user in Register_user.users.values():
        users_data.append(
            {
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "gender": user.gender,
                "looking_for": user.looking_for,
            }
        )

    # Zapíšeme uživatele zpět do souboru
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(users_data, file, ensure_ascii=False, indent=4)


# Načítání uživatelů ze souboru JSON
def load_users_from_file():
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            users_data = json.load(file)  # Načteme data ze souboru JSON
            max_id_number = 0  # Zde budeme ukládat nejvyšší ID

            for user_data in users_data:
                id = user_data.get("id")
                name = user_data.get("name")
                age = user_data.get("age")
                gender = user_data.get("gender")
                looking_for = user_data.get("looking_for")

                # Extrahujeme číslo z ID a hledáme nejvyšší
                if id.startswith("user"):
                    try:
                        id_number = int(id[4:])
                        if id_number > max_id_number:
                            max_id_number = id_number
                    except ValueError:
                        print(f"Chyba při čtení ID: {id}")

                # Vytvoříme novou instanci s ID
                Register_user(id, name, age, gender, looking_for)

            # Nastavíme počet uživatelů na nejvyšší ID
            Register_user.users_count = max_id_number
    except FileNotFoundError:
       print("Žádní uživatelé nebyli nalezeni. Vytvořte první profil a zahajte svou cestu za láskou!")

    except json.JSONDecodeError:
        print("Soubor obsahuje neplatná data JSON.")





class Register_user:
    # Slovník pro uložení instancí
    users = {}
    users_count = 0  # Slovník pro uchování hodnoty

    def __init__(self, id, name, age, gender, looking_for):
        self.id = id
        self.gender = gender
        self.name = name
        self.age = age
        self.looking_for = looking_for
        Register_user.users_count += 1  # Zvýšení počtu uživatelů
        Register_user.users[self.id] = self
        
    @classmethod
    def create_new_user(cls, name, age, gender, looking_for):
        cls.users_count += 1
        id = f"user{cls.users_count}"
        return cls(id, name, age, gender, looking_for)


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
if Register_user.users:
    print("\n\t❤️\tAmor hlásí plný toulec! Na lásku čeká spousta dalších duší.\t💘")
else:
    print("\n\t💔\tZatím tu není nikdo, kdo by čekal na svou šanci. \t😢")
    print("\n\t🌟\tZaložte první profil a dejte lásce šanci!")


def get_birth_date():
    while True:
        user_input = input("\nDatum narození (ve formátu DD.MM.RRRR): ")
        try:
            return datetime.strptime(user_input, "%d.%m.%Y")

        except ValueError:
            # Pokud formát neodpovídá, zobrazí chybu
            print(
                """
                  💬 Ups! Vypadá to, že Amor nezvládá číst vaše datum. 📅
                  🛠️ Zkuste to znovu a zadejte datum ve formátu DD.MM.RRRR – i láska si zaslouží přesnost! ❤️"""
            )


def calculate_age(birth_date):
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
    
    new_user = Register_user.create_new_user(name, age, gender, looking_for)

    print(f"\n\t🌟 Profil vytvořen! Vaše ID: {new_user.id} 🌟")
    print(f"\n\t Poznamenejte si své ID, bez něj nebude možné profil později smazat.")
    print("\n\t🌟 Vaše šance na lásku právě vzrostla o 100%! 🌟")

    # Uložení nové databáze do souboru
    save_users_to_file()


while True:
    action = input(
        """
    
    💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔💔
                   
                     Vítejte na seznamce 💑 💌 POSLEDNÍ ŠANCE 💌 💑! 
                   ☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️☁️️☁️☁️☁️☁️☁️☁️☁️☁️☁️
                
                Ještě pořád je čas najít toho pravého nebo tu pravou. 😊
                    Osud čeká jen na vás, tak co podniknete dál?

    💔 Vaše možnosti:
                   
        1️⃣  ZALOŽIT PROFIL – protože láska si zaslouží druhou (i desátou) šanci! 🌟
                    
        2️⃣  SMAZAT PROFIL – když už máte dost a chcete dát Amorovi dovolenou. 🗑️
                    
        3️⃣  VYHLEDAT spřízněnou duši – kdo ví, třeba někdo čeká právě teď! 🔍
                    
        4️⃣  PROHLÉDNOUT všechny profily – jen tak, pro inspiraci a možná něco víc. 📂
                    
        5️⃣  ODEJÍT – někdy to prostě chce pauzu... 🚪

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

            if to_delete in Register_user.users:
                print("\n\t😢 Váš profil byl smazán. Amor má slzy na krajíčku. 😢")
                del Register_user.users[to_delete]  # ✅ Správný způsob mazání uživatele ze slovníku
                save_users_to_file()
                break
            else:
                print("\n\t❌ Uživatelské ID nebylo nalezeno. Zkuste to znovu nebo napište 'zpět'.")


    elif action == "3":
        print("\n\t🔍 Hledáme spřízněnou duši... držte si klobouky! 🎯")
        find_match()

    elif action == "4":
        for user in Register_user.users.values():
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
