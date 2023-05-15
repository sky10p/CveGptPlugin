import json

import quart
import quart_cors
from quart import request
import aiohttp


app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

cve_api_url = "https://cve.circl.lu/api"

@app.get("/api/cve/<string:cveId>")
async def get_cve(cveId):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{cve_api_url}/cve/{cveId}") as resp:
            data = await resp.text()
    return quart.Response(response=data, status=200)

@app.get("/api/cwe")
async def get_cwe_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{cve_api_url}/cwe") as resp:
            data = await resp.text()
    return quart.Response(response=data, status=200)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
