import os
from flask import Flask, request
from text_process.preprocess import gen_triple
from graph_db.neo4j_driver import Neo4j


app = Flask(__name__)
neo4j = Neo4j()


@app.route("/fact-checking", methods=['POST'])
def check_fact():
    data = request.get_json()
    triples = gen_triple(data['text'])
    res, n_true = neo4j.read(triples)
    response = {}
    response["true_news"] = n_true * 1.0 / len(triples) >= 0.5
    response["num_true_triple"] = n_true
    response["num_triple"] = len(triples)
    triple_res = {}
    for r in res:
        tri = ",".join(r[0:3])
        triple_res[tri] = r[3]
    response["triples_detail"] = triple_res
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)