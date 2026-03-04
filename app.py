from flask import Flask, render_template, request
from grader import AutoGrader, TestCase
import os

app = Flask(__name__)

SUBMISSION_FOLDER = "submissions"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/grade", methods=["POST"])
def grade():

    inputs = request.form.getlist("input[]")
    outputs = request.form.getlist("output[]")

    test_cases = []

    for i in range(len(inputs)):
        test_cases.append(
            TestCase(
                input_data=inputs[i],
                expected_output=outputs[i]
            )
        )

    grader = AutoGrader(time_limit=2.0)

    if not os.path.exists(SUBMISSION_FOLDER):
        return "Submissions folder not found"

    all_results = grader.grade_folder(SUBMISSION_FOLDER, test_cases)

    grader.export_to_excel(all_results)

    return render_template("result.html", results=all_results)


if __name__ == "__main__":
    app.run(debug=True)