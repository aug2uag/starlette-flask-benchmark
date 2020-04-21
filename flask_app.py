#!/usr/bin/env python
from os import urandom
from flask import Flask, jsonify, make_response
app = Flask(__name__)

@app.route("/ping", methods=['GET'])
def hello():
    res = {"foo":"pong"}
    return jsonify(res)

# Returns larger sample JSON from http://json.org/example.html to exercise performance with larger payloads
@app.route("/pong", methods=['GET'])
def big_response():
	return '''{ 
        "glossary": { 
            "title": "example glossary", 
    		"GlossDiv": {
                "title": "S",
    			"GlossList": {
                    "GlossEntry": {
                        "ID": "SGML",
    					"SortAs": "SGML",
    					"GlossTerm": "Standard Generalized Markup Language",
    					"Acronym": "SGML",
    					"Abbrev": "ISO 8879:1986",
    					"GlossDef": {
                            "para": "A meta-markup language, used to create markup languages such as DocBook.",
    						"GlossSeeAlso": ["GML", "XML"]
                        },
    					"GlossSee": "markup"
                    }
                }
            }
        }
    }'''

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=5555)