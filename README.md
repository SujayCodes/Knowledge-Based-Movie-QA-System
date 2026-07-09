# 🎬 CineGraph AI — Knowledge-Based Movie Question Answering System

<p align="center">
  <strong>Ask Movies. Explore Connections.</strong>
</p>

<p align="center">
  An intelligent movie question-answering system powered by Natural Language Processing, MongoDB, Stanford CoreNLP, Neo4j, and Flask.
</p>

---

## 📌 Project Overview

**CineGraph AI** is a knowledge-based Movie Question Answering System that allows users to ask natural-language questions about movies and receive answers generated from a Neo4j knowledge graph.

Unlike a traditional movie search application that searches isolated database records, CineGraph AI represents movie information as an interconnected graph of:

- Movies
- Actors
- Directors
- Genres
- Languages
- Production Companies
- Production Countries
- Writers
- Producers
- Music Composers
- Directors of Photography
- NLP-extracted semantic entities and relationships

The system combines structured movie metadata with relationships automatically extracted from movie descriptions using Natural Language Processing.

The complete pipeline transforms raw TMDB movie datasets into a large-scale knowledge graph containing more than **131,000 nodes** and **354,000 relationships**.

---

# 🚀 Key Features

## 🧠 Natural Language Question Understanding

Users can ask questions in natural language, such as:

```text
Who directed Avatar?
```

```text
Who are the actors in Avatar?
```

```text
What is the revenue of Avatar?
```

```text
Show me action movies.
```

```text
Which movies did James Cameron direct?
```

```text
Show me movies with Sam Worthington.
```

```text
What languages are spoken in Avatar?
```

```text
Which company produced Avatar?
```

```text
Which country produced Avatar?
```

```text
Tell me everything about Avatar.
```

The system identifies the user's intent and extracts relevant entities before generating a graph query.

---

## 🕸️ Large-Scale Knowledge Graph

The final Neo4j knowledge graph contains:

| Graph Component | Count |
|---|---:|
| Movie Nodes | 4,803 |
| Person Nodes | 67,718 |
| Genre Nodes | 20 |
| Language Nodes | 61 |
| Company Nodes | 5,014 |
| Country Nodes | 88 |
| NLP Entity Nodes | 53,305 |
| **Total Nodes** | **131,009** |
| NLP `RELATION` Relationships | 88,809 |
| **Total Relationships** | **354,390** |

All **4,803 movies** from the dataset were successfully imported into the knowledge graph.

---

## 🔍 Semantic Relationship Extraction

Stanford CoreNLP OpenIE is used to extract subject-predicate-object triples from movie descriptions.

For example:

```text
James Cameron directed Avatar.
```

is converted into:

```text
Subject   : James Cameron
Relation  : directed
Object    : Avatar
```

These extracted relationships are stored in MongoDB and later imported into Neo4j.

The final NLP extraction process produced approximately:

```text
Completed Movies       : 4,581
Movies With No Triples : 218
Skipped Movies         : 4
Failed Movies          : 0
Stored Triples         : 89,170
```

After graph processing and relationship creation, **88,809 NLP relationships** were stored in Neo4j.

---

# 🏗️ System Architecture

The overall architecture of CineGraph AI is:

```text
┌──────────────────────────┐
│       User Question      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Question Parser      │
│                          │
│  • Intent Recognition    │
│  • Entity Extraction     │
│  • spaCy NLP             │
│  • Regex Patterns        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Query Generator      │
│                          │
│  • Intent Mapping        │
│  • Cypher Generation     │
│  • Parameter Handling    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│  Neo4j Knowledge Graph   │
│                          │
│  • Movies                │
│  • People                │
│  • Genres                │
│  • Languages             │
│  • Companies             │
│  • Countries             │
│  • NLP Relationships     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Natural Language Answer  │
└──────────────────────────┘
```

---

# 🔄 Complete Data Pipeline

The project follows the pipeline:

```text
TMDB Movies Dataset
        +
TMDB Credits Dataset
        │
        ▼
Prepare_dataset.py
        │
        ▼
TMDB_5000_enriched.csv
        │
        ▼
Dataset_cleaning.py
        │
        ▼
MongoDB
        │
        ▼
NLP_triple_extract.py
        │
        ▼
Semantic Triples
        │
        ▼
Neo4j_import.py
        │
        ▼
Neo4j Knowledge Graph
        │
        ▼
Question_parser.py
        │
        ▼
Query_generator.py
        │
        ▼
Flask Web Application
        │
        ▼
Natural Language Answer
```

