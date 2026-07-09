from neo4j import GraphDatabase

NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "bigdata612"
NEO4J_DATABASE = "neo4j"

driver = None

try:
    print("Connecting to Neo4j...")

    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD)
    )

    driver.verify_connectivity()

    print("Connection successful!")

    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run("""
            RETURN
                'Movie QA System' AS project,
                1 + 1 AS test
        """)

        record = result.single()

        print("Project:", record["project"])
        print("Test result:", record["test"])

    print("\nNeo4j is ready for the project.")

except Exception as error:
    print("\nCONNECTION FAILED")
    print("Error:", error)

finally:
    if driver is not None:
        driver.close()

    print("\nConnection closed.")