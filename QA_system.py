


from Question_parser import parse_question
from Query_generator import QueryGenerator


# ============================================================
# 1. MOVIE QA SYSTEM
# ============================================================

class MovieQASystem:

    def __init__(self):

        print("\nConnecting to Neo4j...")

        self.query_generator = QueryGenerator(
            uri="neo4j://127.0.0.1:7687",
            user="neo4j",
            password="bigdata612",
            database="neo4j"
        )

        print("Connected to Neo4j successfully.")


    # ========================================================
    # 2. PROCESS ONE QUESTION
    # ========================================================

    def answer_question(self, question):

        if not question or not question.strip():

            return {
                "question": question,
                "intent": "Unknown",
                "entities": {},
                "answer": "Please enter a question."
            }


        # ----------------------------------------------------
        # STEP 1: PARSE QUESTION
        # ----------------------------------------------------

        intent, entities = parse_question(
            question
        )


        # ----------------------------------------------------
        # STEP 2: HANDLE UNKNOWN QUESTIONS
        # ----------------------------------------------------

        if intent == "Unknown":

            return {
                "question": question,
                "intent": intent,
                "entities": entities,
                "answer": (
                    "I'm sorry, I couldn't understand that "
                    "question yet. Try asking about a movie's "
                    "director, actors, genre, revenue, language, "
                    "company, country, or other supported details."
                )
            }


        # ----------------------------------------------------
        # STEP 3: QUERY NEO4J
        # ----------------------------------------------------

        answer = self.query_generator.get_response(
            intent,
            entities
        )


        # ----------------------------------------------------
        # STEP 4: RETURN COMPLETE RESULT
        # ----------------------------------------------------

        return {
            "question": question,
            "intent": intent,
            "entities": entities,
            "answer": answer
        }


    # ========================================================
    # 3. CLOSE DATABASE CONNECTION
    # ========================================================

    def close(self):

        self.query_generator.close()


# ============================================================
# 4. TERMINAL APPLICATION
# ============================================================

def main():

    print(
        "\n========================================"
    )

    print(
        "MOVIE QA SYSTEM"
    )

    print(
        "========================================"
    )

    print(
        "Ask questions about movies in the database."
    )

    print(
        "Type 'exit' or 'quit' to stop."
    )

    print(
        "========================================"
    )


    qa_system = None


    try:

        # ----------------------------------------------------
        # START SYSTEM
        # ----------------------------------------------------

        qa_system = MovieQASystem()


        # ----------------------------------------------------
        # QUESTION LOOP
        # ----------------------------------------------------

        while True:

            question = input(
                "\nYou: "
            ).strip()


            # ------------------------------------------------
            # EXIT COMMAND
            # ------------------------------------------------

            if question.lower() in [
                "exit",
                "quit"
            ]:

                print(
                    "\nMovie QA System stopped."
                )

                break


            # ------------------------------------------------
            # EMPTY QUESTION
            # ------------------------------------------------

            if not question:

                print(
                    "\nAssistant: Please enter a question."
                )

                continue


            # ------------------------------------------------
            # PROCESS QUESTION
            # ------------------------------------------------

            result = qa_system.answer_question(
                question
            )


            # ------------------------------------------------
            # SHOW DEBUG INFORMATION
            # ------------------------------------------------

            print(
                f"\nIntent: {result['intent']}"
            )

            print(
                f"Entities: {result['entities']}"
            )


            # ------------------------------------------------
            # SHOW FINAL ANSWER
            # ------------------------------------------------

            print(
                f"\nAssistant:\n{result['answer']}"
            )


    except KeyboardInterrupt:

        print(
            "\n\nMovie QA System stopped."
        )


    except Exception as error:

        print(
            "\n========================================"
        )

        print(
            "QA SYSTEM ERROR"
        )

        print(
            "========================================"
        )

        print(
            f"Error type: {type(error).__name__}"
        )

        print(
            f"Error: {error}"
        )


    finally:

        if qa_system is not None:

            qa_system.close()

            print(
                "\nNeo4j connection closed."
            )


# ============================================================
# 5. RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    main()