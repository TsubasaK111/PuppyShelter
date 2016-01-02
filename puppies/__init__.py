from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

import puppies.views

app.run(host = "0.0.0.0", port = 5001)
