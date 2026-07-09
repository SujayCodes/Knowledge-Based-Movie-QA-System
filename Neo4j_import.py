

import math
import time
from datetime import datetime

from pymongo import MongoClient
from neo4j import GraphDatabase
from tqdm import tqdm


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

# ----------------------------
# MongoDB
# ----------------------------

MONGODB_URI = "mongodb://localhost:27017/"

MONGODB_DATABASE = "MoviesDB"

MOVIES_COLLECTION = "movies"

TRIPLES_COLLECTION = "triples"


# ----------------------------
# Neo4j
# ----------------------------

NEO4J_URI = "neo4j://127.0.0.1:7687"

NEO4J_USER = "neo4j"

NEO4J_PASSWORD = "bigdata612"

NEO4J_DATABASE = "neo4j"


# ----------------------------
# Import settings
# ----------------------------

MOVIE_BATCH_SIZE = 100

TRIPLE_BATCH_SIZE = 500


# ============================================================
# 2. IMPORTANT RUN MODE
# ============================================================

# Keep this True for the FIRST real import.
#
# It removes anything currently inside the Neo4j database
# before importing your complete project data.
#
# After the full import is complete, change it to False.

START_FRESH = True


# ============================================================
# 3. STRUCTURED MOVIE RELATIONSHIPS
# ============================================================

RELATIONSHIP_CONFIG = {

    "genres": {
        "label": "Genre",
        "relationship": "BELONGS_TO_GENRE"
    },

    "spoken_languages": {
        "label": "Language",
        "relationship": "SPOKEN_IN"
    },

    "production_companies": {
        "label": "Company",
        "relationship": "PRODUCTION_COMPANY"
    },

    "production_countries": {
        "label": "Country",
        "relationship": "PRODUCED_IN"
    },

    "cast": {
        "label": "Person",
        "relationship": "ACTED_IN"
    },

    "director": {
        "label": "Person",
        "relationship": "DIRECTED_BY"
    },

    "writers": {
        "label": "Person",
        "relationship": "WRITTEN_BY"
    },

    "producers": {
        "label": "Person",
        "relationship": "PRODUCED_BY"
    },

    "music_composer": {
        "label": "Person",
        "relationship": "COMPOSED_BY"
    },

    "director_of_photography": {
        "label": "Person",
        "relationship": "DOP_BY"
    }
}


# ============================================================
# 4. CONNECT TO MONGODB
# ============================================================

mongo_client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000
)


mongo_db = mongo_client[
    MONGODB_DATABASE
]


movies_collection = mongo_db[
    MOVIES_COLLECTION
]


triples_collection = mongo_db[
    TRIPLES_COLLECTION
]


# ============================================================
# 5. CONNECT TO NEO4J
# ============================================================

neo4j_driver = GraphDatabase.driver(

    NEO4J_URI,

    auth=(
        NEO4J_USER,
        NEO4J_PASSWORD
    )

)


# ============================================================
# 6. TEST CONNECTIONS
# ============================================================

def test_connections():

    print(
        "\n========================================"
    )

    print(
        "TESTING DATABASE CONNECTIONS"
    )

    print(
        "========================================"
    )


    # ----------------------------
    # MongoDB
    # ----------------------------

    try:

        mongo_client.admin.command(
            "ping"
        )

        print(
            "MongoDB connection: SUCCESS"
        )

    except Exception as error:

        raise RuntimeError(

            f"MongoDB connection failed: {error}"

        )


    # ----------------------------
    # Neo4j
    # ----------------------------

    try:

        neo4j_driver.verify_connectivity()

        print(
            "Neo4j connection: SUCCESS"
        )

    except Exception as error:

        raise RuntimeError(

            f"Neo4j connection failed: {error}"

        )


# ============================================================
# 7. EXECUTE NEO4J QUERY
# ============================================================

def execute_query(
    query,
    parameters=None
):

    with neo4j_driver.session(
        database=NEO4J_DATABASE
    ) as session:

        result = session.run(

            query,

            parameters or {}

        )

        return result.consume()


# ============================================================
# 8. CLEAN VALUES FOR NEO4J
# ============================================================

def clean_value(value):

    if value is None:

        return None


    # ----------------------------
    # MongoDB / Python datetime
    # ----------------------------

    if isinstance(
        value,
        datetime
    ):

        return value.isoformat()


    # ----------------------------
    # NaN / Infinity
    # ----------------------------

    if isinstance(
        value,
        float
    ):

        if (
            math.isnan(value)
            or math.isinf(value)
        ):

            return None


    return value


# ============================================================
# 9. CLEAN ENTITY NAME
# ============================================================

