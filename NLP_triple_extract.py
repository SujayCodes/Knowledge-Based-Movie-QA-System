
import socket
import logging
import warnings
import time
from datetime import datetime

from pymongo import MongoClient, ASCENDING
from stanza.server import CoreNLPClient
from tqdm import tqdm


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

MONGODB_URI = "mongodb://localhost:27017/"

DATABASE_NAME = "MoviesDB"

MOVIES_COLLECTION = "movies"

TRIPLES_COLLECTION = "triples"

PROGRESS_COLLECTION = "triple_extraction_progress"


CORENLP_PATH = (
    r"C:\Users\drdev\Downloads\Movie QA System"
    r"\stanza_corenlp\*"
)


# ============================================================
# 2. FULL DATASET SETTINGS
# ============================================================

# None means ALL movies will be processed.
#
# Do not change this to 10.
# This final version is intended for the complete dataset.

MOVIE_LIMIT = None


# Number of triples kept temporarily before inserting into MongoDB.
#
# This reduces the number of database operations while keeping
# memory usage low.

TRIPLE_BATCH_SIZE = 500


# ============================================================
# 3. FIRST FULL RUN SETTING
# ============================================================

# IMPORTANT:
#
# Keep this True ONLY for the first full-dataset run.
#
# It will remove the 266 triples created by your previous
# 10-movie benchmark and start the real extraction from zero.
#
# After the first full run starts successfully, change this
# to False.
#
# If the program later stops or the laptop restarts, keeping
# it False allows the script to resume.

START_FRESH = False


# ============================================================
# 4. LOGGING AND WARNINGS
# ============================================================

logging.getLogger("stanza").setLevel(logging.WARNING)

logging.getLogger("urllib3").setLevel(logging.WARNING)

logging.getLogger("requests").setLevel(logging.WARNING)

warnings.filterwarnings("ignore")


# ============================================================
# 5. CONNECT TO MONGODB
# ============================================================

mongo_client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000
)


db = mongo_client[
    DATABASE_NAME
]


movies_collection = db[
    MOVIES_COLLECTION
]


triples_collection = db[
    TRIPLES_COLLECTION
]


progress_collection = db[
    PROGRESS_COLLECTION
]


# ============================================================
# 6. TEST MONGODB CONNECTION
# ============================================================

def test_mongodb_connection():

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


# ============================================================
# 7. CREATE DATABASE INDEXES
# ============================================================

def create_indexes():

    print(
        "Creating MongoDB indexes..."
    )


    triples_collection.create_index(
        [
            ("movie_id", ASCENDING)
        ]
    )


    progress_collection.create_index(
        [
            ("movie_id", ASCENDING)
        ],
        unique=True
    )


    print(
        "MongoDB indexes ready."
    )


# ============================================================
# 8. FIND FREE PORT
# ============================================================

def find_free_port():

    with socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    ) as sock:

        sock.bind(
            ("127.0.0.1", 0)
        )

        return sock.getsockname()[1]


# ============================================================
# 9. CHECK VALID OVERVIEW
# ============================================================

def is_valid_overview(
    overview
):

    if overview is None:

        return False


    if not isinstance(
        overview,
        str
    ):

        return False


    overview = overview.strip()


    if overview == "":

        return False


    if overview.lower() in [

        "unknown",

        "none",

        "nan",

        "n/a"

    ]:

        return False


    return True


# ============================================================
# 10. EXTRACT OPENIE TRIPLES
# ============================================================

def extract_triples(
    overview,
    movie_id,
    corenlp_client
):

    extracted_triples = []


    annotation = (
        corenlp_client.annotate(
            overview
        )
    )


    for sentence in (
        annotation.sentence
    ):

        for triple in (
            sentence.openieTriple
        ):

            subject = (
                triple.subject.strip()
            )


            predicate = (
                triple.relation.strip()
            )


            obj = (
                triple.object.strip()
            )


            # Skip incomplete triples

            if (
                not subject
                or not predicate
                or not obj
            ):

                continue


            extracted_triples.append(

                {

                    "movie_id":
                        movie_id,

                    "subject":
                        subject,

                    "predicate":
                        predicate,

                    "object":
                        obj

                }

            )


    return extracted_triples


