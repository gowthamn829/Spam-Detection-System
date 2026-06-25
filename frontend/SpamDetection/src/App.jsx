import { useState } from "react";
import UploadForm from "./UploadForm";
import TrainingHistory from "./TrainingHistory";
import Evaluation from "./Evaluation";
import logo from "./assets/logo.png";
import Home from "./Home";
import {
  FaHome,
  FaUpload,
  FaHistory,
  FaChartLine
} from "react-icons/fa";

function App() {
  const [page, setPage] = useState("home");
  const [refresh, setRefresh] = useState(0);
  return (
        <div className="app">

            <div className="sidebar">

                <img
                    src={logo}
                    alt="Spam Detector"
                    className="logo"
                />

                <h2>Spam Detector</h2>
                <button
                    className={page === "home" ? "active" : ""}
                    onClick={() => setPage("home")}
                  >
                    <FaHome />
                    Home
                  </button>

                  <button
                      className={page === "upload" ? "active" : ""}
                      onClick={() => setPage("upload")}
                  >
                      <FaUpload />
                      Submissions
                  </button>

                  <button
                      className={page === "history" ? "active" : ""}
                      onClick={() => setPage("history")}
                  >
                      <FaHistory />
                      History
                  </button>

                  <button
                      className={page === "evaluation" ? "active" : ""}
                      onClick={() => setPage("evaluation")}
                  >
                      <FaChartLine />
                      Insights
                  </button>

            </div>

            <div className="content">
            
                {page === "home" && <Home />}
                {page === "upload" && (
                    <UploadForm
                        setRefresh={setRefresh}
                    />
                )}

                {page === "history" && (
                    <TrainingHistory
                        refresh={refresh}
                    />
                )}

                {page === "evaluation" && (
                    <Evaluation />
                )}

            </div>

        </div>
    );
}

export default App;