
import pandas as pd
from pymongo import MongoClient
from tqdm import tqdm

tqdm.pandas()


# ============================================================
# 1. LOAD ENRICHED DATASET
# ============================================================

file_path = 'TMDB_5000_enriched.csv'
new_data = pd.read_csv(file_path)


# ============================================================
# 2. TEXTUAL COLUMNS
# ============================================================

textual_columns = [
    'title',
    'status',
    'imdb_id',
    'original_language',
    'original_title',
    'overview',
    'tagline',
    'genres',
    'production_companies',
    'production_countries',
    'spoken_languages',
    'cast',
    'director',
    'director_of_photography',
    'writers',
    'producers',
    'music_composer'
]


# ============================================================
# 3. HANDLE MISSING VALUES
# ============================================================

def handle_missing_values(df):

    # Remove movies without a valid title
    df = df[df['title'].notna()].copy()
    df = df[df['title'].str.strip() != ""].copy()

    # Convert zero values to missing values
    df['budget'] = df['budget'].mask(
        df['budget'] == 0,
        pd.NA
    )

    df['revenue'] = df['revenue'].mask(
        df['revenue'] == 0,
        pd.NA
    )

    df['runtime'] = df['runtime'].mask(
        df['runtime'] <= 0,
        pd.NA
    )

    # Fill missing textual relationship columns
    textual_columns_to_fill = [
        'genres',
        'director',
        'imdb_id',
        'spoken_languages',
        'cast',
        'production_companies',
        'production_countries',
        'writers',
        'director_of_photography',
        'producers',
        'music_composer'
    ]

    for col in textual_columns_to_fill:
        if col in df.columns:
            df[col] = df[col].fillna("unknown")

    # Clean missing overview values
    if 'overview' in df.columns:

        df['overview'] = df['overview'].fillna("unknown")

        df['overview'] = (
            df['overview']
            .astype(str)
            .str.strip()
            .replace(
                ["", "n/a", "none"],
                "unknown"
            )
        )

    return df


# ============================================================
# 4. STANDARDIZE TEXT COLUMNS
# ============================================================

def standardize_text_columns(df, columns):

    for col in tqdm(
        columns,
        desc="Standardizing text columns"
    ):

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
            )

    return df


# ============================================================
# 5. CORRECT INCONSISTENT DATA
# ============================================================

def correct_inconsistent_data(df):

    # Convert release date to datetime
    if 'release_date' in df.columns:

        df['release_date'] = pd.to_datetime(
            df['release_date'],
            errors='coerce'
        )

    # Keep only valid numeric values
    df = df[
        (df['budget'].isna()) |
        (df['budget'] >= 0)
    ]

    df = df[
        (df['revenue'].isna()) |
        (df['revenue'] >= 0)
    ]

    df = df[
        (df['runtime'].isna()) |
        (df['runtime'] >= 0)
    ]

    return df


# ============================================================
# 6. NORMALIZE MULTI-VALUE COLUMNS
# ============================================================

def normalize_columns(df):

    columns_to_split = [
        'genres',
        'spoken_languages',
        'production_companies',
        'production_countries',
        'cast',
        'director',
        'director_of_photography',
        'writers',
        'producers',
        'music_composer'
    ]

    for col in tqdm(
        columns_to_split,
        desc="Normalizing columns"
    ):

        if col in df.columns:

            df[col] = (
                df[col]
                .str.strip()
                .str.split(",")
            )

    return df


# ============================================================
# 7. REMOVE DUPLICATES
# ============================================================

def remove_duplicates(df):

    df = df.drop_duplicates(
        subset=[
            'title',
            'release_date'
        ],
        keep='first'
    )

    return df


# ============================================================
# 8. RUN ORIGINAL CLEANING PIPELINE
# ============================================================

cleaned_data = (
    new_data

    .pipe(handle_missing_values)

    .pipe(
        standardize_text_columns,
        textual_columns
    )

    .pipe(correct_inconsistent_data)

    .pipe(normalize_columns)

    .pipe(remove_duplicates)
)


# ============================================================
# 9. DROP UNUSED COLUMN
# ============================================================

cleaned_data = cleaned_data.drop(
    columns=['poster_path'],
    errors='ignore'
)


# ============================================================
# 10. CONNECT TO MONGODB
# ============================================================

client = MongoClient(
    'mongodb://localhost:27017/'
)

db = client['MoviesDB']

collection = db['movies']


# ============================================================
# 11. DELETE OLD / PARTIAL DATA
# ============================================================

collection.drop()


# ============================================================
# 12. CONVERT DATAFRAME TO PYTHON RECORDS
# ============================================================

records = cleaned_data.to_dict(
    orient='records'
)


# ============================================================
# 13. FIX PANDAS VALUES FOR MONGODB
# ============================================================

# Important:
# Pandas values such as NaT, NaN and pd.NA cannot always
# be safely inserted into MongoDB.
#
# We convert them to Python None AFTER converting the
# DataFrame into dictionaries.

for record in records:

    for key, value in record.items():

        # Lists are already valid for MongoDB.
        # Do not pass them to pd.isna(), because pd.isna(list)
        # returns an array instead of one True/False value.

        if isinstance(value, list):
            continue

        if pd.isna(value):
            record[key] = None


# ============================================================
# 14. INSERT RECORDS INTO MONGODB
# ============================================================

batch_size = 1000

for i in tqdm(
    range(0, len(records), batch_size),
    desc="Inserting records to MongoDB"
):

    batch = records[
        i:i + batch_size
    ]

    collection.insert_many(batch)


# ============================================================
# 15. VERIFY INSERTION
# ============================================================

inserted_count = collection.count_documents({})

print("\n========================================")
print("DATA SUCCESSFULLY IMPORTED TO MONGODB")
print("========================================")

print(f"Movies inserted: {inserted_count}")


# ============================================================
# 16. CLOSE CONNECTION
# ============================================================

client.close()


