# ============================================================
# 11. LOAD ALL MOVIES
# ============================================================

def load_movies():

    query = {

        "overview": {

            "$exists": True

        }

    }


    projection = {

        "_id": 0,

        "id": 1,

        "title": 1,

        "overview": 1

    }


    cursor = movies_collection.find(

        query,

        projection

    )


    if MOVIE_LIMIT is not None:

        cursor = cursor.limit(
            MOVIE_LIMIT
        )


    return list(
        cursor
    )


# ============================================================
# 12. GET COMPLETED MOVIE IDS
# ============================================================

def get_completed_movie_ids():

    completed_ids = set()


    cursor = progress_collection.find(

        {

            "status": {

                "$in": [

                    "completed",

                    "no_triples",

                    "skipped"

                ]

            }

        },

        {

            "_id": 0,

            "movie_id": 1

        }

    )


    for document in cursor:

        completed_ids.add(

            document[
                "movie_id"
            ]

        )


    return completed_ids


# ============================================================
# 13. SAVE MOVIE PROGRESS
# ============================================================

def save_progress(
    movie_id,
    title,
    status,
    triple_count=0,
    error_message=None
):

    progress_document = {

        "movie_id":
            movie_id,

        "title":
            title,

        "status":
            status,

        "triple_count":
            triple_count,

        "processed_at":
            datetime.now()

    }


    if error_message:

        progress_document[
            "error"
        ] = str(
            error_message
        )


    progress_collection.update_one(

        {

            "movie_id":
                movie_id

        },

        {

            "$set":
                progress_document

        },

        upsert=True

    )


# ============================================================
# 14. FLUSH TRIPLE BUFFER
# ============================================================

def flush_triple_buffer(
    triple_buffer
):

    if not triple_buffer:

        return 0


    triples_collection.insert_many(
        triple_buffer
    )


    inserted_count = len(
        triple_buffer
    )


    triple_buffer.clear()


    return inserted_count


# ============================================================
# 15. SHOW EXISTING PROGRESS
# ============================================================

def show_existing_progress():

    completed = (
        progress_collection.count_documents(
            {
                "status":
                    "completed"
            }
        )
    )


    no_triples = (
        progress_collection.count_documents(
            {
                "status":
                    "no_triples"
            }
        )
    )


    skipped = (
        progress_collection.count_documents(
            {
                "status":
                    "skipped"
            }
        )
    )


    failed = (
        progress_collection.count_documents(
            {
                "status":
                    "failed"
            }
        )
    )


    stored_triples = (
        triples_collection.count_documents(
            {}
        )
    )


    print(
        "\nExisting progress:"
    )


    print(
        f"Completed movies: "
        f"{completed}"
    )


    print(
        f"Movies with no triples: "
        f"{no_triples}"
    )


    print(
        f"Skipped movies: "
        f"{skipped}"
    )


    print(
        f"Failed movies: "
        f"{failed}"
    )


    print(
        f"Stored triples: "
        f"{stored_triples}"
    )


# ============================================================
# 16. MAIN FUNCTION
# ============================================================

