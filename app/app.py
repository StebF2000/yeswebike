import sys
import os
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def dashboard():
    # print(os.listdir('dashboard/pages'),file=sys.stderr)
    return render_template('pages/dashboard.html')


@app.route('/docs')
def docs():
    # print(os.listdir('dashboard/pages'),file=sys.stderr)
    return render_template('docs/documentation.html')


if __name__ == '__main__':
    app.run()
