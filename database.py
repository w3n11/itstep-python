import faker
from unicodedata import normalize
from re import sub
from random import randint, random, choice


def get_account_number() -> str:
    weights = [6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
    bank_id = "1234"

    while True:
        length = randint(8, 10)
        digits = [randint(0, 9) for _ in range(length)]

        if length == 10 and digits[0] == 0:
            continue
        if all(c == 0 for c in digits):
            continue

        full_number = [0] * (10 - length) + digits
        control_sum = sum(c * v for c, v in zip(full_number, weights))

        if control_sum % 11 == 0:
            base_number = "".join(map(str, digits))
            return f"{base_number}/{bank_id}"


def base_letters(text: str) -> str:
    normalized = normalize('NFKD', text)
    ascii_text = normalized.encode('ascii', 'ignore').decode('utf-8')
    strict_letters = sub(r'[^A-Za-z]', '', ascii_text)
    return strict_letters


def get_email(first_name: str, last_name: str, year_of_birth: int) -> str:
    domains: list[str] = ["seznam.cz", "email.cz", "gmail.com", "outlook.com"]
    dot_between_names: str = "." if random() > .5 else ""
    include_number: bool = bool(randint(0, 1))
    number: str = ""
    if include_number:
        if random() > .5:
            number = str(year_of_birth)[:randint(1, 2) * 2]
        else:
            number = str(randint(0, 99))
    result: str = f"{base_letters(first_name)}{dot_between_names}{base_letters(last_name)}{number}@{choice(domains)}"
    if random() > .5:
        result = result.lower()
    return result


def generate(amount: int = 100) -> None:
    data: list[str] = []
    gen = faker.Faker("cs_CZ")
    for i in range(amount):
        first_name = gen.first_name_male() if i < amount // 2 else gen.first_name_female()
        last_name = gen.last_name_male() if i < amount // 2 else gen.last_name_female()
        year = gen.date_of_birth(minimum_age=18).year
        email = get_email(first_name, last_name, year)
        password = gen.password(randint(10, 16), True, True, True, True)
        balance = randint(1000, 200_000)
        account_number: str = get_account_number()
        data.append(f"{account_number},{last_name},{first_name},{email},{password},{balance},CZK")

    with open(file="accounts.txt", mode="w", encoding="utf-8") as f:
        f.write("\n".join(sorted(data, key=lambda x: int(x.split("/")[0]))))
