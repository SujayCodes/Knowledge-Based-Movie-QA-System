


import re
import warnings

import spacy


# ============================================================
# 1. SUPPRESS WARNINGS
# ============================================================

warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    module="thinc.shims.pytorch"
)


# ============================================================
# 2. LOAD SPACY MODEL
# ============================================================

print("Loading NLP model...")

nlp = spacy.load(
    "en_core_web_sm"   #"en_core_web_trf"
)

print("NLP model loaded successfully.")


# ============================================================
# 3. INTENT PATTERNS
# ============================================================

INTENT_PATTERNS = [

    # --------------------------------------------------------
    # DIRECTOR OF MOVIE
    # --------------------------------------------------------

    {
        "intent": "FindDirector",

        "patterns": [

            r"who directed (?P<Movie>.+)",

            r"who is the director of (?P<Movie>.+)",

            r"who was the director of (?P<Movie>.+)",

            r"tell me the director of (?P<Movie>.+)",

            r"director of (?P<Movie>.+)"

        ]
    },


    # --------------------------------------------------------
    # ACTORS OF MOVIE
    # --------------------------------------------------------

    {
        "intent": "FindActors",

        "patterns": [

            r"who acted in (?P<Movie>.+)",

            r"who starred in (?P<Movie>.+)",

            r"who are the actors in (?P<Movie>.+)",

            r"who is in the cast of (?P<Movie>.+)",

            r"show me the cast of (?P<Movie>.+)",

            r"cast of (?P<Movie>.+)"

        ]
    },


    # --------------------------------------------------------
    # MOVIES BY GENRE
    # --------------------------------------------------------

    {
        "intent": "FindMoviesByGenre",

        "patterns": [

            r"(?:which|what|show me) movies are (?:in|of) the (?P<Genre>.+?) genre",

            r"(?:which|what|show me) movies are (?P<Genre>.+?) movies",

            r"(?:which|what) movies belong to (?:the )?(?P<Genre>.+?) genre",

            r"(?:which|what) movies fall under (?:the )?(?P<Genre>.+?) genre",

            r"show me (?P<Genre>.+?) movies",

            r"movies in (?:the )?(?P<Genre>.+?) genre"

        ]
    },


    # --------------------------------------------------------
    # MOVIES BY DIRECTOR
    # --------------------------------------------------------

    {
        "intent": "FindMoviesByDirector",

        "patterns": [

            r"which movies did (?P<Person>.+?) direct",

            r"what movies did (?P<Person>.+?) direct",

            r"which movies were directed by (?P<Person>.+)",

            r"what movies were directed by (?P<Person>.+)",

            r"show me movies directed by (?P<Person>.+)",

            r"movies directed by (?P<Person>.+)"

        ]
    },


    # --------------------------------------------------------
    # MOVIES BY LANGUAGE
    # --------------------------------------------------------

    {
        "intent": "FindMoviesByLanguage",

        "patterns": [

            r"which movies are in (?P<Language>.+)",

            r"what movies are in (?P<Language>.+)",

            r"show me movies in (?P<Language>.+)",

            r"which movies use (?:the )?(?P<Language>.+?) language",

            r"(?P<Language>.+?) language movies"

        ]
    },


    # --------------------------------------------------------
    # MOVIES BY COMPANY
    # --------------------------------------------------------

    {
        "intent": "FindMoviesByCompany",

        "patterns": [

            r"which movies are produced by (?P<Company>.+)",

            r"what movies were produced by (?P<Company>.+)",

            r"which movies were made by (?P<Company>.+)",

            r"show me movies produced by (?P<Company>.+)",

            r"movies produced by (?P<Company>.+)"

        ]
    },


    # --------------------------------------------------------
    # MOVIES BY COUNTRY
    # --------------------------------------------------------

    {
        "intent": "FindMoviesByCountry",

        "patterns": [

            r"which movies were produced in (?P<Country>.+)",

            r"what movies were produced in (?P<Country>.+)",

            r"which movies are from (?P<Country>.+)",

            r"show me movies from (?P<Country>.+)",

            r"movies produced in (?P<Country>.+)"

        ]
    },


    # --------------------------------------------------------
    # MUSIC COMPOSER
    # --------------------------------------------------------

    {
        "intent": "FindMusicComposer",

        "patterns": [

            r"who composed the music for (?P<Movie>.+)",

            r"who is the music composer of (?P<Movie>.+)",

            r"who composed (?P<Movie>.+)",

            r"music composer of (?P<Movie>.+)"

        ]
    },


    # --------------------------------------------------------
    # DIRECTOR OF PHOTOGRAPHY
    # --------------------------------------------------------

    {
        "intent": "FindDOP",

        "patterns": [

            r"who was the director of photography for (?P<Movie>.+)",

            r"who is the director of photography of (?P<Movie>.+)",

            r"who is the dop of (?P<Movie>.+)",

            r"director of photography of (?P<Movie>.+)",

            r"dop of (?P<Movie>.+)"

        ]
    },


    # --------------------------------------------------------
    # REVENUE
    # --------------------------------------------------------

    {
        "intent": "FindRevenue",

        "patterns": [

            r"what is the revenue of (?P<Movie>.+)",

            r"what was the revenue of (?P<Movie>.+)",

            r"how much money did (?P<Movie>.+?) make",

            r"how much did (?P<Movie>.+?) earn",

            r"box office revenue of (?P<Movie>.+)",

            r"revenue of (?P<Movie>.+)"

        ]
    },


    # --------------------------------------------------------
    # MOVIES BY ACTOR
    # --------------------------------------------------------

    {
        "intent": "FindMoviesByActor",

        "patterns": [

            r"which movies did (?P<Person>.+?) act in",

            r"what movies did (?P<Person>.+?) act in",

            r"which movies did (?P<Person>.+?) star in",

            r"what movies starred (?P<Person>.+)",

            r"show me movies with (?P<Person>.+)",

            r"movies starring (?P<Person>.+)"

        ]
    },


    # --------------------------------------------------------
    # LANGUAGES OF MOVIE
    # --------------------------------------------------------

    {
        "intent": "FindLanguagesOfMovie",

        "patterns": [

            r"what languages does (?P<Movie>.+?) have",

            r"what languages are spoken in (?P<Movie>.+)",

            r"which languages are spoken in (?P<Movie>.+)",

            r"languages spoken in (?P<Movie>.+)",

            r"languages of (?P<Movie>.+)"

        ]
    },


    # --------------------------------------------------------
    # PRODUCTION COMPANY OF MOVIE
    # --------------------------------------------------------

    {
        "intent": "FindCompanyOfMovie",

        "patterns": [

            r"which company produced (?P<Movie>.+)",

            r"what company produced (?P<Movie>.+)",

            r"who produced (?P<Movie>.+)",

            r"production company of (?P<Movie>.+)"

        ]
    },


    # --------------------------------------------------------
    # COUNTRY OF MOVIE
    # --------------------------------------------------------

    {
        "intent": "FindCountryOfMovie",

        "patterns": [

            r"which country produced (?P<Movie>.+)",

            r"what country produced (?P<Movie>.+)",

            r"which country is (?P<Movie>.+?) from",

            r"country of origin of (?P<Movie>.+)"

        ]
    },


    # --------------------------------------------------------
    # ALL DETAILS
    # --------------------------------------------------------

    {
        "intent": "FindAllDetails",

        "patterns": [

            r"give all details of (?P<Movie>.+)",

            r"give me all details of (?P<Movie>.+)",

            r"tell me everything about (?P<Movie>.+)",

            r"show details of (?P<Movie>.+)",

            r"information about (?P<Movie>.+)"

        ]
    },


    # --------------------------------------------------------
    # ANALYTICAL QUESTIONS
    # --------------------------------------------------------

    {
        "intent": "TopMoviesByGenre",

        "patterns": [

            r"what are the top 20 movies in each genre",

            r"show the top 20 movies in each genre"

        ]
    },


    {
        "intent": "TopSuccessfulActors",

        "patterns": [

            r"who are the top 5 most successful actors",

            r"show me the top 5 most successful actors"

        ]
    },


    {
        "intent": "SuccessfulGenresByYear",

        "patterns": [

            r"which genres were most successful in (?P<Year>\d{4})",

            r"what were the most successful genres in (?P<Year>\d{4})"

        ]
    },


    {
        "intent": "TopDirectorsByRating",

        "patterns": [

            r"who are the top 10 directors by average rating",

            r"show the top 10 directors by average rating"

        ]
    },


    {
        "intent": "LanguageSuccess",

        "patterns": [

            r"which languages have the highest rated movies",

            r"which languages have the highest-rated movies"

        ]
    },


    {
        "intent": "TopCompaniesBySuccess",

        "patterns": [

            r"which production companies have the most successful movies",

            r"show the most successful production companies"

        ]
    },


    {
        "intent": "RevenueTopGenres",

        "patterns": [

            r"which genres have generated the most revenue",

            r"which genres have the highest revenue"

        ]
    },


    {
        "intent": "TopMoviesByCountry",

        "patterns": [

            r"what are the highest grossing movies by country",

            r"what are the highest-grossing movies by country"

        ]
    },


    {
        "intent": "YearlyRevenueTrend",

        "patterns": [

            r"what is the yearly box office trend",

            r"show the yearly box office trend"

        ]
    },


    {
        "intent": "GenrePopularityTrend",

        "patterns": [

            r"how has genre popularity changed over time",

            r"show genre popularity over time"

        ]
    }

]


