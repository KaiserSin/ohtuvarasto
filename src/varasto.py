"""Varasto module that implements a simple bounded storage."""


class Varasto:
    """Store items with a fixed capacity and saldo limits."""

    def __init__(self, tilavuus, alku_saldo=0):
        """Create a new storage while clamping invalid inputs."""
        self.tilavuus = max(0.0, tilavuus)
        self.saldo = self._clamped_saldo(alku_saldo)

    def _clamped_saldo(self, alku_saldo):
        """Return saldo constrained between zero and capacity."""
        if alku_saldo < 0.0:
            return 0.0
        if alku_saldo <= self.tilavuus:
            return alku_saldo
        return self.tilavuus

    def paljonko_mahtuu(self):
        """Count remaining capacity without storing duplicate state."""
        return self.tilavuus - self.saldo

    def lisaa_varastoon(self, maara):
        """Increase saldo but never exceed capacity."""
        if maara < 0:
            return
        if maara <= self.paljonko_mahtuu():
            self.saldo = self.saldo + maara
        else:
            self.saldo = self.tilavuus

    def ota_varastosta(self, maara):
        """Withdraw saldo but never return negative amounts."""
        if maara < 0:
            return 0.0
        if maara > self.saldo:
            kaikki_mita_voidaan = self.saldo
            self.saldo = 0.0

            return kaikki_mita_voidaan

        self.saldo = self.saldo - maara

        return maara

    def __str__(self):
        """Represent the storage state as a string."""
        return f"saldo = {self.saldo}, vielä tilaa {self.paljonko_mahtuu()}"
