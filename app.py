from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

def extrair_link(api_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        if "token" in data:
            return data["token"]
        elif "data" in data and isinstance(data["data"], list) and "src" in data["data"][0]:
            return data["data"][0]["src"]
        else:
            return "Formato de resposta desconhecido."
    except requests.exceptions.RequestException as e:
        return f"Erro na requisição: {e}"
    except ValueError:
        return "Erro ao decodificar JSON."


@app.route("/", methods=["GET", "POST"])
def index():
    link = None
    if request.method == "POST":
        anime = request.form.get("anime").lower().replace(" ", "-")
        episodio = request.form.get("episodio")
        api_url = f"https://animefire.plus/video/{anime}/{episodio}"
        link = extrair_link(api_url)
    return render_template("index.html", link=link)



if __name__ == "__main__":
    app.run(debug=True)