def clean_entity_name(
    value
):

    if value is None:

        return None


    value = str(
        value
    ).strip()


    if value == "":

        return None


    if value.lower() in [

        "unknown",

        "none",

        "nan",

        "n/a"

    ]:

        return None


    return value


# ============================================================
# 10. NORMALIZE LIST VALUES
# ============================================================

def normalize_list(
    value
):

    if value is None:

        return []


    # Already a list

    if isinstance(
        value,
        list
    ):

        items = value


    # Single string

    elif isinstance(
        value,
        str
    ):

        items = value.split(",")


    # Other type

    else:

        items = [
            value
        ]


    cleaned_items = []


    for item in items:

        cleaned_item = (
            clean_entity_name(
                item
            )
        )


        if cleaned_item:

            cleaned_items.append(
                cleaned_item
            )


    # Remove duplicates while
    # preserving original order

    return list(
        dict.fromkeys(
            cleaned_items
        )
    )


# ============================================================
# 11. CHECK SOURCE DATA
# ============================================================

def check_source_data():

    movie_count = (
        movies_collection.count_documents(
            {}
        )
    )


    triple_count = (
        triples_collection.count_documents(
            {}
        )
    )


    print(
        "\n========================================"
    )

    print(
        "SOURCE DATA"
    )

    print(
        "========================================"
    )


    print(
        f"Movies in MongoDB: "
        f"{movie_count}"
    )


    print(
        f"NLP triples in MongoDB: "
        f"{triple_count}"
    )


    if movie_count == 0:

        raise RuntimeError(

            "No movies found in MongoDB."

        )


    if triple_count == 0:

        raise RuntimeError(

            "No NLP triples found in MongoDB."

        )


    return (
        movie_count,
        triple_count
    )


# ============================================================
# 12. CLEAR NEO4J DATABASE
# ============================================================

def clear_neo4j_database():

    print(
        "\n========================================"
    )

    print(
        "CLEARING PREVIOUS NEO4J DATA"
    )

    print(
        "========================================"
    )


    execute_query(
        """
        MATCH (n)
        DETACH DELETE n
        """
    )


    print(
        "Previous Neo4j graph data removed."
    )


# ============================================================
# 13. CREATE CONSTRAINTS AND INDEXES
# ============================================================

def create_constraints():

    print(
        "\n========================================"
    )

    print(
        "CREATING CONSTRAINTS"
    )

    print(
        "========================================"
    )


    constraints = [

        """
        CREATE CONSTRAINT movie_id_unique
        IF NOT EXISTS
        FOR (m:Movie)
        REQUIRE m.id IS UNIQUE
        """,

        """
        CREATE CONSTRAINT person_name_unique
        IF NOT EXISTS
        FOR (p:Person)
        REQUIRE p.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT genre_name_unique
        IF NOT EXISTS
        FOR (g:Genre)
        REQUIRE g.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT language_name_unique
        IF NOT EXISTS
        FOR (l:Language)
        REQUIRE l.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT company_name_unique
        IF NOT EXISTS
        FOR (c:Company)
        REQUIRE c.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT country_name_unique
        IF NOT EXISTS
        FOR (c:Country)
        REQUIRE c.name IS UNIQUE
        """,

        """
        CREATE CONSTRAINT entity_name_unique
        IF NOT EXISTS
        FOR (e:Entity)
        REQUIRE e.name IS UNIQUE
        """

    ]


    for query in constraints:

        execute_query(
            query
        )


    print(
        "Constraints created successfully."
    )


# ============================================================
# 14. PREPARE MOVIE DOCUMENT
# ============================================================

def prepare_movie(
    movie
):

    return {

        "id":
            clean_value(
                movie.get("id")
            ),

        "title":
            clean_value(
                movie.get("title")
            ),

        "release_date":
            clean_value(
                movie.get("release_date")
            ),

        "budget":
            clean_value(
                movie.get("budget")
            ),

        "runtime":
            clean_value(
                movie.get("runtime")
            ),

        "vote_average":
            clean_value(
                movie.get("vote_average")
            ),

        "vote_count":
            clean_value(
                movie.get("vote_count")
            ),

        "status":
            clean_value(
                movie.get("status")
            ),

        "revenue":
            clean_value(
                movie.get("revenue")
            ),

        "original_title":
            clean_value(
                movie.get("original_title")
            ),

        "imdb_id":
            clean_value(
                movie.get("imdb_id")
            ),

        "imdb_rating":
            clean_value(
                movie.get("imdb_rating")
            ),

        "imdb_votes":
            clean_value(
                movie.get("imdb_votes")
            ),

        "original_language":
            clean_value(
                movie.get("original_language")
            ),

        "popularity":
            clean_value(
                movie.get("popularity")
            ),

        "overview":
            clean_value(
                movie.get("overview")
            ),

        "tagline":
            clean_value(
                movie.get("tagline")
            )

    }


