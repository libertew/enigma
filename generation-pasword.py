
#!/usr/bin/env python3
"""
╔═══════════════════════════════════════╗
║         ŞİFRE ÜRETİCİ v1.0           ║
║   16 | 32 | 256 karakter desteği     ║
╚═══════════════════════════════════════╝
"""

import secrets
import string
import argparse
import sys


class Renk:
    KIRMIZI   = "\033[91m"
    YESIL     = "\033[92m"
    SARI      = "\033[93m"
    MAVI      = "\033[94m"
    MAGENTA   = "\033[95m"
    CYAN      = "\033[96m"
    BEYAZ     = "\033[97m"
    KALIN     = "\033[1m"
    SIFIRLA   = "\033[0m"

GECERLI_UZUNLUKLAR = [16, 32, 256]

KARAKTER_SETLERI = {
    "harf":   string.ascii_letters,
    "rakam":  string.digits,
    "ozel":   string.punctuation,
}


def sifre_uret(uzunluk: int, buyuk: bool, kucuk: bool, rakam: bool, ozel: bool) -> str:
    """Belirtilen uzunluk ve karakter seçeneklerine göre güvenli şifre üretir."""
    alfabe = ""
    zorunlu = []

    if buyuk:
        alfabe += string.ascii_uppercase
        zorunlu.append(secrets.choice(string.ascii_uppercase))
    if kucuk:
        alfabe += string.ascii_lowercase
        zorunlu.append(secrets.choice(string.ascii_lowercase))
    if rakam:
        alfabe += string.digits
        zorunlu.append(secrets.choice(string.digits))
    if ozel:
        alfabe += string.punctuation
        zorunlu.append(secrets.choice(string.punctuation))

    if not alfabe:
        print(f"{Renk.KIRMIZI}Hata: En az bir karakter türü seçmelisiniz!{Renk.SIFIRLA}")
        sys.exit(1)

    # Kalan karakterleri rastgele doldur
    kalan = uzunluk - len(zorunlu)
    sifreli = zorunlu + [secrets.choice(alfabe) for _ in range(kalan)]

    # Listeyi karıştır
    secrets.SystemRandom().shuffle(sifreli)
    return "".join(sifreli)


def baslik_yazdir():
    print(f"""
{Renk.CYAN}{Renk.KALIN}╔═══════════════════════════════════════════╗
║          🔐  ŞİFRE ÜRETİCİ  v1.0         ║
║      Güvenli | Hızlı | Kriptografik       ║
╚═══════════════════════════════════════════╝{Renk.SIFIRLA}
""")


def guc_seviyesi(uzunluk: int) -> str:
    if uzunluk == 16:
        return f"{Renk.SARI}●●●○○  Orta{Renk.SIFIRLA}"
    elif uzunluk == 32:
        return f"{Renk.YESIL}●●●●○  Güçlü{Renk.SIFIRLA}"
    elif uzunluk == 256:
        return f"{Renk.MAVI}●●●●●  Ultra Güçlü{Renk.SIFIRLA}"
    return "Bilinmiyor"


def sifre_yazdir(sifre: str, uzunluk: int, adet: int):
    print(f"{Renk.KALIN}{'─' * 50}{Renk.SIFIRLA}")
    print(f"  {Renk.MAGENTA}Uzunluk :{Renk.SIFIRLA} {uzunluk} karakter")
    print(f"  {Renk.MAGENTA}Güç     :{Renk.SIFIRLA} {guc_seviyesi(uzunluk)}")
    print(f"  {Renk.MAGENTA}Adet    :{Renk.SIFIRLA} {adet}")
    print(f"{Renk.KALIN}{'─' * 50}{Renk.SIFIRLA}")

    for i in range(adet):
        s = sifre_uret(uzunluk, True, True, True, True) if sifre is None else sifre
        if adet > 1:
            s = sifre_uret(uzunluk, True, True, True, True)
        numara = f"{Renk.CYAN}[{i+1:02d}]{Renk.SIFIRLA} " if adet > 1 else "  ➤  "
        print(f"{numara}{Renk.YESIL}{Renk.KALIN}{s}{Renk.SIFIRLA}")

    print(f"{Renk.KALIN}{'─' * 50}{Renk.SIFIRLA}\n")