# ============================================================
# 4. CLEAN QUESTION
# ============================================================

def clean_question(question):

    question = question.strip().lower()

    question = re.sub(
        r"[?!.,]+$",
        "",
        question
    )

    question = re.sub(
        r"\s+",
        " ",
        question
    )

    return question.strip()


# ============================================================
# 5. CLEAN EXTRACTED ENTITY
# ============================================================

def clean_entity(value):

    if value is None:

        return None

    value = value.strip()

    value = re.sub(
        r"[?!.,]+$",
        "",
        value
    )

    return value.strip()


# ============================================================
# 6. REGEX INTENT MATCHING
# ============================================================

def match_intent_patterns(question):

    for intent_data in INTENT_PATTERNS:

        intent = intent_data[
            "intent"
        ]

        for pattern in intent_data[
            "patterns"
        ]:

            match = re.fullmatch(
                pattern,
                question,
                flags=re.IGNORECASE
            )

            if match:

                entities = {}

                for key, value in (
                    match.groupdict().items()
                ):

                    if value is not None:

                        entities[key] = (
                            clean_entity(value)
                        )

                return intent, entities

    return None, {}


# ============================================================
# 7. SPACY FALLBACK
# ============================================================

def spacy_fallback(question):

    doc = nlp(question)

    entities = {}


    for entity in doc.ents:

        text = clean_entity(
            entity.text
        )


        if entity.label_ == "PERSON":

            entities["Person"] = text


        elif entity.label_ == "WORK_OF_ART":

            entities["Movie"] = text


        elif entity.label_ == "LANGUAGE":

            entities["Language"] = text


        elif entity.label_ == "ORG":

            entities["Company"] = text


        elif entity.label_ == "GPE":

            entities["Country"] = text


    return entities


