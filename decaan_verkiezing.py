from abc import ABC, abstractmethod
from verkiezing import Kandidaat, Stem, Kiezer

# Bestaande Decaan-klassen uit de les
class DecaanKandidaat(Kandidaat):
    def __init__(self, naam, opleiding):
        super().__init__(naam)
        self.opleiding = opleiding

    def __str__(self):
        return f"{self.naam} ({self.opleiding})"
    
class DecaanStem(Stem):
    def __init__(self, kandidaat, opleiding):
        super().__init__(kandidaat)
        self.opleiding = opleiding

    def __str__(self):
        return f"Stem op {self.kandidaat} ({self.opleiding})"
    
class DecaanKiezer(Kiezer):
    def __init__(self, naam, opleiding):
        super().__init__(naam)
        self.opleiding = opleiding

    def stem(self, kandidaat):
        if kandidaat.opleiding == self.opleiding:
            stem = DecaanStem(kandidaat, self.opleiding)
            kandidaat.geef_stem(stem)
            print(f"{self.naam} heeft gestemd op {kandidaat} ({self.opleiding})")
        else:
            print(f"{self.naam} kan niet stemmen op {kandidaat} ({kandidaat.opleiding})")

# 1. Abstracte basis voor verkiezingen
class Verkiezing(ABC):
    def __init__(self):
        self._kandidaten = []  # ingekapselde lijst van kandidaten

    def voeg_kandidaat_toe(self, kandidaat: Kandidaat):
        """Voeg een kandidaat toe aan de verkiezing."""
        self._kandidaten.append(kandidaat)

    def get_kandidaten(self):
        """Retourneer de lijst van kandidaten (immutable)."""
        return tuple(self._kandidaten)

    @abstractmethod
    def laat_stemmen(self, kiezer: Kiezer, kandidaat: Kandidaat):
        """Laat een kiezer stemmen op een kandidaat."""
        raise NotImplementedError

    def get_resultaten(self):
        """Geef een dict terug met kandidaten en hun aantal stemmen."""
        # Gebruik len(kandidaat.stemmen) omdat de basis-Kandidaat geen aantal_stemmen methode heeft
        return {k: len(k.stemmen) for k in self._kandidaten}

# 2. Concrete decaanverkiezing
class DecaanVerkiezing(Verkiezing):
    def laat_stemmen(self, kiezer: DecaanKiezer, kandidaat: DecaanKandidaat):
        """Laat een decaankiezer stemmen via de bestaande stem-logica."""
        kiezer.stem(kandidaat)

# 3. Demonstratie: lijst van kandidaten en kiezers, en stemronde
if __name__ == "__main__":
    import random

    # Maak kandidatenlijst
    kandidaten = [
        DecaanKandidaat("Alice", "Informatica"),
        DecaanKandidaat("Bob", "Wiskunde"),
        DecaanKandidaat("Charlie", "Informatica")
    ]

    # Maak kiezerslijst
    kiezers = [
        DecaanKiezer("Student1", "Informatica"),
        DecaanKiezer("Student2", "Wiskunde"),
        DecaanKiezer("Student3", "Informatica"),
        DecaanKiezer("Student4", "Fysica")
    ]

    # Initialiseer verkiezing en voeg kandidaten toe
    verkiezing = DecaanVerkiezing()
    for kandidaat in kandidaten:
        verkiezing.voeg_kandidaat_toe(kandidaat)

    # Laat alle kiezers stemmen
    for kiezer in kiezers:
        # Kies een kandidaat binnen eigen opleiding als mogelijk
        mogelijke = [c for c in kandidaten if c.opleiding == kiezer.opleiding]
        keuze = random.choice(mogelijke) if mogelijke else random.choice(kandidaten)
        verkiezing.laat_stemmen(kiezer, keuze)

    # Print de verkiezingsresultaten
    print("\nResultaten decaanverkiezing:")
    for kandidaat, stemmen in verkiezing.get_resultaten().items():
        print(f"{kandidaat}: {stemmen} stemmen")