def main():

    print(
        "\n"
        "========================================"
    )


    print(
        "FULL MOVIE NLP TRIPLE EXTRACTION"
    )


    print(
        "========================================"
    )


    # --------------------------------------------------------
    # TEST MONGODB
    # --------------------------------------------------------

    test_mongodb_connection()


    # --------------------------------------------------------
    # CHECK NUMBER OF MOVIES
    # --------------------------------------------------------

    total_movies_in_database = (
        movies_collection.count_documents(
            {}
        )
    )


    print(
        f"Movies in MongoDB: "
        f"{total_movies_in_database}"
    )


    if (
        total_movies_in_database
        == 0
    ):

        raise RuntimeError(

            "No movies found in MongoDB. "
            "Run Dataset_cleaning.py first."

        )


    # --------------------------------------------------------
    # FIRST FULL RUN CLEANUP
    # --------------------------------------------------------

    if START_FRESH:

        print(
            "\nSTART_FRESH = True"
        )


        print(
            "Removing previous TEST triples..."
        )


        triples_collection.drop()


        progress_collection.drop()


        print(
            "Previous test data removed."
        )


        print(
            "Starting full extraction from movie 1."
        )


    else:

        print(
            "\nSTART_FRESH = False"
        )


        print(
            "Resume mode enabled."
        )


    # --------------------------------------------------------
    # CREATE INDEXES
    # --------------------------------------------------------

    create_indexes()


    # --------------------------------------------------------
    # LOAD ALL MOVIES
    # --------------------------------------------------------

    print(
        "\nLoading movies..."
    )


    movies = load_movies()


    total_loaded = len(
        movies
    )


    print(
        f"Movies loaded: "
        f"{total_loaded}"
    )


    # --------------------------------------------------------
    # GET COMPLETED MOVIES
    # --------------------------------------------------------

    completed_movie_ids = (
        get_completed_movie_ids()
    )


    print(
        f"Already processed: "
        f"{len(completed_movie_ids)}"
    )


    # --------------------------------------------------------
    # FIND REMAINING MOVIES
    # --------------------------------------------------------

    remaining_movies = [

        movie

        for movie in movies

        if movie.get("id")
        not in completed_movie_ids

    ]


    print(
        f"Remaining movies: "
        f"{len(remaining_movies)}"
    )


    if not remaining_movies:

        print(
            "\nAll movies have already "
            "been processed."
        )


        show_existing_progress()


        mongo_client.close()


        return


    # --------------------------------------------------------
    # FIND CORENLP PORT
    # --------------------------------------------------------

    port = find_free_port()


    print(
        f"\nCoreNLP port: {port}"
    )


    # --------------------------------------------------------
    # CREATE CORENLP CLIENT
    # --------------------------------------------------------

    corenlp_client = CoreNLPClient(

        endpoint=(
            f"http://localhost:{port}"
        ),

        annotators=[

            "tokenize",

            "ssplit",

            "pos",

            "lemma",

            "ner",

            "depparse",

            "natlog",

            "openie"

        ],

        timeout=120000,

        memory="4G",

        classpath=CORENLP_PATH,

        be_quiet=True

    )


    # --------------------------------------------------------
    # RUN STATISTICS
    # --------------------------------------------------------

    run_processed = 0

    run_with_triples = 0

    run_without_triples = 0

    run_skipped = 0

    run_failed = 0

    run_triples = 0


    triple_buffer = []


    start_time = time.time()


    try:

        # ----------------------------------------------------
        # START CORENLP
        # ----------------------------------------------------

        print(
            "\nStarting CoreNLP..."
        )


        corenlp_client.start()


        print(
            "CoreNLP started successfully."
        )


        print(
            "\nStarting full dataset processing..."
        )


        print(
            "You can stop safely with Ctrl + C."
        )


        print(
            "Progress will be saved.\n"
        )


        # ----------------------------------------------------
        # PROCESS ALL REMAINING MOVIES
        # ----------------------------------------------------

        for movie in tqdm(

            remaining_movies,

            desc="Processing all movies",

            unit="movie"

        ):

            movie_id = (
                movie.get(
                    "id"
                )
            )


            title = (
                movie.get(
                    "title",
                    "unknown"
                )
            )


            overview = (
                movie.get(
                    "overview"
                )
            )


            # ------------------------------------------------
            # INVALID OVERVIEW
            # ------------------------------------------------

            if not is_valid_overview(
                overview
            ):

                run_skipped += 1


                save_progress(

                    movie_id=
                        movie_id,

                    title=
                        title,

                    status=
                        "skipped",

                    triple_count=
                        0

                )


                continue


            try:

                # --------------------------------------------
                # EXTRACT TRIPLES
                # --------------------------------------------

                movie_triples = (
                    extract_triples(

                        overview=
                            overview,

                        movie_id=
                            movie_id,

                        corenlp_client=
                            corenlp_client

                    )
                )


                run_processed += 1


                # --------------------------------------------
                # MOVIE PRODUCED TRIPLES
                # --------------------------------------------

                if movie_triples:

                    run_with_triples += 1


                    triple_count = len(
                        movie_triples
                    )


                    run_triples += (
                        triple_count
                    )


                    triple_buffer.extend(
                        movie_triples
                    )


                    # ----------------------------------------
                    # FLUSH BUFFER WHEN LARGE ENOUGH
                    # ----------------------------------------

                    if (
                        len(triple_buffer)
                        >= TRIPLE_BATCH_SIZE
                    ):

                        flush_triple_buffer(
                            triple_buffer
                        )


                    save_progress(

                        movie_id=
                            movie_id,

                        title=
                            title,

                        status=
                            "completed",

                        triple_count=
                            triple_count

                    )


                # --------------------------------------------
                # ZERO TRIPLES
                # --------------------------------------------

                else:

                    run_without_triples += 1


                    save_progress(

                        movie_id=
                            movie_id,

                        title=
                            title,

                        status=
                            "no_triples",

                        triple_count=
                            0

                    )


            # ------------------------------------------------
            # MOVIE FAILURE
            # ------------------------------------------------

            except Exception as error:

                run_failed += 1


                save_progress(

                    movie_id=
                        movie_id,

                    title=
                        title,

                    status=
                        "failed",

                    triple_count=
                        0,

                    error_message=
                        str(error)

                )


                print(
                    f"\nFAILED: {title}"
                )


                print(
                    f"Error: {error}"
                )


        # ----------------------------------------------------
        # SAVE FINAL BUFFER
        # ----------------------------------------------------

        flush_triple_buffer(
            triple_buffer
        )


    # ========================================================
    # CTRL + C HANDLING
    # ========================================================

    except KeyboardInterrupt:

        print(
            "\n\nExtraction interrupted "
            "by user."
        )


        print(
            "Saving remaining triples..."
        )


        flush_triple_buffer(
            triple_buffer
        )


        print(
            "Progress saved successfully."
        )


        print(
            "\nBefore resuming:"
        )


        print(
            "Set START_FRESH = False"
        )


        print(
            "Then run the script again."
        )


    # ========================================================
    # ALWAYS STOP CORENLP
    # ========================================================

    finally:

        print(
            "\nStopping CoreNLP..."
        )


        try:

            corenlp_client.stop()

        except Exception:

            pass


        print(
            "CoreNLP stopped."
        )


    # --------------------------------------------------------
    # CALCULATE RUN TIME
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # FINAL RUN REPORT
    # --------------------------------------------------------

    print(
        "\n"
        "========================================"
    )


    print(
        "CURRENT RUN REPORT"
    )


    print(
        "========================================"
    )


    print(
        f"Movies processed this run: "
        f"{run_processed}"
    )


    print(
        f"Movies with triples: "
        f"{run_with_triples}"
    )


    print(
        f"Movies without triples: "
        f"{run_without_triples}"
    )


    print(
        f"Movies skipped: "
        f"{run_skipped}"
    )


    print(
        f"Movies failed: "
        f"{run_failed}"
    )


    print(
        f"Triples extracted this run: "
        f"{run_triples}"
    )


    print(
        f"Time: "
        f"{elapsed_minutes:.2f} minutes"
    )


    print(
        f"Time: "
        f"{elapsed_hours:.2f} hours"
    )


    print(
        "========================================"
    )


    # --------------------------------------------------------
    # SHOW TOTAL DATABASE PROGRESS
    # --------------------------------------------------------

    show_existing_progress()


    # --------------------------------------------------------
    # CLOSE MONGODB
    # --------------------------------------------------------

    mongo_client.close()


# ============================================================
# 17. RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    main()