# ============================================================
# 8. MAIN PARSER
# ============================================================

def parse_question(question):

    if not question:

        return "Unknown", {}


    cleaned_question = clean_question(
        question
    )


    # --------------------------------------------------------
    # FIRST: REGEX PATTERN MATCHING
    # --------------------------------------------------------

    intent, entities = match_intent_patterns(
        cleaned_question
    )


    if intent:

        return intent, entities


    # --------------------------------------------------------
    # SECOND: SPACY ENTITY EXTRACTION
    #
    # We extract entities for future NLP expansion,
    # but do not invent an unsupported intent.
    # --------------------------------------------------------

    detected_entities = spacy_fallback(
        cleaned_question
    )


    return "Unknown", detected_entities


# ============================================================
# 9. DIRECT PARSER TEST
# ============================================================

if __name__ == "__main__":

    test_questions = [

        "Who directed Avatar?",

        "Who are the actors in Avatar?",

        "What is the revenue of Avatar?",

        "Show me action movies",

        "Which movies did James Cameron direct?",

        "Show me movies with Sam Worthington",

        "What languages are spoken in Avatar?",

        "Which company produced Avatar?",

        "Which country produced Avatar?",

        "Tell me everything about Avatar",

        "Who are the top 5 most successful actors?",

        "Which genres were most successful in 2010?"

    ]


    print(
        "\n========================================"
    )

    print(
        "QUESTION PARSER TEST"
    )

    print(
        "========================================"
    )


    for question in test_questions:

        intent, entities = parse_question(
            question
        )


        print(
            f"\nQuestion: {question}"
        )

        print(
            f"Intent: {intent}"
        )

        print(
            f"Entities: {entities}"
        )
