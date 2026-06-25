from fastapi import FastAPI, UploadFile
from fastapi import HTTPException
import pandas as pd
import requests
import logging
from datetime import datetime
import os
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from TrainingHistoryService import history_service
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import StringTensorType
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATASET_PATH = "/Users/pandu/Downloads/dataset.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)

logger = logging.getLogger("TrainingServer")

def load_and_validate_csv(file):

    logger.info("Reading uploaded CSV")

    df = pd.read_csv(
        file.file,
        encoding="latin-1"
    )

    required_columns = ["v1", "v2"]

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:

        logger.error(
            f"Missing columns: {missing_columns}"
        )

        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    if df.empty:

        logger.error(
            "CSV is empty"
        )

        raise ValueError(
            "CSV is empty"
        )

    logger.info(
        f"CSV validation successful. Rows: {len(df)}"
    )

    return df


@app.get("/training-history")
def get_training_history():

    return history_service.get_all_history()

@app.get("/")
def home():

    logger.info( "Home endpoint called")

    return {"message": "Training Server Running"}

@app.get("/evaluation")
def get_evaluation():

    with open(
        "evaluation/classification_report.json"
    ) as f:

        report = json.load(f)

    with open(
        "evaluation/confusion_matrix.json"
    ) as f:

        matrix = json.load(f)

    report["confusion_matrix"] = matrix

    return report

