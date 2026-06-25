import { useState } from "react";

function Home() {

    const [message, setMessage] = useState("");
    const [prediction, setPrediction] = useState("");

    const predictMessage = async () => {

        const response = await fetch(
            "http://localhost:8080/SpamClassifier/predict",
            {
                method: "POST",
                headers: {
                    "Content-Type": "text/plain"
                },
                body: message
            }
        );

        const data = await response.json();

        setPrediction(data.prediction);
    };

    return (
        <div className="home-page">

            <div className="home-card">

                <h1>Spam Detection System</h1>

                <p>
                    Detect spam messages using a machine learning model
                    trained on HAM and SPAM datasets.
                </p>

                <div className="feature-grid">

                    <div className="feature-box">
                        Detect spam messages instantly
                    </div>

                    <div className="feature-box">
                        Train custom models using CSV files
                    </div>

                    <div className="feature-box">
                        Track training history
                    </div>

                    <div className="feature-box">
                        View model evaluation insights
                    </div>

                 </div>

                <textarea
                    placeholder="Enter message..."
                    value={message}
                    onChange={(e) =>
                        setMessage(e.target.value)
                    }
                />

                <button
                    className="predict-btn"
                    onClick={predictMessage}
                >
                    Predict
                </button>

                {prediction && (
                    <div className="prediction-result">
                        Prediction : {prediction}
                    </div>
                )}

            </div>

        </div>
    );
}

export default Home;