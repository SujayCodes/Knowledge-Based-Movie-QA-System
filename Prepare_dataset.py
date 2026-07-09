import ast
import pandas as pd


# ============================================================
# 1. FILE PATHS
# ============================================================

MOVIES_FILE = "tmdb_5000_movies.csv"
CREDITS_FILE = "tmdb_5000_credits.csv"
OUTPUT_FILE = "TMDB_5000_enriched.csv"


# ============================================================
# 2. LOAD BOTH DATASETS
# ============================================================

print("Loading datasets...")

movies = pd.read_csv(MOVIES_FILE)
credits = pd.read_csv(CREDITS_FILE)

print(f"Movies shape: {movies.shape}")
print(f"Credits shape: {credits.shape}")


# ============================================================
# 3. HELPER FUNCTION TO SAFELY PARSE JSON-LIKE TEXT
# ============================================================

def safe_parse(value):
    if pd.isna(value):
        return []

    try:
        parsed = ast.literal_eval(value)

        if isinstance(parsed, list):
            return parsed

        return []

    except (ValueError, SyntaxError, TypeError):
        return []


# ============================================================
# 4. EXTRACT NAMES FROM JSON-LIKE COLUMNS
# ============================================================

def extract_names(value):
    items = safe_parse(value)

    names = []

    for item in items:
        if isinstance(item, dict):
            name = item.get("name")

            if name:
                names.append(name.strip())

    return ", ".join(names)


# ============================================================
# 5. EXTRACT ALL CAST MEMBERS
# ============================================================

def extract_cast(value):
    items = safe_parse(value)

    cast_names = []

    for person in items:
        if isinstance(person, dict):
            name = person.get("name")

            if name:
                cast_names.append(name.strip())

    return ", ".join(cast_names)


# ============================================================
# 6. EXTRACT CREW MEMBERS BY EXACT JOB
# ============================================================

def extract_crew_by_job(value, target_jobs):
    items = safe_parse(value)

    names = []

    for person in items:
        if not isinstance(person, dict):
            continue

        job = person.get("job")
        name = person.get("name")

        if job in target_jobs and name:
            names.append(name.strip())

    # Remove duplicate names while preserving original order
    names = list(dict.fromkeys(names))

    return ", ".join(names)


# ============================================================
# 7. PREPARE CREDITS DATASET FOR MERGING
# ============================================================

print("\nPreparing credits dataset...")

credits = credits.rename(columns={"movie_id": "id"})

# Both datasets contain title, so remove the duplicate credits title
credits = credits.drop(columns=["title"], errors="ignore")


# ============================================================
# 8. MERGE MOVIES + CREDITS
# ============================================================

print("Merging datasets...")

data = movies.merge(
    credits,
    on="id",
    how="left"
)

print(f"Merged shape: {data.shape}")


# ============================================================
# 9. CONVERT TMDB JSON-LIKE COLUMNS TO COMMA-SEPARATED TEXT
# ============================================================

print("\nProcessing movie metadata...")

metadata_columns = [
    "genres",
    "production_companies",
    "production_countries",
    "spoken_languages"
]

for column in metadata_columns:
    print(f"Processing {column}...")

    data[column] = data[column].apply(extract_names)


# ============================================================
# 10. EXTRACT ALL CAST MEMBERS
# ============================================================

print("\nExtracting all cast members...")

data["cast"] = data["cast"].apply(extract_cast)


# ============================================================
# 11. EXTRACT CREW INFORMATION
# ============================================================

print("Extracting directors...")

data["director"] = data["crew"].apply(
    lambda value: extract_crew_by_job(
        value,
        {"Director"}
    )
)


print("Extracting writers...")

data["writers"] = data["crew"].apply(
    lambda value: extract_crew_by_job(
        value,
        {
            "Writer",
            "Screenplay",
            "Story",
            "Novel",
            "Characters",
            "Adaptation"
        }
    )
)


print("Extracting producers...")

data["producers"] = data["crew"].apply(
    lambda value: extract_crew_by_job(
        value,
        {
            "Producer",
            "Executive Producer",
            "Co-Producer",
            "Associate Producer"
        }
    )
)


print("Extracting music composers...")

data["music_composer"] = data["crew"].apply(
    lambda value: extract_crew_by_job(
        value,
        {
            "Original Music Composer",
            "Music",
            "Music Composer"
        }
    )
)


print("Extracting directors of photography...")

data["director_of_photography"] = data["crew"].apply(
    lambda value: extract_crew_by_job(
        value,
        {
            "Director of Photography",
            "Cinematography"
        }
    )
)


# ============================================================
# 12. CREATE COLUMNS EXPECTED BY ORIGINAL PROJECT
# ============================================================

print("\nCreating compatibility columns...")

# These fields are not present in the TMDB 5000 datasets.
# They are created so the original Dataset_cleaning.py
# can process the enriched dataset without KeyError.

if "imdb_id" not in data.columns:
    data["imdb_id"] = "unknown"

if "imdb_rating" not in data.columns:
    data["imdb_rating"] = pd.NA

if "imdb_votes" not in data.columns:
    data["imdb_votes"] = pd.NA

if "poster_path" not in data.columns:
    data["poster_path"] = pd.NA


# ============================================================
# 13. REMOVE RAW COLUMNS NOT NEEDED BY ORIGINAL PIPELINE
# ============================================================

data = data.drop(
    columns=[
        "crew",
        "homepage",
        "keywords"
    ],
    errors="ignore"
)


# ============================================================
# 14. ARRANGE IMPORTANT PROJECT COLUMNS
# ============================================================

important_columns = [
    "id",
    "title",
    "status",
    "imdb_id",
    "original_language",
    "original_title",
    "overview",
    "tagline",
    "genres",
    "production_companies",
    "production_countries",
    "spoken_languages",
    "cast",
    "director",
    "director_of_photography",
    "writers",
    "producers",
    "music_composer",
    "release_date",
    "budget",
    "revenue",
    "runtime",
    "vote_average",
    "vote_count",
    "imdb_rating",
    "imdb_votes",
    "popularity",
    "poster_path"
]

# Keep only columns that actually exist
important_columns = [
    column
    for column in important_columns
    if column in data.columns
]

data = data[important_columns]


# ============================================================
# 15. SAVE THE ENRICHED DATASET
# ============================================================

print("\nSaving enriched dataset...")

data.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# ============================================================
# 16. FINAL VERIFICATION
# ============================================================

print("\n========================================")
print("DATASET PREPARATION COMPLETED")
print("========================================")

print(f"Output file: {OUTPUT_FILE}")
print(f"Movies: {len(data)}")
print(f"Columns: {len(data.columns)}")

print("\nFinal columns:")
print(data.columns.tolist())

print("\nSample enriched movie:")
print(
    data[
        [
            "title",
            "genres",
            "cast",
            "director",
            "writers",
            "producers",
            "music_composer",
            "director_of_photography"
        ]
    ].iloc[0]
)