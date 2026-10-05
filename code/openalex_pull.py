"""OpenAlex bibliometric pull for Chapter 15 (run 2026-10-02).

Writes CSVs and a note under _chapter_v3/analysis/bibliometrics/.
Query: title_and_abstract phrase search for the WEF/FEW nexus name variants; types article|review; years 2010-2026.
"""
import json, time, csv, os, sys, urllib.request, urllib.parse

OUT = r"F:/2025/Publications/WEF_Practice_N_America/_chapter_v3/analysis/bibliometrics"
os.makedirs(OUT, exist_ok=True)
RAW = os.path.join(OUT, "raw"); os.makedirs(RAW, exist_ok=True)
BASE = "https://api.openalex.org/works?"
Q = ('"water-energy-food nexus" OR "food-energy-water nexus" OR "water-food-energy nexus" OR '
     '"energy-water-food nexus" OR "food-water-energy nexus" OR "energy-food-water nexus" OR '
     '"WEF nexus" OR "FEW nexus"')
TYPES = "type:article|review"
YEARS = "publication_year:2010-2026"
NA_PLACES = ('"United States" OR "U.S." OR USA OR Canada OR Mexico OR California OR Texas OR Arizona OR Alaska OR Arctic OR '
             'Prairies OR "Great Lakes" OR "Colorado River" OR "Rio Grande" OR Ontario OR Alberta OR Saskatchewan OR "Nuevo Leon" OR Sonora')
NSF = "F4320306076"
calls = []

def get(params, tag):
    url = BASE + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    cached = os.path.join(RAW, tag + ".json")
    if os.path.exists(cached):
        calls.append((tag, url))
        return json.load(open(cached, encoding="utf-8"))
    for attempt in range(12):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "chapter15-bibliometrics (academic use)"})
            d = json.load(urllib.request.urlopen(req, timeout=90))
            calls.append((tag, url))
            with open(os.path.join(RAW, tag + ".json"), "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False)
            time.sleep(2.0)
            return d
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503):
                time.sleep(20 + 15 * attempt); continue
            raise
    raise RuntimeError("failed " + tag)

def by_year(flt, tag):
    d = get({"filter": flt, "group_by": "publication_year", "per-page": 200}, tag)
    return {int(g["key"]): g["count"] for g in d["group_by"]}

f_all = f"title_and_abstract.search:{Q},{TYPES},{YEARS}"
series = {}
series["global"] = by_year(f_all, "global_by_year")
for cc in ["US", "CA", "MX", "CN", "GB", "DE"]:
    series[f"affil_{cc}"] = by_year(f_all + f",authorships.countries:{cc}", f"affil_{cc}_by_year")
series["affil_NA_any"] = by_year(f_all + ",authorships.countries:US|CA|MX", "affil_NA_by_year")
series["place_NA_mention"] = by_year(f"title_and_abstract.search:({Q}) AND ({NA_PLACES}),{TYPES},{YEARS}", "place_NA_by_year")
series["nsf_funded_NA"] = by_year(f_all + f",authorships.countries:US|CA|MX,funders.id:{NSF}", "nsf_NA_by_year")
series["nsf_funded_US"] = by_year(f_all + f",authorships.countries:US,funders.id:{NSF}", "nsf_US_by_year")
series["oa_NA"] = by_year(f_all + ",authorships.countries:US|CA|MX,is_oa:true", "oa_NA_by_year")

