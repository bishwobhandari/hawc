EXTERNAL_LINK = 0
PUBMED = 1
HERO = 2
RIS = 3
DOI = 4
WOS = 5
SCOPUS = 6
EMBASE = 7
REFERENCE_DATABASES = (
    (EXTERNAL_LINK, "External link"),
    (PUBMED, "PubMed"),
    (HERO, "HERO"),
    (RIS, "RIS (EndNote/Reference Manager)"),
    (DOI, "DOI"),
    (WOS, "Web of Science"),
    (SCOPUS, "Scopus"),
    (EMBASE, "Embase"),
)

from pathlib import Path
from hawc.apps.lit.constants import REFERENCE_DATABASES
from hawc.apps.lit.models import Identifiers

for (id, name) in REFERENCE_DATABASES:
    data = Identifiers.objects.filter(database=id).values_list("unique_id", flat=True)
    fn = name.replace("/", "-").replace(" ", "-").lower()
    with open(Path(f"~/Desktop/{fn}.txt").expanduser(), "w") as f:
        f.write("\n".join(sorted(data)))

# use this and review those which aren't caught
# doi https://www.crossref.org/blog/dois-and-matching-regular-expressions/