---

# 📊 Dataset

The project uses the TMDB 5000 Movie Dataset.

## Input Dataset 1 — Movies

```text
tmdb_5000_movies.csv
```

Dataset shape:

```text
4,803 rows × 20 columns
```

It contains information such as:

- Movie title
- Genres
- Overview
- Budget
- Revenue
- Runtime
- Release date
- Popularity
- Vote average
- Vote count
- Production companies
- Production countries
- Spoken languages

---

## Input Dataset 2 — Credits

```text
tmdb_5000_credits.csv
```

Dataset shape:

```text
4,803 rows × 4 columns
```

It contains:

- Movie ID
- Movie title
- Complete cast information
- Complete crew information

---

## Enriched Dataset

The two original datasets are processed and combined using:

```text
Prepare_dataset.py
```

The generated dataset is:

```text
TMDB_5000_enriched.csv
```

Final shape:

```text
4,803 rows × 28 columns
```

The final columns are:

```text
id
title
status
imdb_id
original_language
original_title
overview
tagline
genres
production_companies
production_countries
spoken_languages
cast
director
director_of_photography
writers
producers
music_composer
release_date
budget
revenue
runtime
vote_average
vote_count
imdb_rating
imdb_votes
popularity
poster_path
```

The enriched dataset preserves the complete available cast and crew information required by the project.

---

# 🛠️ Technology Stack

## Backend

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application framework |
| Pandas | Dataset processing and transformation |
| PyMongo | MongoDB communication |
| Neo4j Python Driver | Neo4j database communication |

## Natural Language Processing

| Technology | Purpose |
|---|---|
| spaCy | Question analysis and entity recognition |
| `en_core_web_trf` | Transformer-based English NLP model |
| Stanford CoreNLP | Advanced NLP processing |
| OpenIE | Subject-predicate-object triple extraction |
| Stanza | Python interface for Stanford CoreNLP |
| Regular Expressions | Intent recognition |

## Databases

| Technology | Purpose |
|---|---|
| MongoDB | Storage of cleaned movie data and NLP triples |
| Neo4j | Knowledge graph database |

## Frontend

| Technology | Purpose |
|---|---|
| HTML5 | Page structure |
| CSS3 | Styling and responsive design |
| Jinja2 | Dynamic Flask template rendering |

The frontend intentionally uses **HTML and CSS without JavaScript**.

---

# 📁 Project Structure

```text
Movie QA System/
│
├── movieqa/
│   └── Python virtual environment
│
├── stanza_corenlp/
│   └── Stanford CoreNLP files
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│   ├── home.html
│   └── index.html
│
├── app.py
│
├── Prepare_dataset.py
│
├── Dataset_cleaning.py
│
├── NLP_triple_extract.py
│
├── Neo4j_import.py
│
├── Question_parser.py
│
├── Query_generator.py
│
├── QA_system.py
│
├── Export_to_csv.py
│
├── test_corenlp.py
│
├── tmdb_5000_movies.csv
│
├── tmdb_5000_credits.csv
│
├── TMDB_5000_enriched.csv
│
├── requirements.txt
│
└── README.md
```

---

# 📄 File Descriptions

## `Prepare_dataset.py`

Combines and enriches the two TMDB datasets.

Main responsibilities:

- Loads movie metadata
- Loads credits data
- Matches records using movie IDs
- Extracts cast members
- Extracts directors
- Extracts writers
- Extracts producers
- Extracts music composers
- Extracts directors of photography
- Creates compatibility columns
- Generates the final enriched CSV file

Output:

```text
TMDB_5000_enriched.csv
```

---

## `Dataset_cleaning.py`

Cleans and prepares the enriched dataset for MongoDB.

Main responsibilities:

- Removes invalid movie records
- Handles missing values
- Standardizes textual data
- Corrects inconsistent values
- Converts release dates
- Normalizes multi-value columns
- Removes duplicate records
- Converts data into MongoDB-compatible formats
- Inserts cleaned records into MongoDB