# ============================================================
# 15. IMPORT MOVIE NODE BATCH
# ============================================================

def import_movie_batch(
    movie_batch
):

    query = """

    UNWIND $movies AS movie

    MERGE (m:Movie {id: movie.id})

    SET
        m.title = movie.title,
        m.release_date = movie.release_date,
        m.budget = movie.budget,
        m.runtime = movie.runtime,
        m.vote_average = movie.vote_average,
        m.vote_count = movie.vote_count,
        m.status = movie.status,
        m.revenue = movie.revenue,
        m.original_title = movie.original_title,
        m.imdb_id = movie.imdb_id,
        m.imdb_rating = movie.imdb_rating,
        m.imdb_votes = movie.imdb_votes,
        m.original_language = movie.original_language,
        m.popularity = movie.popularity,
        m.overview = movie.overview,
        m.tagline = movie.tagline

    """


    execute_query(

        query,

        {
            "movies":
                movie_batch
        }

    )


# ============================================================
# 16. IMPORT ALL MOVIE NODES
# ============================================================

def import_movie_nodes(
    total_movies
):

    print(
        "\n========================================"
    )

    print(
        "IMPORTING MOVIE NODES"
    )

    print(
        "========================================"
    )


    projection = {

        "_id": 0

    }


    cursor = movies_collection.find(

        {},

        projection

    ).batch_size(
        MOVIE_BATCH_SIZE
    )


    movie_batch = []


    for movie in tqdm(

        cursor,

        total=total_movies,

        desc="Importing movies",

        unit="movie"

    ):

        prepared_movie = (
            prepare_movie(
                movie
            )
        )


        if (
            prepared_movie["id"]
            is None
        ):

            continue


        movie_batch.append(
            prepared_movie
        )


        if (
            len(movie_batch)
            >= MOVIE_BATCH_SIZE
        ):

            import_movie_batch(
                movie_batch
            )

            movie_batch.clear()


    # Final remaining batch

    if movie_batch:

        import_movie_batch(
            movie_batch
        )


    print(
        "Movie nodes imported successfully."
    )


# ============================================================
# 17. PREPARE STRUCTURED RELATIONSHIPS
# ============================================================

def prepare_relationship_records(
    movies
):

    relationship_records = {

        field: []

        for field
        in RELATIONSHIP_CONFIG

    }


    for movie in movies:

        movie_id = movie.get(
            "id"
        )


        if movie_id is None:

            continue


        for field in (
            RELATIONSHIP_CONFIG
        ):

            values = normalize_list(

                movie.get(
                    field
                )

            )


            for value in values:

                relationship_records[
                    field
                ].append(

                    {

                        "movie_id":
                            movie_id,

                        "name":
                            value

                    }

                )


    return relationship_records


# ============================================================
# 18. IMPORT ONE RELATIONSHIP TYPE
# ============================================================

def import_relationship_type(
    records,
    label,
    relationship_type
):

    if not records:

        return


    # label and relationship_type come only from the
    # fixed RELATIONSHIP_CONFIG dictionary above.

    query = f"""

    UNWIND $records AS row

    MATCH (m:Movie {{id: row.movie_id}})

    MERGE (entity:{label} {{name: row.name}})

    MERGE (m)-[:{relationship_type}]->(entity)

    """


    execute_query(

        query,

        {
            "records":
                records
        }

    )


# ============================================================
# 19. IMPORT ALL STRUCTURED RELATIONSHIPS
# ============================================================

def import_structured_relationships(
    total_movies
):

    print(
        "\n========================================"
    )

    print(
        "IMPORTING MOVIE RELATIONSHIPS"
    )

    print(
        "========================================"
    )


    cursor = movies_collection.find(

        {},

        {
            "_id": 0,
            "id": 1,
            **{
                field: 1
                for field
                in RELATIONSHIP_CONFIG
            }
        }

    ).batch_size(
        MOVIE_BATCH_SIZE
    )


    movie_batch = []


    for movie in tqdm(

        cursor,

        total=total_movies,

        desc="Creating relationships",

        unit="movie"

    ):

        movie_batch.append(
            movie
        )


        if (
            len(movie_batch)
            >= MOVIE_BATCH_SIZE
        ):

            process_relationship_batch(
                movie_batch
            )

            movie_batch.clear()


    # Final remaining batch

    if movie_batch:

        process_relationship_batch(
            movie_batch
        )


    print(
        "Structured movie relationships "
        "imported successfully."
    )


