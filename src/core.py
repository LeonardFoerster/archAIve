import requests
import feedparser
from transformers import pipeline

ARXIV_CATEGORIES = {
    # --- Computer Science (cs) ---
    "cs.AI - Artificial Intelligence": "cs.AI",
    "cs.AR - Hardware Architecture": "cs.AR",
    "cs.CC - Computational Complexity": "cs.CC",
    "cs.CE - Computational Engineering, Finance, and Science": "cs.CE",
    "cs.CG - Computational Geometry": "cs.CG",
    "cs.CL - Computation and Language (NLP)": "cs.CL",
    "cs.CR - Cryptography and Security": "cs.CR",
    "cs.CV - Computer Vision and Pattern Recognition": "cs.CV",
    "cs.CY - Computers and Society": "cs.CY",
    "cs.DB - Databases": "cs.DB",
    "cs.DC - Distributed, Parallel, and Cluster Computing": "cs.DC",
    "cs.DL - Digital Libraries": "cs.DL",
    "cs.DM - Discrete Mathematics": "cs.DM",
    "cs.DS - Data Structures and Algorithms": "cs.DS",
    "cs.ET - Emerging Technologies": "cs.ET",
    "cs.FL - Formal Languages and Automata Theory": "cs.FL",
    "cs.GL - General Literature": "cs.GL",
    "cs.GR - Graphics": "cs.GR",
    "cs.GT - Computer Science and Game Theory": "cs.GT",
    "cs.HC - Human-Computer Interaction": "cs.HC",
    "cs.IR - Information Retrieval": "cs.IR",
    "cs.IT - Information Theory": "cs.IT",
    "cs.LG - Machine Learning": "cs.LG",
    "cs.LO - Logic in Computer Science": "cs.LO",
    "cs.MA - Multiagent Systems": "cs.MA",
    "cs.MM - Multimedia": "cs.MM",
    "cs.MS - Mathematical Software": "cs.MS",
    "cs.NA - Numerical Analysis": "cs.NA",
    "cs.NE - Neural and Evolutionary Computing": "cs.NE",
    "cs.NI - Networking and Internet Architecture": "cs.NI",
    "cs.OH - Other Computer Science": "cs.OH",
    "cs.OS - Operating Systems": "cs.OS",
    "cs.PF - Performance": "cs.PF",
    "cs.PL - Programming Languages": "cs.PL",
    "cs.RO - Robotics": "cs.RO",
    "cs.SC - Symbolic Computation": "cs.SC",
    "cs.SD - Sound": "cs.SD",
    "cs.SE - Software Engineering": "cs.SE",
    "cs.SI - Social and Information Networks": "cs.SI",
    "cs.SY - Systems and Control": "cs.SY",

    # --- Economics (econ) ---
    "econ.EM - Econometrics": "econ.EM",
    "econ.GN - General Economics": "econ.GN",
    "econ.TH - Theoretical Economics": "econ.TH",

    # --- Electrical Engineering and Systems Science (eess) ---
    "eess.AS - Audio and Speech Processing": "eess.AS",
    "eess.IV - Image and Video Processing": "eess.IV",
    "eess.SP - Signal Processing": "eess.SP",
    "eess.SY - Systems and Control": "eess.SY",

    # --- Mathematics (math) ---
    "math.AC - Commutative Algebra": "math.AC",
    "math.AG - Algebraic Geometry": "math.AG",
    "math.AP - Analysis of PDEs": "math.AP",
    "math.AT - Algebraic Topology": "math.AT",
    "math.CA - Classical Analysis and ODEs": "math.CA",
    "math.CO - Combinatorics": "math.CO",
    "math.CT - Category Theory": "math.CT",
    "math.CV - Complex Variables": "math.CV",
    "math.DG - Differential Geometry": "math.DG",
    "math.DS - Dynamical Systems": "math.DS",
    "math.FA - Functional Analysis": "math.FA",
    "math.GM - General Mathematics": "math.GM",
    "math.GN - General Topology": "math.GN",
    "math.GR - Group Theory": "math.GR",
    "math.GT - Geometric Topology": "math.GT",
    "math.HO - History and Overview": "math.HO",
    "math.IT - Information Theory": "math.IT",
    "math.KT - K-Theory and Homology": "math.KT",
    "math.LO - Logic": "math.LO",
    "math.MG - Metric Geometry": "math.MG",
    "math.MP - Mathematical Physics": "math.MP",
    "math.NA - Numerical Analysis": "math.NA",
    "math.NT - Number Theory": "math.NT",
    "math.OA - Operator Algebras": "math.OA",
    "math.OC - Optimization and Control": "math.OC",
    "math.PR - Probability": "math.PR",
    "math.QA - Quantum Algebra": "math.QA",
    "math.RA - Rings and Algebras": "math.RA",
    "math.RT - Representation Theory": "math.RT",
    "math.SG - Symplectic Geometry": "math.SG",
    "math.SP - Spectral Theory": "math.SP",
    "math.ST - Statistics Theory": "math.ST",

    # --- Physics ---
    "astro-ph.CO - Cosmology and Nongalactic Astrophysics": "astro-ph.CO",
    "astro-ph.EP - Earth and Planetary Astrophysics": "astro-ph.EP",
    "astro-ph.GA - Astrophysics of Galaxies": "astro-ph.GA",
    "astro-ph.HE - High Energy Astrophysical Phenomena": "astro-ph.HE",
    "astro-ph.IM - Instrumentation and Methods for Astrophysics": "astro-ph.IM",
    "astro-ph.SR - Solar and Stellar Astrophysics": "astro-ph.SR",
    "cond-mat.dis-nn - Disordered Systems and Neural Networks": "cond-mat.dis-nn",
    "cond-mat.mes-hall - Mesoscale and Nanoscale Physics": "cond-mat.mes-hall",
    "cond-mat.mtrl-sci - Materials Science": "cond-mat.mtrl-sci",
    "cond-mat.other - Other Condensed Matter": "cond-mat.other",
    "cond-mat.quant-gas - Quantum Gases": "cond-mat.quant-gas",
    "cond-mat.soft - Soft Condensed Matter": "cond-mat.soft",
    "cond-mat.stat-mech - Statistical Mechanics": "cond-mat.stat-mech",
    "cond-mat.str-el - Strongly Correlated Electrons": "cond-mat.str-el",
    "cond-mat.supr-con - Superconductivity": "cond-mat.supr-con",
    "gr-qc - General Relativity and Quantum Cosmology": "gr-qc",
    "hep-ex - High Energy Physics - Experiment": "hep-ex",
    "hep-lat - High Energy Physics - Lattice": "hep-lat",
    "hep-ph - High Energy Physics - Phenomenology": "hep-ph",
    "hep-th - High Energy Physics - Theory": "hep-th",
    "math-ph - Mathematical Physics": "math-ph",
    "nlin.AO - Adaptation and Self-Organizing Systems": "nlin.AO",
    "nlin.CD - Chaotic Dynamics": "nlin.CD",
    "nlin.CG - Cellular Automata and Lattice Gases": "nlin.CG",
    "nlin.PS - Pattern Formation and Solitons": "nlin.PS",
    "nlin.SI - Exactly Solvable and Integrable Systems": "nlin.SI",
    "nucl-ex - Nuclear Experiment": "nucl-ex",
    "nucl-th - Nuclear Theory": "nucl-th",
    "physics.acc-ph - Accelerator Physics": "physics.acc-ph",
    "physics.ao-ph - Atmospheric and Oceanic Physics": "physics.ao-ph",
    "physics.app-ph - Applied Physics": "physics.app-ph",
    "physics.atm-clus - Atomic and Molecular Clusters": "physics.atm-clus",
    "physics.atom-ph - Atomic Physics": "physics.atom-ph",
    "physics.bio-ph - Biological Physics": "physics.bio-ph",
    "physics.chem-ph - Chemical Physics": "physics.chem-ph",
    "physics.class-ph - Classical Physics": "physics.class-ph",
    "physics.comp-ph - Computational Physics": "physics.comp-ph",
    "physics.data-an - Data Analysis, Statistics and Probability": "physics.data-an",
    "physics.ed-ph - Physics Education": "physics.ed-ph",
    "physics.flu-dyn - Fluid Dynamics": "physics.flu-dyn",
    "physics.gen-ph - General Physics": "physics.gen-ph",
    "physics.geo-ph - Geophysics": "physics.geo-ph",
    "physics.hist-ph - History and Philosophy of Physics": "physics.hist-ph",
    "physics.ins-det - Instrumentation and Detectors": "physics.ins-det",
    "physics.med-ph - Medical Physics": "physics.med-ph",
    "physics.optics - Optics": "physics.optics",
    "physics.plasm-ph - Plasma Physics": "physics.plasm-ph",
    "physics.pop-ph - Popular Physics": "physics.pop-ph",
    "physics.soc-ph - Physics and Society": "physics.soc-ph",
    "physics.space-ph - Space Physics": "physics.space-ph",
    "quant-ph - Quantum Physics": "quant-ph",

    # --- Quantitative Biology (q-bio) ---
    "q-bio.BM - Biomolecules": "q-bio.BM",
    "q-bio.CB - Cell Behavior": "q-bio.CB",
    "q-bio.GN - Genomics": "q-bio.GN",
    "q-bio.MN - Molecular Networks": "q-bio.MN",
    "q-bio.NC - Neurons and Cognition": "q-bio.NC",
    "q-bio.OT - Other Quantitative Biology": "q-bio.OT",
    "q-bio.PE - Populations and Evolution": "q-bio.PE",
    "q-bio.QM - Quantitative Methods": "q-bio.QM",
    "q-bio.SC - Subcellular Processes": "q-bio.SC",
    "q-bio.TO - Tissues and Organs": "q-bio.TO",

    # --- Quantitative Finance (q-fin) ---
    "q-fin.CP - Computational Finance": "q-fin.CP",
    "q-fin.EC - Economics": "q-fin.EC",
    "q-fin.GN - General Finance": "q-fin.GN",
    "q-fin.MF - Mathematical Finance": "q-fin.MF",
    "q-fin.PM - Portfolio Management": "q-fin.PM",
    "q-fin.PR - Pricing of Securities": "q-fin.PR",
    "q-fin.RM - Risk Management": "q-fin.RM",
    "q-fin.ST - Statistical Finance": "q-fin.ST",
    "q-fin.TR - Trading and Market Microstructure": "q-fin.TR",

    # --- Statistics (stat) ---
    "stat.AP - Applications": "stat.AP",
    "stat.CO - Computation": "stat.CO",
    "stat.ME - Methodology": "stat.ME",
    "stat.ML - Machine Learning": "stat.ML",
    "stat.OT - Other Statistics": "stat.OT",
    "stat.TH - Theory": "stat.TH",
}

def create_summarizer():
    """Creates and returns the summarization pipeline model."""
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def fetch_arxiv_papers(category='cs.LG', max_results=5):
    """Fetches and parses paper data from the arXiv API for a given category."""
    url = f'http://export.arxiv.org/api/query?search_query=cat:{category}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        return feed.entries
    except requests.RequestException as e:
        print(f"Error: Failed to fetch data from arXiv. {e}")
        return []

def summarize_text(text, summarizer):
    """Summarizes a given piece of text using the loaded AI model."""
    if not text:
        return "No text provided to summarize."
    summary = summarizer(text[:1024], max_length=150, min_length=75, do_sample=False)
    return summary[0]['summary_text']
