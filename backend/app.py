"""Flask application entry point for DeepTrust AI."""

from flask import Flask, jsonify

from routes.upload_routes import upload_bp


# Create the Flask application instance.
app = Flask(__name__)

# Register upload-related endpoints.
app.register_blueprint(upload_bp)


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
