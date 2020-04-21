#!/usr/bin/env python
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
import uvicorn

async def hello(request):
    return JSONResponse({"hello":"world"})

async def big_response(request):
	return PlainTextResponse('''{ 
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
    }''')

routes = [
    Route('/ping', endpoint=hello),
    Route('/pong', endpoint=big_response),
]

app = Starlette(routes=routes, debug=True)

if __name__ == "__main__":
    uvicorn.run('starlette_app:app', host='0.0.0.0', port=5000, reload=True)
