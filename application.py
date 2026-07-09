

from flask import Flask, request, render_template
from Question_parser import parse_question
from Query_generator import QueryGenerator


# ============================================================
# 1. CREATE FLASK APPLICATION
# ============================================================

#app = Flask(__name__)


application=Flask(__name__)

app=application


# ============================================================
# 2. CONNECT TO NEO4J
# ============================================================

generator = QueryGenerator(
    uri="neo4j://127.0.0.1:7687",
    user="neo4j",
    password="bigdata612",
    database="neo4j"
)


# ============================================================
# 3. HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "home.html"
    )


# ============================================================
# 4. MOVIE QA PAGE
# ============================================================

@app.route(
    "/ask",
    methods=["GET", "POST"]
)
def ask():

    question = ""
    response = None
    intent = None
    entities = None


    # --------------------------------------------------------
    # PROCESS QUESTION
    # --------------------------------------------------------

    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        ).strip()


        # ----------------------------------------------------
        # EMPTY QUESTION
        # ----------------------------------------------------

        if not question:

            response = (
                "Please enter a movie-related question."
            )


        else:

            try:

                # --------------------------------------------
                # PARSE QUESTION
                # --------------------------------------------

                intent, entities = parse_question(
                    question
                )


                # --------------------------------------------
                # UNKNOWN QUESTION
                # --------------------------------------------

                if intent == "Unknown":

                    response = (
                        "I couldn't understand that question yet. "
                        "Try asking about directors, actors, genres, "
                        "revenue, languages, companies, countries, "
                        "or movie details."
                    )


                # --------------------------------------------
                # QUERY NEO4J
                # --------------------------------------------

                else:

                    response = generator.get_response(
                        intent,
                        entities
                    )


            except Exception as error:

                print(
                    f"Question processing error: {error}"
                )

                response = (
                    "Something went wrong while processing "
                    "your question. Please try again."
                )


    return render_template(
        "index.html",
        question=question,
        response=response,
        intent=intent,
        entities=entities
    )


# ============================================================
# 5. ABOUT PAGE SECTION REDIRECT
# ============================================================

@app.route("/about")
def about():

    return render_template(
        "home.html",
        scroll_to_about=True
    )


# ============================================================
# 6. ERROR HANDLER
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "home.html"
    ), 404


# ============================================================
# 7. RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print(
        "\n========================================"
    )

    print(
        "MOVIE QA SYSTEM WEB APPLICATION"
    )

    print(
        "========================================"
    )

    print(
        "Open in browser:"
    )

    print(
        "http://127.0.0.1:8081"
    )

    print(
        "========================================\n"
    )


    app.run(
        debug=True,
        port=8081,
        use_reloader=False
    )