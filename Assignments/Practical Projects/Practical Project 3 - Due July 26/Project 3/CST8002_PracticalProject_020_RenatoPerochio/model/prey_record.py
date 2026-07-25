# ============================================================
# Course:      CST8002 - Programming Language Research Project
# Professor:   Stanley Pieda
# Due Date:    July 26, 2026
# Author:      Renato Perocchio
# References:
#   [1] Python Software Foundation. (2024). Classes. docs.python.org.
#       [online] Available at: https://docs.python.org/3/tutorial/classes.html
#       [Accessed on June 19, 2026]
#   [2] CoderPad. (2024). Classes & OOP in Python. coderpad.io.
#       [online] Available at: https://coderpad.io/blog/development/classes-object-oriented-programming-python/
#       [Accessed on June 19, 2026]
# ============================================================

"""
Defines the PreyRecord class, a data record object representing a single row
from the prey collection and analysis dataset.
"""


class PreyRecord:
    """
    A record object representing one entry from the prey collection and analysis
    dataset. Each field corresponds to a column in the source CSV file.
    """

    def __init__(self, year, species, common_name, study_site, associated_community,
                 lat, long, delta13C, delta13Cc, delta15N, delta15Nc,
                 tp, cn, astaxanthin, canthaxanthin, retinol):
        """
        Initializes a PreyRecord with all 16 fields from the dataset.

        Args:
            year: The year the sample was collected.
            species: The scientific species name.
            common_name: The common name of the species.
            study_site: The location where the sample was collected.
            associated_community: The associated community name.
            lat: Latitude of the study site.
            long: Longitude of the study site.
            delta13C: Raw delta 13C isotope value.
            delta13Cc: Corrected delta 13C isotope value.
            delta15N: Raw delta 15N isotope value.
            delta15Nc: Corrected delta 15N isotope value.
            tp: Trophic position value.
            cn: Carbon to nitrogen ratio.
            astaxanthin: Astaxanthin concentration in mg/kg.
            canthaxanthin: Canthaxanthin concentration in mg/kg.
            retinol: Retinol concentration in mg/kg.
        """
        self.year = year
        self.species = species
        self.common_name = common_name
        self.study_site = study_site
        self.associated_community = associated_community
        self.lat = lat
        self.long = long
        self.delta13C = delta13C
        self.delta13Cc = delta13Cc
        self.delta15N = delta15N
        self.delta15Nc = delta15Nc
        self.tp = tp
        self.cn = cn
        self.astaxanthin = astaxanthin
        self.canthaxanthin = canthaxanthin
        self.retinol = retinol