MongoDB database:

```text
MoviesDB
```

Main movie collection:

```text
movies
```

---

## `NLP_triple_extract.py`

Extracts semantic relationships from movie descriptions.

Main responsibilities:

- Reads movie descriptions from MongoDB
- Starts Stanford CoreNLP
- Uses OpenIE for relationship extraction
- Extracts subject-predicate-object triples
- Applies fallback extraction where necessary
- Processes all movie entries
- Tracks extraction progress
- Supports resumable processing
- Stores extracted triples in MongoDB
- Prevents completed movies from being unnecessarily reprocessed

Example triple:

```text
Subject   : James Cameron
Relation  : directed
Object    : Avatar
```

---

## `Neo4j_import.py`

Builds the complete movie knowledge graph.

Main responsibilities:

- Connects to MongoDB
- Connects to Neo4j
- Creates graph constraints
- Creates movie nodes
- Creates person nodes
- Creates genre nodes
- Creates language nodes
- Creates company nodes
- Creates country nodes
- Creates NLP entity nodes
- Creates structured relationships
- Creates NLP-derived relationships
- Verifies the final graph

The import successfully created:

```text
131,009 nodes
354,390 relationships
```

---

## `Question_parser.py`

Converts natural-language questions into structured intents and entities.

Example input:

```text
Who directed Avatar?
```

Parsed result:

```text
Intent: FindDirector
Entities: {'Movie': 'avatar'}
```

The parser uses:

- Regex-based intent patterns
- spaCy transformer NLP
- Named Entity Recognition
- Fallback entity extraction

---

## `Query_generator.py`

Converts parsed intents into Neo4j Cypher queries.

Example:

```text
Question:
Who directed Avatar?
```

The system processes:

```text
Intent:
FindDirector
```

```text
Entity:
Movie = avatar
```

The corresponding graph query searches the Neo4j knowledge graph and returns:

```text
The director of 'Avatar' is James Cameron.
```

---

## `app.py`

The main Flask web application.

Responsibilities:

- Starts the Flask server
- Displays the homepage
- Displays the question-answering interface
- Accepts user questions
- Calls the question parser
- Calls the query generator
- Returns answers to the frontend

Default application address:

```text
http://127.0.0.1:8081
```

---

## `home.html`

The landing page of CineGraph AI.

It contains:

- Project introduction
- Hero section
- Knowledge graph visualization
- Project statistics
- Technology overview
- Architecture explanation
- Navigation to the QA system

---

## `index.html`

The interactive question-answering page.

It contains:

- Question input form
- Suggested questions
- Answer display
- Query information
- Navigation back to the homepage

---

## `style.css`

Contains the complete visual design of the project.

The interface uses:

- Dark navy background
- White and blue graph cards
- Purple highlights
- Cyan accents
- Responsive layouts
- Knowledge graph-inspired visuals

---

# 🔗 Knowledge Graph Model

The graph contains the following major node types:

```text
Movie
Person
Genre
Language
Company
Country
NLP Entity
```

A simplified graph representation is:

```text
(Person)-[:DIRECTED]->(Movie)

(Person)-[:ACTED_IN]->(Movie)

(Person)-[:WROTE]->(Movie)

(Person)-[:PRODUCED]->(Movie)

(Person)-[:COMPOSED_MUSIC_FOR]->(Movie)

(Person)-[:DIRECTOR_OF_PHOTOGRAPHY_FOR]->(Movie)

(Movie)-[:HAS_GENRE]->(Genre)

(Movie)-[:HAS_LANGUAGE]->(Language)

(Movie)-[:PRODUCED_BY]->(Company)

(Movie)-[:PRODUCED_IN]->(Country)

(NLP Entity)-[:RELATION]->(NLP Entity)
```

This structure allows the system to answer both direct factual questions and analytical questions involving graph relationships.

---

# 💬 Supported Question Types

## Movie Director

```text
Who directed Avatar?
```

Intent:

```text
FindDirector
```

---

## Movie Actors

```text
Who are the actors in Avatar?
```

Intent:

```text
FindActors
```

---

## Movies by Genre

```text
Show me action movies.
```

Intent:

