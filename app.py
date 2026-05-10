from flask import Flask, render_template, request

app = Flask(__name__)


def analyze_code(code):

    warnings = []

    score = 100

    lines = code.split('\n')

    # Detect print statements
    if "print(" in code:
        warnings.append("Debug print statements detected.")
        score -= 10

    # Detect comments
    if "#" not in code:
        warnings.append("Very few comments found.")
        score -= 10

    # Detect long lines
    for line in lines:
        if len(line) > 80:
            warnings.append("Long lines detected.")
            score -= 5
            break

    # Count functions
    function_count = code.count("def ")

    # Too many functions
    if function_count > 5:
        warnings.append("Too many functions detected.")
        score -= 10

    # Too many lines
    if len(lines) > 20:
        warnings.append("Large code block detected.")
        score -= 10

    # Detect global variables
    if "=" in code and "def " not in code:
        warnings.append("Possible global variables detected.")
        score -= 5

    # Detect nested loops
    if "for" in code and "while" in code:
        warnings.append("Complex looping structure detected.")
        score -= 10

    # Prevent negative score
    if score < 0:
        score = 0

    return warnings, score, function_count, len(lines)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    code = request.form['code']

    warnings, score, function_count, line_count = analyze_code(code)

    return render_template(
        'report.html',
        warnings=warnings,
        score=score,
        function_count=function_count,
        line_count=line_count
    )


if __name__ == '__main__':
    app.run(debug=True)