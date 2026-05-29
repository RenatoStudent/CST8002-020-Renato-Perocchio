class PreyRecord:
    def __init__(self, year, species, common_name, study_site, associated_community, lat, long, 
            delta13C, delta13Cc, deltaN, deltaNc, tp, cn, astaxanthin, canthaxanthin, retinol):
        self.year =  year
        self.species = species
        self.common_name = common_name
        self.study_site = study_site
        self.associated_community = associated_community
        self.lat = lat
        self.long = long
        self.delta13C = delta13C
        self.delta13Cc = delta13Cc
        self.deltaN = deltaN
        self.deltaNc = deltaNc
        self.tp = tp
        self.cn = cn
        self.astaxanthin = astaxanthin
        self.canthaxanthin = canthaxanthin
        self.retinol = retinol
