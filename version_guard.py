import sys

def check():
    MIN_VERSION = (3, 10)

    if sys.version_info < MIN_VERSION:
        print("\n" + "="*60)
        print("ZASTARALÁ VERZE PYTHONU!")
        print("="*60)
        print(f"Aktuálně používáte verzi: {sys.version_info.major}.{sys.version_info.minor}")
        print(f"Tento projekt vyžaduje alespoň Python {MIN_VERSION[0]}.{MIN_VERSION[1]} nebo novější.")
        print("\nProsím, nainstalujte novější verzi (např. 3.14 z Microsoft Store).")
        print("Postupujte podle instrukcí v souboru README.md.")
        print("="*60 + "\n")
        sys.exit(1)