years = list(range(2010, 2027))
with open(os.path.join(OUT, "annual_counts.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    cols = [k for k in series if series[k]]
    w.writerow(["year"] + cols)
    for y in years:
        w.writerow([y] + [series[k].get(y, 0) for k in cols])

# top cited NA works
top = get({"filter": f_all + ",authorships.countries:US|CA|MX", "sort": "cited_by_count:desc", "per-page": 50,
           "select": "id,doi,title,publication_year,cited_by_count,primary_location,authorships,type"}, "top_cited_NA")
with open(os.path.join(OUT, "top_cited_na.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["rank", "year", "cited_by_count", "first_author", "countries", "journal", "title", "doi"])
    for i, r in enumerate(top["results"], 1):
        auth = r.get("authorships") or []
        fa = auth[0]["author"]["display_name"] if auth else ""
        countries = sorted({c for a in auth for c in (a.get("countries") or [])})
        src = (r.get("primary_location") or {}).get("source") or {}
        w.writerow([i, r["publication_year"], r["cited_by_count"], fa, "|".join(countries), src.get("display_name", ""), r["title"], r.get("doi", "")])

# topics: NA vs global (primary topic and subfield)
for scope, flt in [("NA", f_all + ",authorships.countries:US|CA|MX"), ("global", f_all)]:
    for gb in ["primary_topic.id", "primary_topic.subfield.id", "primary_topic.field.id"]:
        d = get({"filter": flt, "group_by": gb, "per-page": 50}, f"topics_{scope}_{gb.replace('.', '_')}")
        with open(os.path.join(OUT, f"topics_{scope}_{gb.split('.')[-2] if gb.count('.')==2 else 'topic'}.csv"), "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(["key", "name", "count"])
            for g in d["group_by"]:
                w.writerow([g["key"], g.get("key_display_name", ""), g["count"]])

# country ranking overall (affiliation)
d = get({"filter": f_all, "group_by": "authorships.countries", "per-page": 60}, "countries_all")
with open(os.path.join(OUT, "countries_all.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["country", "name", "count"])
    for g in d["group_by"]:
        w.writerow([g["key"], g.get("key_display_name", ""), g["count"]])
# recent-period country ranking 2022-2026
d = get({"filter": f"title_and_abstract.search:{Q},{TYPES},publication_year:2022-2026", "group_by": "authorships.countries", "per-page": 60}, "countries_2022_2026")
with open(os.path.join(OUT, "countries_2022_2026.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["country", "name", "count"])
    for g in d["group_by"]:
        w.writerow([g["key"], g.get("key_display_name", ""), g["count"]])
# NA institutions
d = get({"filter": f_all + ",authorships.countries:US|CA|MX", "group_by": "authorships.institutions.lineage", "per-page": 40}, "institutions_NA")
with open(os.path.join(OUT, "institutions_na.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id", "name", "count"])
    for g in d["group_by"]:
        w.writerow([g["key"], g.get("key_display_name", ""), g["count"]])
# funders NA
d = get({"filter": f_all + ",authorships.countries:US|CA|MX", "group_by": "funders.id", "per-page": 30}, "funders_NA")
with open(os.path.join(OUT, "funders_na.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id", "name", "count"])
    for g in d["group_by"]:
        w.writerow([g["key"], g.get("key_display_name", ""), g["count"]])
# totals
tot = get({"filter": f_all, "per-page": 1}, "total_all")["meta"]["count"]
tot_na = get({"filter": f_all + ",authorships.countries:US|CA|MX", "per-page": 1}, "total_NA")["meta"]["count"]
tot_place = get({"filter": f"title_and_abstract.search:({Q}) AND ({NA_PLACES}),{TYPES},{YEARS}", "per-page": 1}, "total_place")["meta"]["count"]
tot_nocountry = get({"filter": f_all + ",authorships.countries:null", "per-page": 1}, "total_nocountry")["meta"]["count"] if True else None

with open(os.path.join(OUT, "bibliometrics_note.md"), "w", encoding="utf-8") as f:
    f.write("# OpenAlex bibliometric pull, run 2026-10-02\n\n")
    f.write(f"Query (title_and_abstract.search): {Q}\nFilters: {TYPES}; {YEARS}\n\n")
    f.write(f"Totals: all = {tot}; NA-affiliated (US|CA|MX) = {tot_na}; NA place named in title/abstract = {tot_place}; records without any affiliation country = {tot_nocountry}\n\n")
    f.write("API calls:\n")
    for tag, url in calls:
        f.write(f"- {tag}: {url}\n")
    f.write("\nCaveats: OpenAlex coverage and affiliation parsing; 2026 is partial (year to date); phrase search misses works that use only 'energy-water nexus' or 'water security'; boolean OR across eight name variants; counts change as OpenAlex updates.\n")
print("done", tot, tot_na, tot_place, tot_nocountry)
print({k: sum(v.values()) for k, v in series.items() if v})
