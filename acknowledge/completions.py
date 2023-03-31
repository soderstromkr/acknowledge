#helper vars

# keys to extract information 
keys='funding agencies (FUND), grant numbers (GRNB), \
facilities or universities or labs (INFRA), beamlines (BEAM), \
individuals with full names (IND), and type of assistance (TYPE)'

# few shot learning mapping
prompt_1 = 'Open Access funding provided by Projekt DEAL. The authors gratefully acknowledge the support of Dr. Olaf Medenbach for performing the pre-preparation and Mr. Maximilian Kruth, Forschungszentrum Julich, Ernst Ruska-Centre for Microscopy and Spectroscopy with Electrons (ER-C) for the fine-tuning of the SXNT sample. The authors would like to thank Dr. Robert Mucke, Forschungszentrum Julich, Institute of Energy and Climate Research: Materials Synthesis and Processing (IEK-1) for the data management and assisting with the analyses of the tomograms. We gratefully acknowledge the German Federal Ministry of Education and Research (BMBF) for financing of the project Verbundvorhaben SOFC Degradation (Proposal Number 03SF0494A) and the ESRF for its financial support under MA-3254 experiment at the ID16B beamline.'

completion_1 = {
    "FUND": "Projekt DEAL|German Federal Ministry of Education and Research (BMBF)|ESRF",
    "IND": "Dr. Olaf Medenbach|Mr. Maximilian Kruth|Dr. Robert Mucke",
    "INFRA": "Forschungszentrum Julich|Ernst Ruska-Centre for Microscopy and Spectroscopy with Electrons (ER-C)|Institute of Energy and Climate Research: Materials Synthesis and Processing (IEK-1)",
    "BEAM": "ID16B",
    "GRNB": "03SF0494A",
    "TYPE": "open access funding|performing preparation|fine-tuning of the SXNT sample|data management and assisting with analysis|financing the project|financial support"
    }

prompt_2 = 'ESRF and Knut and Alice Wallenberg Foundation (KAW 2014.0052).'

completion_2 = {
    "FUND": "Alice Wallenberg Foundation",
    "IND": "NaN",
    "INFRA": "ESRF",
    "BEAM": "NaN",
    "GRNB": "KAW 2014.0052",
    "TYPE": "NaN"
    }

prompt_3 = 'Financial support from the European Union within the framework of the H2020 project Nanoscience Foundries and Fine Analysis (NFFA), grant no. 654360, and the use of the FIB dual beam instrument granted by BMBF under grant 5K13WC3 (PT-DESY) is gratefully acknowledged. Y.Y.K., D.D., S.L., L.G., and I.A.V. acknowledge the support by the Helmholtz Associations Initiative and Networking Fund and the Russian Science Foundation (Project No. 18-41-06001).'

completion_3 = {
    "FUND": "European Union NFFA|Helmholtz Associations Initiative and Networking Fund|Russian Science Foundation",
    "IND": "PT-DESY",
    "INFRA": "",
    "BEAM": "FIB dual beam",
    "GRNB": "NFFA 654360|5K13WC3|18-41-06001",
    "TYPE": "financial support|use of instrument|support"
    }

error_completion = {
    "FUND": "NaN",
    "IND": "NaN",
    "INFRA": "NaN",
    "BEAM": "NaN",
    "GRNB": "NaN",
    "TYPE": "NaN"
    }

# instructions 
instructions = 'Extract the following data: {} in JSON format, use "NaN" if none found. From the following text: '.format(keys)