# ============================================================
# 20. PROCESS RELATIONSHIP BATCH
# ============================================================

def process_relationship_batch(
    movie_batch
):

    relationship_records = (
        prepare_relationship_records(
            movie_batch
        )
    )


    for field, config in (
        RELATIONSHIP_CONFIG.items()
    ):

        records = (
            relationship_records[
                field
            ]
        )


        import_relationship_type(

            records=records,

            label=config[
                "label"
            ],

            relationship_type=config[
                "relationship"
            ]

        )


# ============================================================
# 21. PREPARE NLP TRIPLE
# ============================================================

def prepare_triple(
    triple
):

    movie_id = clean_value(

        triple.get(
            "movie_id"
        )

    )


    subject = clean_entity_name(

        triple.get(
            "subject"
        )

    )


    predicate = clean_entity_name(

        triple.get(
            "predicate"
        )

    )


    obj = clean_entity_name(

        triple.get(
            "object"
        )

    )


    if (
        movie_id is None
        or subject is None
        or predicate is None
        or obj is None
    ):

        return None


    return {

        "movie_id":
            movie_id,

        "subject":
            subject,

        "predicate":
            predicate,

        "object":
            obj

    }


# ============================================================
# 22. IMPORT NLP TRIPLE BATCH
# ============================================================

def import_triple_batch(
    triple_batch
):

    query = """

    UNWIND $triples AS triple

    MATCH (m:Movie {id: triple.movie_id})

    MERGE (subject:Entity {
        name: triple.subject
    })

    MERGE (object:Entity {
        name: triple.object
    })

    MERGE (subject)-[
        relation:RELATION {
            type: triple.predicate
        }
    ]->(object)

    MERGE (m)-[:HAS_SUBJECT]->(subject)

    MERGE (m)-[:HAS_OBJECT]->(object)

    """


    execute_query(

        query,

        {
            "triples":
                triple_batch
        }

    )


# ============================================================
# 23. IMPORT ALL NLP TRIPLES
# ============================================================

def import_nlp_triples(
    total_triples
):

    print(
        "\n========================================"
    )

    print(
        "IMPORTING NLP TRIPLES"
    )

    print(
        "========================================"
    )


    cursor = triples_collection.find(

        {},

        {

            "_id": 0,

            "movie_id": 1,

            "subject": 1,

            "predicate": 1,

            "object": 1

        }

    ).batch_size(
        TRIPLE_BATCH_SIZE
    )


    triple_batch = []


    skipped_triples = 0


    for triple in tqdm(

        cursor,

        total=total_triples,

        desc="Importing NLP triples",

        unit="triple"

    ):

        prepared_triple = (
            prepare_triple(
                triple
            )
        )


        if prepared_triple is None:

            skipped_triples += 1

            continue


        triple_batch.append(
            prepared_triple
        )


        if (
            len(triple_batch)
            >= TRIPLE_BATCH_SIZE
        ):

            import_triple_batch(
                triple_batch
            )

            triple_batch.clear()


    # Final remaining batch

    if triple_batch:

        import_triple_batch(
            triple_batch
        )


    print(
        "NLP triples imported successfully."
    )


    print(
        f"Invalid triples skipped: "
        f"{skipped_triples}"
    )


# ============================================================
# 24. GET SINGLE COUNT
# ============================================================

def get_count(
    query
):

    with neo4j_driver.session(
        database=NEO4J_DATABASE
    ) as session:

        result = session.run(
            query
        )

        record = result.single()

        return record[
            "count"
        ]


# ============================================================
# 25. VERIFY FINAL GRAPH
# ============================================================

