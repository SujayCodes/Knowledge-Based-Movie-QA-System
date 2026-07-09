
from neo4j import GraphDatabase


# ============================================================
# 1. QUERY GENERATOR
# ============================================================

class QueryGenerator:

    def __init__(
        self,
        uri="neo4j://127.0.0.1:7687",
        user="neo4j",
        password="bigdata612",
        database="neo4j"
    ):

        self.database = database

        self.driver = GraphDatabase.driver(
            uri,
            auth=(user, password)
        )

        self.driver.verify_connectivity()


    # ========================================================
    # 2. CLOSE CONNECTION
    # ========================================================

    def close(self):

        self.driver.close()


    # ========================================================
    # 3. EXECUTE QUERY
    # ========================================================

    def execute_query(
        self,
        query,
        parameters=None
    ):

        with self.driver.session(
            database=self.database
        ) as session:

            result = session.run(
                query,
                parameters or {}
            )

            return [
                record.data()
                for record in result
            ]


    # ========================================================
    # 4. GENERATE CYPHER QUERY
    # ========================================================

    def generate_query(
        self,
        intent,
        entities
    ):

        # ----------------------------------------------------
        # FIND DIRECTOR
        # ----------------------------------------------------

        if intent == "FindDirector":

            return """
            MATCH (m:Movie)-[:DIRECTED_BY]->(d:Person)
            WHERE toLower(m.title) = toLower($movie_title)
            RETURN DISTINCT d.name AS director
            ORDER BY director
            """, {
                "movie_title": entities.get("Movie")
            }


        # ----------------------------------------------------
        # FIND ACTORS
        # ----------------------------------------------------

        elif intent == "FindActors":

            return """
            MATCH (m:Movie)-[:ACTED_IN]->(a:Person)
            WHERE toLower(m.title) = toLower($movie_title)
            RETURN DISTINCT a.name AS actor
            ORDER BY actor
            """, {
                "movie_title": entities.get("Movie")
            }


        # ----------------------------------------------------
        # FIND MOVIES BY GENRE
        # ----------------------------------------------------

        elif intent == "FindMoviesByGenre":

            return """
            MATCH (m:Movie)-[:BELONGS_TO_GENRE]->(g:Genre)
            WHERE toLower(g.name) = toLower($genre_name)
            RETURN DISTINCT
                m.title AS movie_title,
                m.vote_average AS rating
            ORDER BY rating DESC
            LIMIT 20
            """, {
                "genre_name": entities.get("Genre")
            }


        # ----------------------------------------------------
        # FIND MOVIES BY DIRECTOR
        # ----------------------------------------------------

        elif intent == "FindMoviesByDirector":

            return """
            MATCH (m:Movie)-[:DIRECTED_BY]->(d:Person)
            WHERE toLower(d.name) = toLower($director_name)
            RETURN DISTINCT
                m.title AS movie_title,
                m.release_date AS release_date
            ORDER BY release_date DESC
            LIMIT 20
            """, {
                "director_name": entities.get("Person")
            }


        # ----------------------------------------------------
        # FIND MOVIES BY LANGUAGE
        # ----------------------------------------------------

        elif intent == "FindMoviesByLanguage":

            return """
            MATCH (m:Movie)-[:SPOKEN_IN]->(l:Language)
            WHERE toLower(l.name) = toLower($language_name)
            RETURN DISTINCT
                m.title AS movie_title,
                m.vote_average AS rating
            ORDER BY rating DESC
            LIMIT 20
            """, {
                "language_name": entities.get("Language")
            }


        # ----------------------------------------------------
        # FIND MOVIES BY COMPANY
        # ----------------------------------------------------

        elif intent == "FindMoviesByCompany":

            return """
            MATCH (m:Movie)-[:PRODUCTION_COMPANY]->(c:Company)
            WHERE toLower(c.name) = toLower($company_name)
            RETURN DISTINCT
                m.title AS movie_title,
                m.release_date AS release_date
            ORDER BY release_date DESC
            LIMIT 20
            """, {
                "company_name": entities.get("Company")
            }


        # ----------------------------------------------------
        # FIND MOVIES BY COUNTRY
        # ----------------------------------------------------

        elif intent == "FindMoviesByCountry":

            return """
            MATCH (m:Movie)-[:PRODUCED_IN]->(c:Country)
            WHERE toLower(c.name) = toLower($country_name)
            RETURN DISTINCT
                m.title AS movie_title,
                m.vote_average AS rating
            ORDER BY rating DESC
            LIMIT 20
            """, {
                "country_name": entities.get("Country")
            }


        # ----------------------------------------------------
        # FIND MUSIC COMPOSER
        # ----------------------------------------------------

        elif intent == "FindMusicComposer":

            return """
            MATCH (m:Movie)-[:COMPOSED_BY]->(p:Person)
            WHERE toLower(m.title) = toLower($movie_title)
            RETURN DISTINCT p.name AS music_composer
            ORDER BY music_composer
            """, {
                "movie_title": entities.get("Movie")
            }


        # ----------------------------------------------------
        # FIND DIRECTOR OF PHOTOGRAPHY
        # ----------------------------------------------------

        elif intent == "FindDOP":

            return """
            MATCH (m:Movie)-[:DOP_BY]->(p:Person)
            WHERE toLower(m.title) = toLower($movie_title)
            RETURN DISTINCT
                p.name AS director_of_photography
            ORDER BY director_of_photography
            """, {
                "movie_title": entities.get("Movie")
            }


        # ----------------------------------------------------
        # FIND REVENUE
        # ----------------------------------------------------

        elif intent == "FindRevenue":

            return """
            MATCH (m:Movie)
            WHERE toLower(m.title) = toLower($movie_title)
            RETURN
                m.title AS title,
                m.revenue AS revenue
            LIMIT 1
            """, {
                "movie_title": entities.get("Movie")
            }


        # ----------------------------------------------------
        # FIND MOVIES BY ACTOR
        # ----------------------------------------------------

        elif intent == "FindMoviesByActor":

            return """
            MATCH (m:Movie)-[:ACTED_IN]->(p:Person)
            WHERE toLower(p.name) = toLower($actor_name)
            RETURN DISTINCT
                m.title AS movie_title,
                m.release_date AS release_date
            ORDER BY release_date DESC
            LIMIT 20
            """, {
                "actor_name": entities.get("Person")
            }


        # ----------------------------------------------------
        # FIND LANGUAGES OF MOVIE
        # ----------------------------------------------------

        elif intent == "FindLanguagesOfMovie":

            return """
            MATCH (m:Movie)-[:SPOKEN_IN]->(l:Language)
            WHERE toLower(m.title) = toLower($movie_title)
            RETURN DISTINCT l.name AS language
            ORDER BY language
            """, {
                "movie_title": entities.get("Movie")
            }


        # ----------------------------------------------------
        # FIND COMPANY OF MOVIE
        # ----------------------------------------------------

        elif intent == "FindCompanyOfMovie":

            return """
            MATCH (m:Movie)-[:PRODUCTION_COMPANY]->(c:Company)
            WHERE toLower(m.title) = toLower($movie_title)
            RETURN DISTINCT c.name AS company
            ORDER BY company
            """, {
                "movie_title": entities.get("Movie")
            }


        # ----------------------------------------------------
        # FIND COUNTRY OF MOVIE
        # ----------------------------------------------------

        elif intent == "FindCountryOfMovie":

            return """
            MATCH (m:Movie)-[:PRODUCED_IN]->(c:Country)
            WHERE toLower(m.title) = toLower($movie_title)
            RETURN DISTINCT c.name AS country
            ORDER BY country
            """, {
                "movie_title": entities.get("Movie")
            }


        # ----------------------------------------------------
        # FIND ALL MOVIE DETAILS
        # ----------------------------------------------------

        elif intent == "FindAllDetails":

            return """
            MATCH (m:Movie)
            WHERE toLower(m.title) = toLower($movie_title)

            OPTIONAL MATCH (m)-[:DIRECTED_BY]->(d:Person)
            OPTIONAL MATCH (m)-[:BELONGS_TO_GENRE]->(g:Genre)
            OPTIONAL MATCH (m)-[:SPOKEN_IN]->(l:Language)

            RETURN
                m.title AS title,
                m.release_date AS release_date,
                m.budget AS budget,
                m.runtime AS runtime,
                m.vote_average AS vote_average,
                m.status AS status,
                m.revenue AS revenue,
                m.original_language AS original_language,
                collect(DISTINCT d.name) AS directors,
                collect(DISTINCT g.name) AS genres,
                collect(DISTINCT l.name) AS languages
            LIMIT 1
            """, {
                "movie_title": entities.get("Movie")
            }


        # ----------------------------------------------------
        # TOP 20 MOVIES IN EACH GENRE
        # ----------------------------------------------------

        elif intent == "TopMoviesByGenre":

            return """
            MATCH (m:Movie)-[:BELONGS_TO_GENRE]->(g:Genre)
            WHERE m.vote_average IS NOT NULL

            WITH
                g,
                m
            ORDER BY
                g.name,
                m.vote_average DESC

            WITH
                g,
                collect({
                    movie: m.title,
                    rating: m.vote_average
                })[0..20] AS top_movies

            UNWIND top_movies AS item

            RETURN
                g.name AS genre,
                item.movie AS movie,
                item.rating AS rating

            ORDER BY
                genre,
                rating DESC
            """, {}


        # ----------------------------------------------------
        # TOP SUCCESSFUL ACTORS
        # ----------------------------------------------------

        elif intent == "TopSuccessfulActors":

            return """
            MATCH (m:Movie)-[:ACTED_IN]->(a:Person)

            WHERE
                m.vote_average IS NOT NULL
                AND m.vote_average > 7.5

            RETURN
                a.name AS actor,
                count(DISTINCT m) AS successful_movies,
                avg(m.vote_average) AS average_rating

            ORDER BY
                successful_movies DESC,
                average_rating DESC

            LIMIT 5
            """, {}


        # ----------------------------------------------------
        # SUCCESSFUL GENRES BY YEAR
        # ----------------------------------------------------

        elif intent == "SuccessfulGenresByYear":

            return """
            MATCH (m:Movie)-[:BELONGS_TO_GENRE]->(g:Genre)

            WHERE
                m.release_date STARTS WITH $year
                AND m.vote_average IS NOT NULL

            RETURN
                g.name AS genre,
                avg(m.vote_average) AS average_rating,
                count(DISTINCT m) AS movie_count

            ORDER BY
                average_rating DESC

            LIMIT 10
            """, {
                "year": entities.get("Year")
            }


        # ----------------------------------------------------
        # TOP DIRECTORS
        # ----------------------------------------------------

        elif intent == "TopDirectorsByRating":

            return """
            MATCH (m:Movie)-[:DIRECTED_BY]->(d:Person)

            WHERE m.vote_average IS NOT NULL

            WITH
                d,
                avg(m.vote_average) AS avg_rating,
                count(DISTINCT m) AS movie_count

            WHERE movie_count >= 2

            RETURN
                d.name AS director,
                avg_rating,
                movie_count

            ORDER BY avg_rating DESC

            LIMIT 10
            """, {}


        # ----------------------------------------------------
        # LANGUAGE SUCCESS
        # ----------------------------------------------------

        elif intent == "LanguageSuccess":

            return """
            MATCH (m:Movie)-[:SPOKEN_IN]->(l:Language)

            WHERE m.vote_average IS NOT NULL

            RETURN
                l.name AS language,
                avg(m.vote_average) AS average_rating,
                count(DISTINCT m) AS movie_count

            ORDER BY average_rating DESC

            LIMIT 20
            """, {}


        # ----------------------------------------------------
        # TOP COMPANIES
        # ----------------------------------------------------

        elif intent == "TopCompaniesBySuccess":

            return """
            MATCH (m:Movie)-[:PRODUCTION_COMPANY]->(c:Company)

            WHERE
                m.vote_average IS NOT NULL
                AND m.vote_average > 7.5

            RETURN
                c.name AS company,
                count(DISTINCT m) AS successful_movies,
                avg(m.vote_average) AS average_rating

            ORDER BY
                successful_movies DESC,
                average_rating DESC

            LIMIT 20
            """, {}


        # ----------------------------------------------------
        # TOP GENRES BY REVENUE
        # ----------------------------------------------------

        elif intent == "RevenueTopGenres":

            return """
            MATCH (m:Movie)-[:BELONGS_TO_GENRE]->(g:Genre)

            WHERE
                m.revenue IS NOT NULL
                AND m.revenue > 0

            RETURN
                g.name AS genre,
                sum(m.revenue) AS total_revenue,
                count(DISTINCT m) AS movie_count

            ORDER BY total_revenue DESC
            """, {}


        # ----------------------------------------------------
        # TOP MOVIES BY COUNTRY
        # ----------------------------------------------------

        elif intent == "TopMoviesByCountry":

            return """
            MATCH (m:Movie)-[:PRODUCED_IN]->(c:Country)

            WHERE
                m.revenue IS NOT NULL
                AND m.revenue > 0

            WITH
                c,
                m

            ORDER BY
                c.name,
                m.revenue DESC

            WITH
                c,
                collect({
                    movie: m.title,
                    revenue: m.revenue
                })[0..5] AS top_movies

            UNWIND top_movies AS item

            RETURN
                c.name AS country,
                item.movie AS movie,
                item.revenue AS revenue

            ORDER BY
                country,
                revenue DESC
            """, {}


        # ----------------------------------------------------
        # YEARLY REVENUE TREND
        # ----------------------------------------------------

        elif intent == "YearlyRevenueTrend":

            return """
            MATCH (m:Movie)

            WHERE
                m.release_date IS NOT NULL
                AND size(m.release_date) >= 4
                AND m.revenue IS NOT NULL
                AND m.revenue > 0

            WITH
                substring(m.release_date, 0, 4) AS year,
                m

            WHERE year =~ '\\\\d{4}'

            RETURN
                year,
                sum(m.revenue) AS total_revenue,
                count(DISTINCT m) AS movie_count

            ORDER BY year ASC
            """, {}


        # ----------------------------------------------------
        # GENRE POPULARITY TREND
        # ----------------------------------------------------

        elif intent == "GenrePopularityTrend":

            return """
            MATCH (m:Movie)-[:BELONGS_TO_GENRE]->(g:Genre)

            WHERE
                m.release_date IS NOT NULL
                AND size(m.release_date) >= 4

            WITH
                substring(m.release_date, 0, 4) AS year,
                g,
                m

            WHERE year =~ '\\\\d{4}'

            RETURN
                year,
                g.name AS genre,
                count(DISTINCT m) AS movie_count

            ORDER BY
                year ASC,
                movie_count DESC
            """, {}


        # ----------------------------------------------------
        # UNKNOWN INTENT
        # ----------------------------------------------------

        return None, {}


    # ========================================================
    # 5. FORMAT MONEY
    # ========================================================

    @staticmethod
    def format_money(value):

        if value is None or value <= 0:

            return "Unknown"

        return f"${value:,.0f}"


    # ========================================================
    # 6. FORMAT LIST
    # ========================================================

    @staticmethod
    def format_list(values):

        values = [
            str(value)
            for value in values
            if value is not None
        ]

        return ", ".join(values)


    # ========================================================
    # 7. GET NATURAL-LANGUAGE RESPONSE
    # ========================================================

    def get_response(
        self,
        intent,
        entities
    ):

        query, parameters = self.generate_query(
            intent,
            entities
        )


        if not query:

            return (
                "I'm sorry, I couldn't understand "
                "that question yet."
            )


        try:

            results = self.execute_query(
                query,
                parameters
            )

        except Exception as error:

            print(
                f"Neo4j query error: {error}"
            )

            return (
                "A database error occurred while "
                "processing your question."
            )


        if not results:

            return (
                "I couldn't find any matching results "
                "in the movie database."
            )


        # ----------------------------------------------------
        # SIMPLE QUESTION RESPONSES
        # ----------------------------------------------------

        if intent == "FindDirector":

            names = [
                row["director"]
                for row in results
            ]

            return (
                f"The director of "
                f"'{entities['Movie'].title()}' is "
                f"{self.format_list(names)}."
            )


        elif intent == "FindActors":

            names = [
                row["actor"]
                for row in results
            ]

            return (
                f"The actors in "
                f"'{entities['Movie'].title()}' are: "
                f"{self.format_list(names)}."
            )


        elif intent == "FindMoviesByGenre":

            movies = [
                row["movie_title"]
                for row in results
            ]

            return (
                f"Top movies in the "
                f"'{entities['Genre'].title()}' genre include: "
                f"{self.format_list(movies)}."
            )


        elif intent == "FindMoviesByDirector":

            movies = [
                row["movie_title"]
                for row in results
            ]

            return (
                f"Movies directed by "
                f"{entities['Person'].title()} include: "
                f"{self.format_list(movies)}."
            )


        elif intent == "FindMoviesByLanguage":

            movies = [
                row["movie_title"]
                for row in results
            ]

            return (
                f"Movies in "
                f"'{entities['Language'].title()}' include: "
                f"{self.format_list(movies)}."
            )


        elif intent == "FindMoviesByCompany":

            movies = [
                row["movie_title"]
                for row in results
            ]

            return (
                f"Movies produced by "
                f"'{entities['Company'].title()}' include: "
                f"{self.format_list(movies)}."
            )


        elif intent == "FindMoviesByCountry":

            movies = [
                row["movie_title"]
                for row in results
            ]

            return (
                f"Movies produced in "
                f"'{entities['Country'].title()}' include: "
                f"{self.format_list(movies)}."
            )


        elif intent == "FindMusicComposer":

            names = [
                row["music_composer"]
                for row in results
            ]

            return (
                f"The music composer for "
                f"'{entities['Movie'].title()}' is "
                f"{self.format_list(names)}."
            )


        elif intent == "FindDOP":

            names = [
                row["director_of_photography"]
                for row in results
            ]

            return (
                f"The director of photography for "
                f"'{entities['Movie'].title()}' is "
                f"{self.format_list(names)}."
            )


        elif intent == "FindRevenue":

            row = results[0]

            return (
                f"The revenue of "
                f"'{row['title'].title()}' is "
                f"{self.format_money(row['revenue'])}."
            )


        elif intent == "FindMoviesByActor":

            movies = [
                row["movie_title"]
                for row in results
            ]

            return (
                f"Movies featuring "
                f"{entities['Person'].title()} include: "
                f"{self.format_list(movies)}."
            )


        elif intent == "FindLanguagesOfMovie":

            languages = [
                row["language"]
                for row in results
            ]

            return (
                f"The languages spoken in "
                f"'{entities['Movie'].title()}' are: "
                f"{self.format_list(languages)}."
            )


        elif intent == "FindCompanyOfMovie":

            companies = [
                row["company"]
                for row in results
            ]

            return (
                f"The production companies for "
                f"'{entities['Movie'].title()}' are: "
                f"{self.format_list(companies)}."
            )


        elif intent == "FindCountryOfMovie":

            countries = [
                row["country"]
                for row in results
            ]

            return (
                f"The countries associated with "
                f"'{entities['Movie'].title()}' are: "
                f"{self.format_list(countries)}."
            )


        elif intent == "FindAllDetails":

            row = results[0]

            return (
                f"Details of '{row['title'].title()}':\n"
                f"- Release Date: {row['release_date'] or 'Unknown'}\n"
                f"- Budget: {self.format_money(row['budget'])}\n"
                f"- Revenue: {self.format_money(row['revenue'])}\n"
                f"- Runtime: {row['runtime'] or 'Unknown'} minutes\n"
                f"- Rating: {row['vote_average'] or 'Unknown'}\n"
                f"- Status: {row['status'] or 'Unknown'}\n"
                f"- Original Language: "
                f"{row['original_language'] or 'Unknown'}\n"
                f"- Director(s): "
                f"{self.format_list(row['directors']) or 'Unknown'}\n"
                f"- Genres: "
                f"{self.format_list(row['genres']) or 'Unknown'}\n"
                f"- Spoken Languages: "
                f"{self.format_list(row['languages']) or 'Unknown'}"
            )


        # ----------------------------------------------------
        # ANALYTICAL RESPONSES
        # ----------------------------------------------------

        elif intent == "TopMoviesByGenre":

            grouped = {}

            for row in results:

                grouped.setdefault(
                    row["genre"],
                    []
                ).append(
                    f"{row['movie']} ({row['rating']})"
                )

            lines = []

            for genre, movies in grouped.items():

                lines.append(
                    f"{genre}: {', '.join(movies)}"
                )

            return (
                "Top movies by genre:\n"
                + "\n".join(lines)
            )


        elif intent == "TopSuccessfulActors":

            lines = [
                (
                    f"{row['actor']} — "
                    f"{row['successful_movies']} successful movies, "
                    f"average rating {row['average_rating']:.2f}"
                )
                for row in results
            ]

            return (
                "Top 5 most successful actors:\n"
                + "\n".join(lines)
            )


        elif intent == "SuccessfulGenresByYear":

            lines = [
                (
                    f"{row['genre']} — "
                    f"average rating {row['average_rating']:.2f}, "
                    f"{row['movie_count']} movies"
                )
                for row in results
            ]

            return (
                f"Most successful genres in "
                f"{entities['Year']}:\n"
                + "\n".join(lines)
            )


        elif intent == "TopDirectorsByRating":

            lines = [
                (
                    f"{row['director']} — "
                    f"average rating {row['avg_rating']:.2f} "
                    f"across {row['movie_count']} movies"
                )
                for row in results
            ]

            return (
                "Top directors by average rating:\n"
                + "\n".join(lines)
            )


        elif intent == "LanguageSuccess":

            lines = [
                (
                    f"{row['language']} — "
                    f"average rating {row['average_rating']:.2f} "
                    f"across {row['movie_count']} movies"
                )
                for row in results
            ]

            return (
                "Languages with the highest-rated movies:\n"
                + "\n".join(lines)
            )


        elif intent == "TopCompaniesBySuccess":

            lines = [
                (
                    f"{row['company']} — "
                    f"{row['successful_movies']} successful movies"
                )
                for row in results
            ]

            return (
                "Most successful production companies:\n"
                + "\n".join(lines)
            )


        elif intent == "RevenueTopGenres":

            lines = [
                (
                    f"{row['genre']} — "
                    f"{self.format_money(row['total_revenue'])}"
                )
                for row in results
            ]

            return (
                "Genres ranked by total revenue:\n"
                + "\n".join(lines)
            )


        elif intent == "TopMoviesByCountry":

            grouped = {}

            for row in results:

                grouped.setdefault(
                    row["country"],
                    []
                ).append(
                    f"{row['movie']} "
                    f"({self.format_money(row['revenue'])})"
                )

            lines = [
                f"{country}: {', '.join(movies)}"
                for country, movies in grouped.items()
            ]

            return (
                "Highest-grossing movies by country:\n"
                + "\n".join(lines)
            )


        elif intent == "YearlyRevenueTrend":

            lines = [
                (
                    f"{row['year']}: "
                    f"{self.format_money(row['total_revenue'])}"
                )
                for row in results
            ]

            return (
                "Yearly box-office revenue trend:\n"
                + "\n".join(lines)
            )


        elif intent == "GenrePopularityTrend":

            lines = [
                (
                    f"{row['year']} — "
                    f"{row['genre']}: "
                    f"{row['movie_count']} movies"
                )
                for row in results
            ]

            return (
                "Genre popularity over time:\n"
                + "\n".join(lines)
            )


        return (
            "The query ran successfully, but I could not "
            "format the response."
        )


# ============================================================
# 8. DIRECT FILE TEST
# ============================================================

if __name__ == "__main__":

    generator = QueryGenerator(
        password="bigdata612"
    )

    try:

        test_cases = [

            (
                "FindDirector",
                {
                    "Movie": "avatar"
                }
            ),

            (
                "FindActors",
                {
                    "Movie": "avatar"
                }
            ),

            (
                "FindRevenue",
                {
                    "Movie": "avatar"
                }
            ),

            (
                "FindMoviesByGenre",
                {
                    "Genre": "action"
                }
            )

        ]


        for intent, entities in test_cases:

            print(
                "\n========================================"
            )

            print(
                f"Intent: {intent}"
            )

            print(
                f"Entities: {entities}"
            )

            print(
                "========================================"
            )

            response = generator.get_response(
                intent,
                entities
            )

            print(response)


    finally:

        generator.close()