```text
FindMoviesByGenre
```

---

## Movies by Director

```text
Which movies did James Cameron direct?
```

Intent:

```text
FindMoviesByDirector
```

---

## Movies by Actor

```text
Show me movies with Sam Worthington.
```

Intent:

```text
FindMoviesByActor
```

---

## Movies by Language

```text
Show me English movies.
```

Intent:

```text
FindMoviesByLanguage
```

---

## Movies by Company

```text
Which movies were produced by Paramount Pictures?
```

Intent:

```text
FindMoviesByCompany
```

---

## Movies by Country

```text
Which movies were produced in the USA?
```

Intent:

```text
FindMoviesByCountry
```

---

## Music Composer

```text
Who composed the music for Avatar?
```

Intent:

```text
FindMusicComposer
```

---

## Director of Photography

```text
Who was the director of photography for Avatar?
```

Intent:

```text
FindDOP
```

---

## Movie Revenue

```text
What is the revenue of Avatar?
```

Intent:

```text
FindRevenue
```

---

## Movie Languages

```text
What languages are spoken in Avatar?
```

Intent:

```text
FindLanguagesOfMovie
```

---

## Production Company

```text
Which company produced Avatar?
```

Intent:

```text
FindCompanyOfMovie
```

---

## Production Country

```text
Which country produced Avatar?
```

Intent:

```text
FindCountryOfMovie
```

---

## Complete Movie Details

```text
Tell me everything about Avatar.
```

Intent:

```text
FindAllDetails
```

---

# 📈 Analytical Questions

The system also supports analytical graph queries.

Examples include:

```text
Who are the top 5 most successful actors?
```

```text
Which genres were most successful in 2010?
```

```text
Who are the top 10 directors by average rating?
```

```text
Which languages have the highest-rated movies?
```

```text
Which production companies have the most successful movies?
```

```text
Which genres have generated the most revenue?
```

```text
What are the highest-grossing movies by country?
```

```text
What is the yearly box office trend?
```

```text
How has genre popularity changed over time?
```

---

# ⚙️ Installation and Setup

## Prerequisites

Before running the project, install:

- Python
- MongoDB Community Server
- Neo4j Desktop
- Java JDK 17
- Stanford CoreNLP

The project was developed and tested with:

```text
MongoDB 8.3.4
Java OpenJDK 17
Neo4j Desktop 2.2.1
```

---

## Step 1 — Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
```

Move into the project directory:

```bash
cd "Movie QA System"
```

---

## Step 2 — Create a Virtual Environment

Create the environment:

```bash
python -m venv movieqa
```

Activate it on Windows:

```bash
movieqa\Scripts\activate
```

If using Conda, activate the corresponding project environment instead.

---

## Step 3 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

Install the spaCy transformer model:

```bash
python -m spacy download en_core_web_trf
```

---

## Step 4 — Verify MongoDB

Check the MongoDB service:

```bash
sc query MongoDB
```

The service should show:

```text
STATE : 4 RUNNING
```

Test the MongoDB connection:

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
print(client.admin.command("ping"))
```

Expected output:

```text
{'ok': 1.0}
```

---

## Step 5 — Verify Java

Run:

```bash
java -version
```

The project uses Java 17.

Example:

```text
openjdk version "17"
```

---

## Step 6 — Prepare Stanford CoreNLP

The Stanford CoreNLP files should be available inside:

```text
stanza_corenlp/
```

Test CoreNLP using:

```bash
python test_corenlp.py
```

A successful test should produce output similar to:

```text
CoreNLP started successfully.

Extracted triples:

James Cameron | directed | Avatar

CoreNLP stopped.
```

---

## Step 7 — Prepare the Enriched Dataset

Place these files in the project directory:

```text
tmdb_5000_movies.csv
tmdb_5000_credits.csv
```

Run:

```bash
python Prepare_dataset.py
```

Expected output:

```text
DATASET PREPARATION COMPLETED

Movies: 4803
Columns: 28
```

The script generates:

```text
TMDB_5000_enriched.csv
```

---

## Step 8 — Clean and Import Data into MongoDB

Run:

```bash
python Dataset_cleaning.py
```

Expected output:

```text
Data successfully imported to MongoDB.
```

---

## Step 9 — Extract NLP Triples