def interaktif_mod():
    """Argüman verilmezse interaktif mod başlar."""
    baslik_yazdir()
    print(f"{Renk.BEYAZ}Şifre uzunluğunu seçin:{Renk.SIFIRLA}")
    print(f"  {Renk.CYAN}1{Renk.SIFIRLA}) 16  karakter  {Renk.SARI}(Orta Güç){Renk.SIFIRLA}")
    print(f"  {Renk.CYAN}2{Renk.SIFIRLA}) 32  karakter  {Renk.YESIL}(Güçlü){Renk.SIFIRLA}")
    print(f"  {Renk.CYAN}3{Renk.SIFIRLA}) 256 karakter  {Renk.MAVI}(Ultra Güçlü){Renk.SIFIRLA}")
    print(f"  {Renk.CYAN}4{Renk.SIFIRLA}) Hepsini üret")
    print()

    secim = input(f"{Renk.MAGENTA}Seçiminiz (1-4): {Renk.SIFIRLA}").strip()

    secim_map = {"1": [16], "2": [32], "3": [256], "4": [16, 32, 256]}
    if secim not in secim_map:
        print(f"{Renk.KIRMIZI}Geçersiz seçim!{Renk.SIFIRLA}")
        sys.exit(1)

    uzunluklar = secim_map[secim]

    adet_str = input(f"{Renk.MAGENTA}Kaç adet üretilsin? (varsayılan: 1): {Renk.SIFIRLA}").strip()
    adet = int(adet_str) if adet_str.isdigit() and int(adet_str) > 0 else 1

    print()
    for uzunluk in uzunluklar:
        sifre_yazdir(None, uzunluk, adet)

    print(f"{Renk.YESIL}✓ Şifreler kriptografik olarak güvenli (secrets modülü) üretildi.{Renk.SIFIRLA}")


def main():
    parser = argparse.ArgumentParser(
        prog="sifre_uretici",
        description="🔐 Güvenli şifre üretici — 16, 32 veya 256 karakter",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Örnekler:
  python sifre_uretici.py -u 16
  python sifre_uretici.py -u 32 -a 5
  python sifre_uretici.py -u 256 -a 3
  python sifre_uretici.py --hepsi
  python sifre_uretici.py                  (interaktif mod)
"""
    )

    parser.add_argument(
        "-u", "--uzunluk",
        type=int,
        choices=GECERLI_UZUNLUKLAR,
        metavar="UZUNLUK",
        help="Şifre uzunluğu: 16, 32 veya 256"
    )
    parser.add_argument(
        "-a", "--adet",
        type=int,
        default=1,
        metavar="ADET",
        help="Üretilecek şifre adedi (varsayılan: 1)"
    )
    parser.add_argument(
        "--hepsi",
        action="store_true",
        help="16, 32 ve 256 karakterlik şifreleri aynı anda üret"
    )
    parser.add_argument(
        "--sessiz",
        action="store_true",
        help="Sadece şifreyi yazdır (script entegrasyonu için)"
    )

    
    if len(sys.argv) == 1:
        interaktif_mod()
        return

    args = parser.parse_args()

    if not args.uzunluk and not args.hepsi:
        parser.print_help()
        sys.exit(1)

    uzunluklar = GECERLI_UZUNLUKLAR if args.hepsi else [args.uzunluk]

    if args.sessiz:
        
        for uzunluk in uzunluklar:
            for _ in range(args.adet):
                print(sifre_uret(uzunluk, True, True, True, True))
        return

    baslik_yazdir()
    for uzunluk in uzunluklar:
        sifre_yazdir(None, uzunluk, args.adet)

    print(f"{Renk.YESIL}✓ Şifreler kriptografik olarak güvenli (secrets modülü) üretildi.{Renk.SIFIRLA}\n")


if __name__ == "__main__":
    main()


