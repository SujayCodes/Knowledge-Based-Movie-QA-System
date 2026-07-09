from stanza.server import CoreNLPClient

CORENLP_PATH = r"C:\Users\drdev\Downloads\Movie QA System\stanza_corenlp\*"

print("Starting CoreNLP...")

client = CoreNLPClient(
    annotators=[
        "tokenize",
        "ssplit",
        "pos",
        "lemma",
        "ner",
        "depparse",
        "coref",
        "openie"
    ],
    timeout=60000,
    memory="4G",
    classpath=CORENLP_PATH,
    be_quiet=True
)

try:
    client.start()

    print("CoreNLP started successfully.")

    text = "James Cameron directed Avatar. The film became highly successful."

    annotation = client.annotate(text)

    print("\nExtracted triples:")

    for sentence in annotation.sentence:
        for triple in sentence.openieTriple:
            print(
                triple.subject,
                "|",
                triple.relation,
                "|",
                triple.object
            )

finally:
    client.stop()
    print("\nCoreNLP stopped.")