Run:

```bash
python NLP_triple_extract.py
```

The script processes all movie entries and stores extracted relationships in MongoDB.

This process can take significant time because Stanford CoreNLP performs advanced NLP analysis.

The extraction script is designed to track progress so completed movies do not need to be unnecessarily processed again.

---

## Step 10 — Start Neo4j

Open Neo4j Desktop.

Start the local instance used by the project.

The local connection URI is typically:

```text
neo4j://127.0.0.1:7687
```

Ensure the database is running before continuing.

---

## Step 11 — Configure Neo4j Credentials

The project requires a valid Neo4j username and password.

For development, configure the connection using environment variables or a local configuration file that is excluded from Git.

Recommended environment variables:

```text
NEO4J_URI=neo4j://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

> Never commit real database passwords or secrets to a public Git repository.

---

## Step 12 — Import the Knowledge Graph

Run:

```bash
python Neo4j_import.py
```

A successful import should display:

```text
FINAL NEO4J GRAPH VERIFICATION

Movie nodes: 4803
Person nodes: 67718
Genre nodes: 20
Language nodes: 61
Company nodes: 5014
Country nodes: 88
NLP Entity nodes: 53305

Total nodes: 131009

NLP RELATION relationships: 88809
Total relationships: 354390

All 4,803 movie nodes imported: YES

NEO4J IMPORT COMPLETED SUCCESSFULLY
```

---

## Step 13 — Test the Question Parser

Run:

```bash
python Question_parser.py
```

Example input:

```text
Who directed Avatar?
```

Expected result:

```text
Intent: FindDirector
Entities: {'Movie': 'avatar'}
```

---

## Step 14 — Test the Query Generator

Run:

```bash
python Query_generator.py
```

Example output:

```text
Intent: FindDirector
Entities: {'Movie': 'avatar'}

The director of 'Avatar' is James Cameron.
```

---

## Step 15 — Run the Flask Application

Start the application:

```bash
python app.py
```

Open a browser and visit:

```text
http://127.0.0.1:8081
```

The CineGraph AI homepage should now be available.

---

# 🌐 Flask Routes

The application contains two primary routes.

## Homepage

```text
/
```

Displays:

```text
home.html
```

---

## Question Answering Interface

```text
/ask
```

Displays:

```text
index.html
```

and processes user questions using:

```text
Question_parser.py
        ↓
Query_generator.py
        ↓
Neo4j
        ↓
Natural Language Answer
```

---

# 🧪 Example End-to-End Execution

User asks:

```text
Who directed Avatar?
```

### Step 1 — Question Parsing

```text
Intent: FindDirector
Entities: {'Movie': 'avatar'}
```

### Step 2 — Query Generation

The system selects the Cypher query associated with:

```text
FindDirector
```

### Step 3 — Graph Search

Neo4j searches the relationship:

```text
(Person)-[:DIRECTED]->(Movie)
```

### Step 4 — Answer Generation

The final response is:

```text
The director of 'Avatar' is James Cameron.
```

---

# 🎯 Project Objectives

The major objectives of CineGraph AI are:

1. Build a complete movie data processing pipeline.
2. Combine movie metadata and cast/crew information.
3. Store cleaned movie records in MongoDB.
4. Extract semantic relationships from movie descriptions.
5. Build a large-scale Neo4j knowledge graph.
6. Understand natural-language movie questions.
7. Convert user questions into graph queries.
8. Generate human-readable answers.
9. Provide an interactive and visually appealing web interface.
10. Demonstrate the practical integration of NLP and graph databases.

---

# 💡 Why Use a Knowledge Graph?

Traditional relational databases store data in separate tables.

A knowledge graph directly represents relationships.

For example:

```text
James Cameron
      │
   DIRECTED
      │
      ▼
    Avatar
      │
      ├── HAS_GENRE ──────► Action
      │
      ├── ACTED_IN ◄────── Sam Worthington
      │
      ├── PRODUCED_BY ────► Lightstorm Entertainment
      │
      └── PRODUCED_IN ────► USA
