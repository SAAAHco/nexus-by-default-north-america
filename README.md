# Nexus by Default: data for Chapter 15

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23148569.svg)](https://doi.org/10.5281/zenodo.23148569)

Supporting data for Ashkanani, Z., & Mohtar, R. H. (2026). *Nexus by Default: How North America Governs Water, Energy, and Food in Practice* (Chapter 15), in an edited volume on the water-energy-food nexus in practice (Taylor & Francis, forthcoming).

The repository contains the coded literature corpus, the typed inventories of trade-offs and synergies, the OpenAlex bibliometric counts with the raw query responses, and the plotted values for each data figure in the chapter.

## Contents

### data/

| File | Contents | Used in |
|---|---|---|
| `Coded corpus - studies (205 records).csv` | One row per coded document: key, year, document type, source, geographic scope, countries, places, representative coordinates, scale, directed linkages, extensions, methods, governance / equity / outcome flags, relevance rating, DOI, and APA reference string | Sections 2.1 and 3.2; Figures 15.3 and 15.4 |
| `Coded corpus - outcome evaluations.csv` | The 31 North American studies that measured the outcome of a policy, program, project, or event after the fact | Sections 3.2 and 6 |
| `Inventory - trade-offs typed.csv` | 379 trade-off items: study key, resources traded off, evidence, magnitude, mechanism type, and observed/modeled status | Section 7; Figure 15.12a |
| `Inventory - synergies typed.csv` | 250 synergy items: study key, measure, evidence, magnitude, conditions, mechanism type, and observed/modeled status | Section 8; Figure 15.12b |
| `OpenAlex annual counts 2010-2026.csv` | Annual counts of articles and reviews naming the water-energy-food nexus: world, by affiliation country, North American affiliation, North American place named, NSF-acknowledged, open access | Section 3.1; Figure 15.2 |
| `OpenAlex top-cited NA works.csv` | The 50 most cited works with a United States, Canadian, or Mexican author affiliation | Section 3.1 |
| `OpenAlex funders NA.csv`, `OpenAlex institutions NA.csv`, `OpenAlex topics *.csv`, `OpenAlex countries *.csv` | Funder, institution, topic-subfield, and country rankings | Section 3.1 |
| `bibliometrics_raw/*.json` | Raw OpenAlex API responses, retrieved October 2 and 4, 2026 | Figure 15.2 caption |
| `Figure 15.n data.csv` | Plotted values for Figures 15.2 to 15.12 | Figure captions |

### code/

`openalex_pull.py` documents the OpenAlex query (title-and-abstract phrase search across the common orderings of the nexus name, article and review types, publication years 2010 to 2026) and the filters used for each series.

## Coding scheme

- `na_scope`: US, CA, MX, Arctic (Alaska and northern Canada), Transboundary, Multi-NA (two or more countries), Global-with-NA (global work with North American content), Non-NA (retained for context only).
- `linkages`: W->E water for energy; E->W energy for water; W->F water for food; E->F energy for food; FL->E food and land for energy; F->W food-system effects on water; WEF-all studies that quantify or model all three resources together.
- `governance_focus`, `equity_indigenous_focus`, `evaluates_outcomes`: True where the item is a main object of the study; `evaluates_outcomes` is True only for measured outcomes of real policies, programs, projects, or events, not for scenario projections.
- `relevance`: 1 (peripheral) to 5 (central) to the chapter's question.
- `status`: observed (measured or documented in a real system) or modeled (scenario, simulation, or optimization result).

Documents from the authors' collection were coded from full texts; documents added by the structured search of 2019 to 2026 literature were coded from full texts where openly available and otherwise from abstracts. Coding reflects the authors' judgments.

## Sources and licences

Official statistics were drawn from the U.S. Geological Survey, Energy Information Administration, Department of Agriculture, Census Bureau, and Bureau of Reclamation; Statistics Canada, Environment and Climate Change Canada, the Canada Energy Regulator, and Natural Resources Canada; and Mexico's Comisión Nacional del Agua, Instituto Nacional de Estadística y Geografía, Secretaría de Energía, Centro Nacional de Control de Energía, and Secretaría de Agricultura y Desarrollo Rural. These are public domain or released under open government licences that require attribution. OpenAlex data are CC0. Natural Earth map layers are public domain.

This repository is released under the Creative Commons Attribution 4.0 International licence (see `LICENSE`).

## Citation

Ashkanani, Z., & Mohtar, R. H. (2026). *Nexus by default: Data for Chapter 15* (Version 1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.23148569

All versions: https://doi.org/10.5281/zenodo.23148568. Source: https://github.com/SAAAHco/nexus-by-default-north-america
