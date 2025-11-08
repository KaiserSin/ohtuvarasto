"""Command-line demonstration for the Varasto class."""
from varasto import Varasto


def initialize_varastot():
    """Create the demo storages for juice and beer."""
    return Varasto(100.0), Varasto(100.0, 20.2)


def show_initial_state(mehua, olutta):
    """Print the storages right after initialization."""
    print("Luonnin jälkeen:")
    print(f"Mehuvarasto: {mehua}")
    print(f"Olutvarasto: {olutta}")


def show_getters(olutta):
    """Inspect Olut-varasto getter values."""
    print("Olut getterit:")
    print(f"saldo = {olutta.saldo}")
    print(f"tilavuus = {olutta.tilavuus}")
    print(f"paljonko_mahtuu = {olutta.paljonko_mahtuu()}")


def adjust_mehu(mehua):
    """Exercise valid adjustments on the juice storage."""
    print("Mehu setterit:")
    print("Lisätään 50.7")
    mehua.lisaa_varastoon(50.7)
    print(f"Mehuvarasto: {mehua}")
    print("Otetaan 3.14")
    mehua.ota_varastosta(3.14)
    print(f"Mehuvarasto: {mehua}")


def show_error_cases():
    """Demonstrate invalid constructor arguments."""
    print("Virhetilanteita:")
    print("Varasto(-100.0);")
    huono = Varasto(-100.0)
    print(huono)
    print("Varasto(100.0, -50.7)")
    huono = Varasto(100.0, -50.7)
    print(huono)


def demonstrate_overfill(olutta):
    """Show that overfilling caps saldo to capacity."""
    print(f"Olutvarasto: {olutta}")
    print("olutta.lisaa_varastoon(1000.0)")
    olutta.lisaa_varastoon(1000.0)
    print(f"Olutvarasto: {olutta}")


def demonstrate_invalid_addition(mehua):
    """Show that negative additions are ignored."""
    print(f"Mehuvarasto: {mehua}")
    print("mehua.lisaa_varastoon(-666.0)")
    mehua.lisaa_varastoon(-666.0)
    print(f"Mehuvarasto: {mehua}")


def demonstrate_excess_withdrawal(olutta):
    """Show that withdrawing too much returns only available amount."""
    print(f"Olutvarasto: {olutta}")
    print("olutta.ota_varastosta(1000.0)")
    saatiin = olutta.ota_varastosta(1000.0)
    print(f"saatiin {saatiin}")
    print(f"Olutvarasto: {olutta}")


def demonstrate_negative_withdrawal(mehua):
    """Show that negative withdrawals produce zero."""
    print(f"Mehuvarasto: {mehua}")
    print("mehua.otaVarastosta(-32.9)")
    saatiin = mehua.ota_varastosta(-32.9)
    print(f"saatiin {saatiin}")
    print(f"Mehuvarasto: {mehua}")


def main():
    """Run the full Varasto demonstration."""
    mehua, olutta = initialize_varastot()
    show_initial_state(mehua, olutta)
    show_getters(olutta)
    adjust_mehu(mehua)
    show_error_cases()
    demonstrate_overfill(olutta)
    demonstrate_invalid_addition(mehua)
    demonstrate_excess_withdrawal(olutta)
    demonstrate_negative_withdrawal(mehua)


if __name__ == "__main__":
    main()
