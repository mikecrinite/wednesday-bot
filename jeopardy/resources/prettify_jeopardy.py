import json

if __name__ == '__main__':
    with open('JEOPARDY_QUESTIONS.json', 'r') as f:
        pretty = json.dumps(json.load(f), indent=4)

    with open('JEOPARDY_READABLE.json', 'w') as w:
        w.write(pretty)