@app.post("/train")
def train(
    file: UploadFile,
    type: str = "separate"
):
    try:

        logger.info(
            "Training request received"
        )

        logger.info(
            f"File received: {file.filename}"
        )

        os.makedirs("uploads", exist_ok=True)
        os.makedirs("backup", exist_ok=True)

        csv_path = os.path.abspath(
            os.path.join("uploads", file.filename)
        )

        file.file.seek(0)

        with open(csv_path, "wb") as f:
            f.write(file.file.read())

        file.file.seek(0)

        model_name = (
            f"spam_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.onnx"
        )
        os.makedirs(
                "models",
                exist_ok=True
            )

        onnx_path = os.path.abspath(
            os.path.join(
                "models",
                model_name
            )
        )

        logger.info(
            f"Training type: {type}"
        )

        try:

            uploaded_df = load_and_validate_csv(file)

        except ValueError as e:

            raise HTTPException(
                status_code=400,
                detail=str(e)
            )

        BACKUP_DATASET_PATH = os.path.abspath(
            "backup/dataset_backup.csv"
        )

        # --------------------
        # MERGE / SEPARATE
        # --------------------

        if type.lower() == "merge":

            logger.info(
                "Merge mode selected"
            )

            try:

                existing_df = pd.read_csv(
                    DATASET_PATH,
                    encoding="latin-1"
                )

                existing_df.to_csv(
                    BACKUP_DATASET_PATH,
                    index=False
                )

                logger.info(
                    "Current dataset backed up"
                )

                df = pd.concat(
                    [
                        existing_df,
                        uploaded_df
                    ],
                    ignore_index=True
                )

                df = df.drop_duplicates()

                logger.info(
                    f"Merged rows: {len(df)}"
                )

                df.to_csv(
                    DATASET_PATH,
                    index=False
                )

                logger.info(
                    "Merged dataset saved"
                )

            except FileNotFoundError:

                logger.info(
                    "No existing dataset found. Using uploaded dataset."
                )

                df = uploaded_df

                df.to_csv(
                    DATASET_PATH,
                    index=False
                )

        elif type.lower() == "separate":

            logger.info(
                "Separate mode selected"
            )

            try:

                existing_df = pd.read_csv(
                    DATASET_PATH,
                    encoding="latin-1"
                )

                existing_df.to_csv(
                    BACKUP_DATASET_PATH,
                    index=False
                )

                logger.info(
                    "Current dataset backed up"
                )

            except FileNotFoundError:

                logger.info(
                    "No existing dataset found"
                )

            uploaded_df.to_csv(
                DATASET_PATH,
                index=False
            )

            logger.info(
                "Current dataset replaced"
            )

            df = uploaded_df

        else:

            raise HTTPException(
                status_code=400,
                detail="type must be merge or separate"
            )

        # --------------------
        # TRAIN MODEL
        # --------------------

        X = df["v2"]
        y = df["v1"]

        logger.info(
            "Building pipeline"
        )

        pipeline = Pipeline([
            (
                "tfidf",
                TfidfVectorizer(
                    stop_words="english",
                    ngram_range=(1, 2)
                )
            ),
            (
                "clf",
                MultinomialNB()
            )
        ])

        logger.info(
            "Starting model training"
        )

        pipeline.fit(X, y)

        logger.info(
            "Model training completed"
                )
        # --------------------
        # MODEL EVALUATION
        # --------------------
        
        os.makedirs(
            "evaluation",
            exist_ok=True
        )
        
        test_csv_path = os.path.abspath(
            "evaluation/testing.csv"
        )
        
        logger.info(
            f"Loading test dataset: {test_csv_path}"
        )
        
        test_df = pd.read_csv(
            test_csv_path,
            encoding="latin-1"
        )
        
        required_columns = ["v1", "v2"]
        
        missing_columns = [
            col
            for col in required_columns
            if col not in test_df.columns
        ]
        
        if missing_columns:
        
            raise HTTPException(
                status_code=500,
                detail=f"Testing CSV missing columns: {missing_columns}"
            )
        
        X_test = test_df["v2"]
        y_test = test_df["v1"]
        
        logger.info(
            f"Testing rows: {len(test_df)}"
        )
        
        y_pred = pipeline.predict(
            X_test
        )
        
        logger.info(
            "Predictions completed"
        )
        
        # --------------------
        # CLASSIFICATION REPORT
        # --------------------
        
        report = classification_report(
            y_test,
            y_pred,
            output_dict=True
        )
        
        report_path = os.path.abspath(
            "evaluation/classification_report.json"
        )
        
        with open(
            report_path,
            "w"
        ) as f:
        
            json.dump(
                report,
                f,
                indent=4
            )
        
        logger.info(
            f"Classification report saved: {report_path}"
        )
        
        # --------------------
        # CONFUSION MATRIX
        # --------------------
        
        cm = confusion_matrix(
            y_test,
            y_pred
        )
        
        confusion_data = {
            "labels": pipeline.classes_.tolist(),
            "matrix": cm.tolist()
        }
        
        confusion_path = os.path.abspath(
            "evaluation/confusion_matrix.json"
        )
        
        with open(
            confusion_path,
            "w"
        ) as f:
        
            json.dump(
                confusion_data,
                f,
                indent=4
            )
        
        logger.info(
            f"Confusion matrix saved: {confusion_path}"
        )

        # --------------------
        # CONVERT TO ONNX
        # --------------------

        initial_type = [
            (
                "input",
                StringTensorType(
                    [None, 1]
                )
            )
        ]

        logger.info(
            "Converting model to ONNX"
        )

        onnx_model = convert_sklearn(
            pipeline,
            initial_types=initial_type,
            target_opset=21
        )

        logger.info(
            "ONNX conversion completed"
        )

        # --------------------
        # SAVE ONNX
        # --------------------

        with open(onnx_path, "wb") as f:

            f.write(
                onnx_model.SerializeToString()
            )

        logger.info(
            "ONNX file saved"
        )

        # --------------------
        # SEND TO JAVA SERVER
        # --------------------

        logger.info(
            "Uploading ONNX model to Java server"
        )

        with open(onnx_path, "rb") as model_file:

            files = {
                "model": (
                    model_name,
                    model_file,
                    "application/octet-stream"
                )
            }

            response = requests.post(
                "http://localhost:8080/SpamClassifier/upload-model",
                files=files
            )

        logger.info(
            f"Java server response: {response.status_code}"
        )

        if response.status_code != 200:

            raise HTTPException(
                status_code=500,
                detail="Failed to upload model to Java server"
            )

        # --------------------
        # SAVE HISTORY
        # --------------------

        history_service.save_history(
            csv_path=csv_path,
            onnx_path=onnx_path,
            training_type=type
        )

        logger.info(
            "Training history saved successfully"
        )

        return {
            "message": "Model Trained Successfully",
            "training_type": type,
            "classes": pipeline.classes_.tolist(),
            "onnx_file": model_name,
            "csv_file": csv_path
        }

    except HTTPException:
        raise

    except Exception as e:

        logger.exception(
            "Training failed"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )                   