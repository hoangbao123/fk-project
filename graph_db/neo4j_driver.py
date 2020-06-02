from neo4j import GraphDatabase


def push_triples(tx, triples):
    for triple in triples:
        result = tx.run("CREATE (a:Ent {name: $head}) "
                        "CREATE (b:Ent {name: $tail}) "
                        "CREATE (a)-[:RELATION {name: $relation}]->(b)",
                        head=triple[0], tail=triple[1], relation=triple[2])
        print(result)


def push_triple_merge(tx, triples):
    for triple in triples:
        result = tx.run("MERGE (a: Ent {name: $head})"
                        "MERGE (b: Ent {name: $tail})"
                        "MERGE (a)-[:RELATION {name: $relation}]->(b)",
                        head=triple[0], tail=triple[1], relation=triple[2])
        print(result)


class Neo4j:
    def __init__(self):
        uri = "bolt://34.87.20.130:7687"
        self.driver = GraphDatabase.driver(uri, auth=("neo4j", "baohn"))

    def push(self, triples):
        with self.driver.session() as session:
            # session.read_transaction(print_friends_of, "Ian")
            # session.write_transaction(push_triples, triples)
            session.write_transaction(push_triple_merge, triples)


if __name__ == "__main__":
    neo = Neo4j()
    neo.push([("bao", "tam", "co"), ("bao", "cho", "thich"), ("hang", "cho", "thich")])
