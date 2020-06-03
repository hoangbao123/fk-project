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

def check_triple(tx, triples):
    n = len(triples)
    n_true = 0
    res = []
    for triple in triples:
        flag = False
        for record in tx.run( "MATCH (a: Ent {name: $head})-[:RELATION {name: $relation}]->(b: Ent {name: $tail}) return a.name",
                        head=triple[0], tail=triple[1], relation=triple[2]):
            print (record['a.name'])
            n_true += 1
            flag = True
        if (flag):
            res.append((triple[0], triple[1], triple[2], True))
        else:
            res.append((triple[0], triple[2], triple[1], False))
    return (res, n_true)


class Neo4j:
    def __init__(self):
        uri = "bolt://34.87.20.130:7687"
        self.driver = GraphDatabase.driver(uri, auth=("neo4j", "baohn"))

    def push(self, triples):
        with self.driver.session() as session:
            # session.read_transaction(print_friends_of, "Ian")
            # session.write_transaction(push_triples, triples)
            session.write_transaction(push_triple_merge, triples)

    def read(self, triples):
        with self.driver.session() as session:
            # session.read_transaction(print_friends_of, "Ian")
            # session.write_transaction(push_triples, triples)
            return session.read_transaction(check_triple, triples)

if __name__ == "__main__":
    neo = Neo4j()
    neo.push([("bao", "tam", "co"), ("bao", "cho", "thich"), ("hang", "cho", "thich")])