```

This makes relationship-based questions more natural and efficient.

The project demonstrates how structured data and NLP-derived knowledge can coexist inside the same graph.

---

# 🌟 Project Highlights

- Processes all 4,803 movies in the dataset
- Preserves complete available cast information
- Extracts detailed crew information
- Uses a transformer-based NLP model
- Performs OpenIE semantic relationship extraction
- Supports resumable large-scale NLP processing
- Stores intermediate data in MongoDB
- Builds a Neo4j knowledge graph
- Contains more than 131,000 graph nodes
- Contains more than 354,000 graph relationships
- Supports factual and analytical questions
- Generates natural-language responses
- Includes a custom responsive frontend
- Uses no frontend JavaScript
- Integrates data engineering, NLP, graph databases, backend development, and frontend design

---

# 🔮 Future Improvements

Future versions of CineGraph AI can include:

- Fuzzy matching for misspelled movie names
- Voice-based question input
- Movie recommendation using graph similarity
- Graph embeddings
- Semantic vector search
- Large Language Model integration
- Multi-hop reasoning
- Conversational question context
- User accounts and question history
- Dynamic graph visualization
- Movie poster integration
- Cloud deployment
- Docker containerization
- REST API support
- Automated graph updates using newer movie datasets

---

# ⚠️ Important Notes

## Database Passwords

Do not upload real Neo4j passwords to GitHub.

Avoid code such as:

```python
QueryGenerator(password="your_real_password")
```

for public repositories.

Use environment variables instead.

---

## Large Dataset Files

Large generated datasets may exceed GitHub's normal file-size limits.

Consider excluding generated or very large files using `.gitignore`.

Example:

```text
movieqa/
stanza_corenlp/
__pycache__/
*.pyc
.env
TMDB_5000_enriched.csv
```

Do not ignore the original dataset files if you intentionally want to distribute them and their licenses permit redistribution.

---

## NLP Processing Time

Processing thousands of movie descriptions with Stanford CoreNLP can take significant time.

The extraction script should be allowed to finish completely.

Avoid manually stopping the process unless necessary.

---

## MongoDB and Neo4j

Both database services must be running when required by the corresponding scripts.

Before starting the final Flask application, ensure Neo4j is running.

---

# 🐛 Troubleshooting

## MongoDB Connection Error

Check:

```bash
sc query MongoDB
```

If MongoDB is not running, start the MongoDB service.

---

## Java Not Found

Check:

```bash
java -version
```

If Java is not recognized, install JDK 17 and configure the system `PATH`.

---

## CoreNLP Port Error

If a port is already in use, stop the previous CoreNLP process or use a free port.

The error may appear as:

```text
possibly something is already running there
```

---

## Neo4j Connection Error

Verify:

- Neo4j Desktop is open
- The local instance is running
- The URI is correct
- The username is correct
- The password is correct

Typical URI:

```text
neo4j://127.0.0.1:7687
```

---

## spaCy Model Not Found

Run:

```bash
python -m spacy download en_core_web_trf
```

---

# 📚 Learning Outcomes

This project demonstrates practical knowledge of:

- Data preprocessing
- Dataset integration
- ETL pipelines
- MongoDB
- NoSQL databases
- Natural Language Processing
- Named Entity Recognition
- Intent classification
- Open Information Extraction
- Subject-predicate-object triples
- Knowledge graph construction
- Neo4j
- Cypher query language
- Flask backend development
- Jinja2 templates
- HTML and CSS frontend development
- Full-stack AI application integration

---

# 👨‍💻 Developer

**Sujay Chand**

B.Tech Computer Science and Engineering

Project Domain:

```text
Natural Language Processing
Knowledge Graphs
Graph Databases
NoSQL Databases
Full-Stack AI Applications
```

---

# 📜 License

This project is intended for educational and academic purposes.

The datasets, libraries, frameworks, and external tools used in this project remain subject to their respective licenses and terms of use.

---

# 🙏 Acknowledgements

This project uses technologies and concepts from:

- TMDB movie datasets
- Python
- MongoDB
- Neo4j
- spaCy
- Stanford CoreNLP
- Stanza
- Flask
- Open Information Extraction

---

<p align="center">
  <strong>CineGraph AI</strong>
</p>

<p align="center">
  Transforming movie data into connected knowledge.
</p>

<p align="center">
  🎬 Ask Movies. Explore Connections. 🕸️
</p>