def verify_graph():

    print(
        "\n========================================"
    )

    print(
        "FINAL NEO4J GRAPH VERIFICATION"
    )

    print(
        "========================================"
    )


    movie_nodes = get_count(

        """
        MATCH (m:Movie)
        RETURN count(m) AS count
        """

    )


    person_nodes = get_count(

        """
        MATCH (p:Person)
        RETURN count(p) AS count
        """

    )


    genre_nodes = get_count(

        """
        MATCH (g:Genre)
        RETURN count(g) AS count
        """

    )


    language_nodes = get_count(

        """
        MATCH (l:Language)
        RETURN count(l) AS count
        """

    )


    company_nodes = get_count(

        """
        MATCH (c:Company)
        RETURN count(c) AS count
        """

    )


    country_nodes = get_count(

        """
        MATCH (c:Country)
        RETURN count(c) AS count
        """

    )


    entity_nodes = get_count(

        """
        MATCH (e:Entity)
        RETURN count(e) AS count
        """

    )


    total_nodes = get_count(

        """
        MATCH (n)
        RETURN count(n) AS count
        """

    )


    total_relationships = get_count(

        """
        MATCH ()-[r]->()
        RETURN count(r) AS count
        """

    )


    nlp_relationships = get_count(

        """
        MATCH ()-[r:RELATION]->()
        RETURN count(r) AS count
        """

    )


    print(
        f"Movie nodes: "
        f"{movie_nodes}"
    )


    print(
        f"Person nodes: "
        f"{person_nodes}"
    )


    print(
        f"Genre nodes: "
        f"{genre_nodes}"
    )


    print(
        f"Language nodes: "
        f"{language_nodes}"
    )


    print(
        f"Company nodes: "
        f"{company_nodes}"
    )


    print(
        f"Country nodes: "
        f"{country_nodes}"
    )


    print(
        f"NLP Entity nodes: "
        f"{entity_nodes}"
    )


    print(
        f"Total nodes: "
        f"{total_nodes}"
    )


    print(
        f"NLP RELATION relationships: "
        f"{nlp_relationships}"
    )


    print(
        f"Total relationships: "
        f"{total_relationships}"
    )


    print(
        "========================================"
    )


    if movie_nodes == 4803:

        print(
            "All 4,803 movie nodes imported: YES"
        )

    else:

        print(
            "WARNING: Expected 4,803 movie nodes."
        )


# ============================================================
# 26. MAIN FUNCTION
# ============================================================

def main():

    start_time = time.time()


    print(
        "\n========================================"
    )

    print(
        "MOVIE QA SYSTEM - NEO4J IMPORT"
    )

    print(
        "========================================"
    )


    try:

        # ----------------------------
        # Test connections
        # ----------------------------

        test_connections()


        # ----------------------------
        # Check MongoDB source data
        # ----------------------------

        (
            total_movies,
            total_triples
        ) = check_source_data()


        # ----------------------------
        # Clear graph on first run
        # ----------------------------

        if START_FRESH:

            print(
                "\nSTART_FRESH = True"
            )

            clear_neo4j_database()

        else:

            print(
                "\nSTART_FRESH = False"
            )

            print(
                "Existing graph will be preserved."
            )

            print(
                "MERGE will prevent duplicate nodes "
                "and relationships."
            )


        # ----------------------------
        # Constraints
        # ----------------------------

        create_constraints()


        # ----------------------------
        # Stage 1
        # ----------------------------

        import_movie_nodes(
            total_movies
        )


        # ----------------------------
        # Stage 2
        # ----------------------------

        import_structured_relationships(
            total_movies
        )


        # ----------------------------
        # Stage 3
        # ----------------------------

        import_nlp_triples(
            total_triples
        )


        # ----------------------------
        # Verification
        # ----------------------------

        verify_graph()


        # ----------------------------
        # Total time
        # ----------------------------

        elapsed_seconds = (
            time.time()
            - start_time
        )


        elapsed_minutes = (
            elapsed_seconds
            / 60
        )


        elapsed_hours = (
            elapsed_minutes
            / 60
        )


        print(
            "\n========================================"
        )

        print(
            "NEO4J IMPORT COMPLETED SUCCESSFULLY"
        )

        print(
            "========================================"
        )


        print(
            f"Total time: "
            f"{elapsed_minutes:.2f} minutes"
        )


        print(
            f"Total time: "
            f"{elapsed_hours:.2f} hours"
        )


        print(
            "\nNext project stage:"
        )


        print(
            "Query_generator.py"
        )


        print(
            "========================================"
        )


    except KeyboardInterrupt:

        print(
            "\n\nImport stopped by user."
        )


        print(
            "Because the script uses MERGE, "
            "you can rerun it safely."
        )


        print(
            "Before rerunning, set:"
        )


        print(
            "START_FRESH = False"
        )


    except Exception as error:

        print(
            "\n========================================"
        )

        print(
            "IMPORT FAILED"
        )

        print(
            "========================================"
        )


        print(
            f"Error type: "
            f"{type(error).__name__}"
        )


        print(
            f"Error: "
            f"{error}"
        )


        print(
            "\nDo not run Dataset_cleaning.py "
            "or NLP_triple_extract.py again."
        )


        print(
            "Send me this complete error output."
        )


    finally:

        neo4j_driver.close()

        mongo_client.close()


        print(
            "\nDatabase connections closed."
        )


# ============================================================
# 27. RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    main()