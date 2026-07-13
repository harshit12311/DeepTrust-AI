"""Flask application entry point for DeepTrust AI."""

from flask import Flask, jsonify


# Create the Flask application instance.
app = Flask(__name__)


@app.route("/")
def home():
    """Return the backend service status."""
    return jsonify(
        project="DeepTrust AI",
        status="Backend Running",
        version="1.0",
        message= "Welcome to DeepTrust AI API"
    )


if __name__ == "__main__":
    # Enable debug mode during local development.
    app.run(debug=True)
