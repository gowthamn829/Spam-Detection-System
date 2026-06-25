import { useState } from "react";

function UploadForm({ setRefresh }) {
    const [loading, setLoading] = useState(false);
    const [file, setFile] = useState(null);
    const [trainingType, setTrainingType] = useState("separate");
    const [message, setMessage] = useState("");
    const [testMessage, setTestMessage] = useState("");
    const [prediction, setPrediction] = useState("");

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const trainModel = async () => {

        if (!file) {
            setMessage("Please select a CSV file");
            return;
        }

        const formData = new FormData();

        formData.append("file", file);
        formData.append("type", trainingType);

        try {

            setLoading(true);
            setMessage("Training model...");

            const response = await fetch(
                "http://127.0.0.1:8000/train",
                {
                    method: "POST",
                    body: formData,
                }
            );

            const data = await response.json();

            if (response.ok) {

                setMessage(data.message);

                if (setRefresh) {
                    setRefresh((prev) => prev + 1);
                }

            } else {

                setMessage(
                    data.detail || "Training failed"
                );
            }

        } catch (error) {

            console.error(error);
            setMessage("Server connection failed");

        } finally {

            setLoading(false);
        }
    };
    const predictMessage = async () => {

        const response = await fetch(
            "http://localhost:8080/SpamClassifier/predict",
            {
                method: "POST",
                headers: {
                    "Content-Type": "text/plain"
                },
                body: testMessage
            }
        );
    
        const data = await response.json();
    
        setPrediction(data.prediction);
    };

    return (
        <div className="card">

        <h1>Model Training Submission</h1>
    
        <p className="subtitle">
            Upload a HAM/SPAM dataset, train a model, and test predictions instantly.
        </p>
    
        <div className="upload-box">
    
            <h3>Select Dataset</h3>
    
            <input
                type="file"
                accept=".csv"
                onChange={handleFileChange}
            />
    
            <p>
                <strong>Selected File:</strong>{" "}
                {file ? file.name : "No file selected"}
            </p>
    
        </div>
    
        <div className="mode-box">
    
            <h3>Training Mode</h3>
    
            <label>
                <input
                    type="radio"
                    value="separate"
                    checked={trainingType === "separate"}
                    onChange={(e) =>
                        setTrainingType(e.target.value)
                    }
                />
                Separate Training
            </label>
    
            <label>
                <input
                    type="radio"
                    value="merge"
                    checked={trainingType === "merge"}
                    onChange={(e) =>
                        setTrainingType(e.target.value)
                    }
                />
                Merge Training
            </label>
    
        </div>
    
        <button
            className="train-btn"
            onClick={trainModel}
            disabled={loading}
        >
            {loading ? "Training..." : "Train Model"}
        </button>
    
        {message && (
            <div className="status-box">
                {message}
            </div>
        )}
    
        <hr style={{ margin: "30px 0" }} />
    
        <h2>Quick Test Prediction</h2>
    
        <textarea
            className="prediction-textarea"
            rows="5"
            placeholder="Enter a message to test..."
            value={testMessage}
            onChange={(e) =>
                setTestMessage(e.target.value)
            }
        />
    
        <br />
        <br />
    
        <button
            className="predict-btn"
            onClick={predictMessage}
        >
            Predict
        </button>
    
        {prediction && (
            <div className="prediction-result">
                Prediction: {prediction}
            </div>
        )}
    
    </div>
    );
}

export default UploadForm;