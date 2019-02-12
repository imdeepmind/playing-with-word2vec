from flask import Flask, jsonify, request
from flask_cors import CORS
import gensim
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def index():
    return jsonify({
        "success" : True
    })


@app.route("/similar/", methods=['GET'])
def similar():
    try:
        word = request.args.get('word')
        if word:
            model = gensim.models.KeyedVectors.load_word2vec_format('model.bin', binary=True)
            data = model.wv.most_similar(word)
            similar = json.dumps(data, separators=(',',':'))
            return jsonify({
                "success" : True,
                "data": data
            })
        else:
            return jsonify({
                "success" : False,
                "message": "Please provide a word"
            })
    except Exception as ex:
        print(ex)
        return jsonify({
            "success": False,
            "message" : "Something went wrong"
        })
