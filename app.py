from flask import Flask, render_template, request, jsonify


from core.article_manger import ArticleMaker
from crewai import LLM
from config import DefaultCFG

llm = LLM(
    model=DefaultCFG.llm_model,
    api_key=DefaultCFG.api_key
)


maker = ArticleMaker(llm)


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        topic = request.form.get("topic")

        generated_article = maker.make(topic)

        print(f"Generated article for topic '{topic}': {generated_article}")
        return jsonify({"article": generated_article})
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
