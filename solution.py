from os import path
from database import generate


class DatabaseNotFound(Exception):
    pass


class LoadingAccountsFailed(Exception):
    pass


class SuspiciousLoginAttempt(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


class InvalidAmountError(Exception):
    pass


class Account:
    def __init__(
            self,
            account_number: str,
            first_name: str,
            last_name: str,
            login_email: str,
            login_password: str,
            balance: str,
            currency: str
    ) -> None:
        self.account_number = account_number
        self.first_name = first_name
        self.last_name = last_name
        self.login_email = login_email
        self.login_password = login_password
        self.balance = int(balance)
        self.currency = currency


class Bank:
    def __init__(self, filepath: str = "accounts.txt") -> None:
        self.accounts_filepath = filepath
        self.accounts: list[Account] = []
        self.logged_users: list[str] = []

        if path.exists(self.accounts_filepath):
            if not self.load_accounts():
                raise LoadingAccountsFailed("Nepodařilo se načíst databázi účtů.")
        else:
            raise DatabaseNotFound("Soubor s databází nebyl nalezen.")

    def load_accounts(self) -> bool:
        try:
            with open(file=self.accounts_filepath, mode="r", encoding="utf-8") as f:
                for line in f.read().splitlines():
                    if line.strip():
                        self.accounts.append(Account(*line.split(",")))
                return True
        except Exception as e:
            print(f"Chyba při načítání účtů: {e}")
            return False

    def save_accounts(self) -> None:
        """Uloží aktuální stav všech účtů zpět do databáze (souboru)."""
        lines = []
        for acc in self.accounts:
            lines.append(
                f"{acc.account_number},{acc.first_name},"
                f"{acc.last_name},{acc.login_email},"
                f"{acc.login_password},{acc.balance},{acc.currency}"
            )
        with open(file=self.accounts_filepath, mode="w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def login(self) -> Account | None:
        """Vrací objekt účtu při úspěšném přihlášení, jinak None."""
        email: str = input("Email: ")

        for account in self.accounts:
            if email == account.login_email:
                attempts_left: int = 3
                while attempts_left > 0:
                    password: str = input(f"Password ({attempts_left} pokusy): ")
                    if password == account.login_password:
                        self.logged_users.append(email)
                        return account
                    print("Neplatné heslo.")
                    attempts_left -= 1

                self.send_warning(email)
                raise SuspiciousLoginAttempt(f"Účet {email} byl dočasně zablokován.")

        print("Účet s tímto emailem neexistuje.")
        return None

    def send_warning(self, email: str) -> None:
        print(f"\n[SYSTEM] Odeslán varovný email na {email}: Detekován podezřelý pokus o přihlášení.")

    def process_payment(self, sender: Account) -> None:
        target_number = input("Zadejte číslo účtu příjemce: ")

        if sender.account_number == target_number:
            print("Nemůžete poslat peníze sami sobě.")
            return

        target_account = next((acc for acc in self.accounts if acc.account_number == target_number), None)

        if not target_account:
            print("Cílový účet nebyl nalezen.")
            return

        try:
            amount = int(input("Zadejte částku k odeslání: "))

            if amount < 1:
                raise InvalidAmountError("Částka musí být větší než nula.")

            if amount > sender.balance:
                raise InsufficientFundsError(f"Nemáte dostatek prostředků. Váš zůstatek je {sender.balance}"
                                             f" {sender.currency}.")

        except ValueError:
            print("Neplatný formát částky. Zadejte celé číslo.")
            return
        except (InvalidAmountError, InsufficientFundsError) as e:
            print(f"Zamítnuto: {e}")
            return

        sender.balance -= amount
        target_account.balance += amount
        self.save_accounts()
        print(f"Platba {amount} {sender.currency} na účet {target_number} proběhla úspěšně!")


def logged_in_menu(bank: Bank, user: Account):
    while True:
        print("\n--- MŮJ ÚČET ---")
        print(f"Uživatel: {user.first_name} {user.last_name}")
        print(f"Číslo účtu: {user.account_number}")
        print(f"Zůstatek: {user.balance} {user.currency}")
        print("-" * 16)
        print("1 - Odeslat peníze")
        print("2 - Odhlásit se")

        choice = input("Vaše volba: ")
        if choice == "1":
            bank.process_payment(user)
        elif choice == "2":
            print("Byli jste úspěšně odhlášeni.")
            break
        else:
            print("Neplatná volba.")


def client_app():
    print("Spouštím bankovní aplikaci...")
    if not path.exists("accounts.txt"):
        generate(2000)

    try:
        bank = Bank()
    except (DatabaseNotFound, LoadingAccountsFailed) as e:
        print(f"Kritická chyba: {e}")
        return

    while True:
        print("\n=== INTERNETOVÉ BANKOVNICTVÍ ===")
        print("1 - Přihlásit se")
        print("2 - Ukončit")
        choice = input("Vaše volba: ")

        if choice == "2":
            print("Děkujeme, že využíváte naše služby.")
            break
        elif choice == "1":
            try:
                user_account = bank.login()
                if user_account:
                    print("\nPřihlášení bylo úspěšné.")
                    logged_in_menu(bank, user_account)
            except SuspiciousLoginAttempt as e:
                print(f"Bezpečnostní varování: {e}")
        else:
            print("Neplatná volba.")


if __name__ == "__main__":
    client_app()
