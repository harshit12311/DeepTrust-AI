import { useState } from "react";
import api from "../services/api";

function UploadCard() {

    const [file, setFile] = useState(null);
    const [prediction, setPrediction] = useState("");
    const [confidence, setConfidence] = useState("");

    const analyzeImage = async () => {

        if (!file) {
            alert("Select an image first.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {

            // Upload image
            const uploadResponse = await api.post("/upload", formData);

            // Run prediction
            const predictionResponse = await api.post("/predict/image", {
                filename: uploadResponse.data.filename
            });

            setPrediction(predictionResponse.data.prediction);
            setConfidence(predictionResponse.data.confidence);

        }  catch (error) {
    console.error(error);

    if (error.response) {
        alert(error.response.data.message || "Prediction failed.");
    } else {
        alert("Prediction failed.");
    }
}
  }  };

    return (

        <div className="card">

            <h2>Image Detection</h2>

            <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
            />

            <br /><br />

            <button onClick={analyzeImage}>
                Analyze Image
            </button>

            <br /><br />

            <h3>Prediction: {prediction}</h3>

            <h3>Confidence: {confidence}%</h3>

        </div>

    );
}

export default UploadCard;