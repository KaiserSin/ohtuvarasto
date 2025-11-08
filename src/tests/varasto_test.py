"""Unit tests for the Varasto storage class."""

import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    """Test suite that exercises Varasto edge cases and core behavior."""

    def setUp(self):
        """Create a baseline storage for reuse."""
        self.varasto = Varasto(10)

    def test_saldo_tilavuus_nollataan(self):
        """Negative constructor arguments are clamped to zero."""
        v = Varasto(-1, -1)
        self.assertAlmostEqual(v.tilavuus, 0.0)
        self.assertAlmostEqual(v.saldo, 0.0)

    def test_saldo_enemman_tilavuus(self):
        """Saldo cannot exceed capacity even at construction time."""
        v = Varasto(8, 10)
        self.assertAlmostEqual(v.saldo, 8)

    def test_lisaa_varastoon_neg(self):
        """Negative additions are ignored."""
        self.varasto.lisaa_varastoon(-3)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_lisaa_varastoon_enemman_tilavuus(self):
        """Adding more than fits caps saldo to capacity."""
        self.varasto.lisaa_varastoon(11)
        self.assertAlmostEqual(self.varasto.saldo, 10)

    def test_ota_varastosta_neg(self):
        """Negative withdrawals do not change saldo."""
        self.varasto.ota_varastosta(-2)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_ota_varastosta_enemman_saldo(self):
        """Withdrawing too much returns everything available."""
        self.varasto.lisaa_varastoon(5)
        saatu = self.varasto.ota_varastosta(7)
        self.assertAlmostEqual(saatu, 5.0)
        self.assertAlmostEqual(self.varasto.saldo, 0.0)

    def test_str_muoto(self):
        """__str__ reports saldo and remaining space."""
        self.assertEqual(str(self.varasto), "saldo = 0, vielä tilaa 10")

    def test_konstruktori_luo_tyhjan_varaston(self):
        """Constructor initializes saldo to zero."""
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        """Constructor stores the declared capacity."""
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        """Adding items increases saldo."""
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        """Adding items reduces the free capacity."""
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        """Withdrawing returns the requested amount when possible."""
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        """Withdrawing frees up storage."""
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)
