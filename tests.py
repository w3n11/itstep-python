import os
import random
from test import TestCase, Procedure, NewInstance  # type: ignore

TEST_DB = "test_accounts.txt"


def setup_db():
    """Vytvoří dočasnou databázi pro testy, aby nebyly závislé na produkčním souboru."""
    with open(TEST_DB, "w", encoding="utf-8") as f:
        f.write("1111/1234,Novak,Jan,jan@banka.cz,TajneHeslo1,5000,CZK\n")
        f.write("2222/1234,Svobodova,Eva,eva@banka.cz,TajneHeslo2,10000,CZK\n")


def teardown_db():
    """Uklidí dočasnou databázi po dokončení testu."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_db_loading(assignment) -> bool:
    try:
        bank = assignment.Bank(filepath=TEST_DB)
        if len(bank.accounts) != 2:
            raise AssertionError("Banka nenačetla správný počet účtů.")
        return True
    except assignment.DatabaseNotFound:
        raise AssertionError("Banka vyhodila DatabaseNotFound..")


def test_successful_login(assignment) -> bool:
    bank = assignment.Bank(filepath=TEST_DB)
    acc = bank.login()
    if acc is None:
        raise AssertionError("Při zadání správného hesla metoda nevrátila účet, ale None.")
    if acc.login_email != "jan@banka.cz":
        raise AssertionError(f"Očekáván účet pro jan@banka.cz, ale vrácen {acc.login_email}.")
    return True


def test_payment_negative_amount(assignment) -> bool:
    bank = assignment.Bank(filepath=TEST_DB)
    acc = [a for a in bank.accounts if a.account_number == "1111/1234"][0]
    bank.process_payment(acc)

    if acc.balance != 5000:
        raise AssertionError("Při zadání záporné částky se změnil zůstatek.")
    return True


def test_payment_overdraft(assignment) -> bool:
    bank = assignment.Bank(filepath=TEST_DB)
    acc = [a for a in bank.accounts if a.account_number == "1111/1234"][0]
    bank.process_payment(acc)

    if acc.balance != 5000:
        raise AssertionError("Uživatel úspěšně odeslal více peněz, než měl na účtu.")
    return True


def test_payment_valid_and_operator(assignment) -> bool:
    bank = assignment.Bank(filepath=TEST_DB)
    sender = [a for a in bank.accounts if a.account_number == "1111/1234"][0]
    receiver = [a for a in bank.accounts if a.account_number == "2222/1234"][0]

    bank.process_payment(sender)

    if sender.balance == 5000 and receiver.balance == 10000:
        raise AssertionError("Platba se vůbec neprovedla, zůstatky se nezměnily.")
    if sender.balance == 3000 and receiver.balance == 8000:
        raise AssertionError("Cílovému účtu se peníze odečetly místo přičtení.")
    if sender.balance != 3000 or receiver.balance != 12000:
        raise AssertionError("Zůstatky po platbě nesedí s očekávaným výpočtem.")
    return True


def test_payment_to_self(assignment) -> bool:
    bank = assignment.Bank(filepath=TEST_DB)
    acc = [a for a in bank.accounts if a.account_number == "1111/1234"][0]
    bank.process_payment(acc)

    if acc.balance != 5000:
        raise AssertionError("Zůstatek se změnil, ačkoliv uživatel posílal peníze sám sobě.")
    return True


def validate_db_saved(filepath: str) -> bool:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return "jan@banka.cz,TajneHeslo1,3000,CZK" in content and "eva@banka.cz,TajneHeslo2,12000,CZK" in content


def test_bonus_integrity(assignment) -> bool:
    try:
        bank = assignment.Bank(filepath=TEST_DB)
    except Exception:
        raise AssertionError("Banka se nenačetla.")

    if not hasattr(bank, "check_integrity"):
        raise AssertionError("Bance chybí metoda 'check_integrity()'.")

    if not bank.check_integrity():
        raise AssertionError("check_integrity() vrací False, i když se nic nestalo.")

    hacker = bank.accounts[0]
    hacker.balance += 100_000

    if bank.check_integrity():
        raise AssertionError("Metoda neodhalila, že si uživatel přidal peníze.")

    return True


def generate(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)

    result: list[TestCase] = [
        # --- 1. BASE FUNCTIONALITY ---
        TestCase(
            id=(1, 0),
            name="Třída Account se správně inicializuje",
            func=TestCase.test_class_init,
            args=("Account", ("1111", "Jan", "Novak", "jan@mail.cz", "heslo", "1500", "CZK")),
            expected_return=True
        ),
        TestCase(
            id=(1, 1),
            name="Třída Bank a základní kostra existuje",
            func=TestCase.test_class_existence,
            args=("Bank",),
            expected_return=True
        ),
        TestCase(
            id=(1, 2),
            name="Načítání databáze z parametru konstruktoru",
            func=test_db_loading,
            setup=setup_db,
            teardown=teardown_db,
            expected_return=True,
            prerequisites={(1, 1)}
        ),

        # --- 2. LOGIN ---
        TestCase(
            id=(2, 0),
            name="Úspěšné přihlášení správným heslem vrací objekt Account",
            func=test_successful_login,
            inputs=["jan@banka.cz", "TajneHeslo1"],
            setup=setup_db,
            teardown=teardown_db,
            verify_print=lambda _: True,
            expected_return=True,
            prerequisites={(1, 2)}
        ),
        TestCase(
            id=(2, 1),
            name="Neexistující email vrací z loginu None",
            func=TestCase.test_class,
            args=("Bank", Procedure().add("login", expected_return_or_value=None), (TEST_DB,)),
            inputs=["neexistuje@banka.cz"],
            setup=setup_db,
            teardown=teardown_db,
            verify_print=lambda _: True,
            expected_return=True,
            prerequisites={(1, 2)}
        ),
        TestCase(
            id=(2, 2),
            name="Zablokování účtu po 3 špatných heslech",
            func=TestCase.test_class,
            args=("Bank", Procedure().add("login", ignore=True), (TEST_DB,)),
            inputs=["jan@banka.cz", "spatne1", "spatne2", "spatne3"],
            expected_exception=NewInstance("SuspiciousLoginAttempt"),
            setup=setup_db,
            teardown=teardown_db,
            verify_print=lambda _: True,
            prerequisites={(1, 2)}
        ),

        # --- 3. PAYMENTS ---
        TestCase(
            id=(3, 0),
            name="Úspěšná platba upraví zůstatky objektů",
            func=test_payment_valid_and_operator,
            inputs=["2222/1234", "2000"],
            setup=setup_db,
            teardown=teardown_db,
            expected_return=True,
            verify_print=lambda _: True,
            prerequisites={(2, 0)}
        ),
        TestCase(
            id=(3, 1),
            name="Úspěšná platba se uloží zpět do souboru",
            func=test_payment_valid_and_operator,
            inputs=["2222/1234", "2000"],
            setup=setup_db,
            teardown=teardown_db,
            expected_return=True,
            verify_print=lambda _: True,
            file_validators={TEST_DB: validate_db_saved},
            prerequisites={(3, 0)}
        ),
        TestCase(
            id=(3, 2),
            name="Zákaz zasílání peněz sobě samému",
            func=test_payment_to_self,
            inputs=["1111/1234", "1000"],
            setup=setup_db,
            teardown=teardown_db,
            expected_return=True,
            verify_print=lambda _: True,
            prerequisites={(2, 0)}
        ),
        TestCase(
            id=(3, 3),
            name="Zákaz záporných částek při platbě",
            func=test_payment_negative_amount,
            inputs=["2222/1234", "-5000"],
            setup=setup_db,
            teardown=teardown_db,
            expected_return=True,
            verify_print=lambda _: True,
            prerequisites={(2, 0)}
        ),
        TestCase(
            id=(3, 4),
            name="Ochrana proti přečerpání účtu",
            func=test_payment_overdraft,
            inputs=["2222/1234", "9999999"],
            setup=setup_db,
            teardown=teardown_db,
            expected_return=True,
            verify_print=lambda _: True,
            prerequisites={(2, 0)}
        )
    ]
    return result


def generate_bonus(seed: int | None = None) -> list[TestCase]:
    random.seed(seed)

    result: list[TestCase] = [
        TestCase(
            id=(4, 0),
            name="Třída Bank má bezpečnostní metodu check_integrity",
            func=TestCase.test_class_definition,
            args=("Bank", "check_integrity", (), False),
            expected_return=True
        ),
        TestCase(
            id=(4, 1),
            name="Odhalení podvodu pomocí kontrolního součtu všech peněz",
            func=test_bonus_integrity,
            setup=setup_db,
            teardown=teardown_db,
            expected_return=True,
            prerequisites={(4, 0)}
        )
    ]
    return result
