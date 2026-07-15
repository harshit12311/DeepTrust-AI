import { useState } from "react";
import api from "../services/api";

function VideoUploadCard() {

    const [file, setFile] = useState(null);
    const [prediction, setPrediction] = useState("");
    const [confidence, setConfidence] = useState("");

    const analyzeVideo = async () => {

        if (!file) {
            alert("Select a video first.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {

            // Upload video
            const uploadResponse = await api.post("/upload", formData);

            // Predict video
            const predictionResponse = await api.post("/predict/video", {
                filename: uploadResponse.data.filename
            });

            setPrediction(predictionResponse.data.prediction);
            setConfidence(predictionResponse.data.confidence);

        } catch (error) {
            console.error(error);
            alert("Video prediction failed.");
        }
    };

    return (

        <div className="card">

            <h2>Video Detection</h2>

            <input
                type="file"
                accept="video/*"
                onChange={(e) => setFile(e.target.files[0])}
            />

            <br /><br />

            <button onClick={analyzeVideo}>
                Analyze Video
            </button>

            <br /><br />

            <h3>Prediction: {prediction}</h3>

            <h3>Confidence: {confidence}%</h3>

        </div>

    );
}

export default VideoUploadCard;