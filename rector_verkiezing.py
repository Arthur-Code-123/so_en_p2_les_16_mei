from abc import ABC, abstractmethod
from verkiezing import Kandidaat, Stem, Kiezer

# -----------------------------
# Abstracte basis voor verkiezingen
# -----------------------------
class Verkiezing(ABC):
    def __init__(self):
        self._kandidaten = []  # ingekapselde lijst van kandidaten

    def voeg_kandidaat_toe(self, kandidaat: Kandidaat):
        """Voeg een kandidaat toe aan de verkiezing."""
        self._kandidaten.append(kandidaat)

    def get_kandidaten(self):
        """Retourneer immutable tuple van kandidaten."""
        return tuple(self._kandidaten)

    @abstractmethod
    def laat_stemmen(self, kiezer: Kiezer, kandidaat: Kandidaat):
        """Laat een kiezer stemmen op een kandidaat."""
        raise NotImplementedError

    def get_resultaten(self):
        """Geef dict kandidaten → aantal stemmen."""
        return {k: len(k.stemmen) for k in self._kandidaten}


# -----------------------------
# Rectorverkiezing
# -----------------------------
class RectorKandidaat(Kandidaat):
    def __init__(self, naam, faculteit):
        super().__init__(naam)
        self.faculteit = faculteit
    def __str__(self):
        return self.naam

class RectorStem(Stem):
    def __init__(self, kandidaat, faculteit):
        super().__init__(kandidaat)
        self.faculteit = faculteit
    def __str__(self):
        return f"Stem op {self.kandidaat} ({self.faculteit})"

class RectorKiezer(Kiezer):
    def __init__(self, naam, faculteit):
        super().__init__(naam)
        self.faculteit = faculteit

    def stem(self, kandidaat: RectorKandidaat):
        stem = RectorStem(kandidaat, kandidaat.faculteit)
        kandidaat.geef_stem(stem)
        print(f"{self.naam} heeft gestemd op {kandidaat} ({kandidaat.faculteit})")

class RectorVerkiezing(Verkiezing):
    def laat_stemmen(self, kiezer: RectorKiezer, kandidaat: RectorKandidaat):
        kiezer.stem(kandidaat)


# -----------------------------
# Demonstratie rectorverkiezing
# -----------------------------
if __name__ == "__main__":
    import random

    # Kandidatenlijst voor rectorverkiezing
    kandidaten = [
        RectorKandidaat("Eva", "Economie"),
        RectorKandidaat("Frank", "Rechten"),
        RectorKandidaat("Greta", "Economie")
    ]

    # Kiezerslijst voor rectorverkiezing
    kiezers = [
        RectorKiezer("Rectorkiezer1", "Economie"),
        RectorKiezer("Rectorkiezer2", "Rechten"),
        RectorKiezer("Rectorkiezer3", "Geneeskunde"),
        RectorKiezer("Rectorkiezer4", "Economie")
    ]

    # Initialiseer verkiezing en voeg kandidaten toe
    verkiezing = RectorVerkiezing()
    for kandidaat in kandidaten:
        verkiezing.voeg_kandidaat_toe(kandidaat)

    # Laat alle kiezers stemmen (opties over alle kandidaten)
    for kiezer in kiezers:
        keuze = random.choice(kandidaten)
        verkiezing.laat_stemmen(kiezer, keuze)

    # Print de uitslag
    print("\nResultaten rectorverkiezing:")
    for kandidaat, aantal in verkiezing.get_resultaten().items():
        print(f"{kandidaat} ({kandidaat.faculteit}): {aantal} stemmen")