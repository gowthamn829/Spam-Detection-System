from datetime import datetime
import os

from database_service import database_service


class TrainingHistoryService:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            cls._instance.connection = database_service.get_connection()

            return cls._instance

    def save_history(
        self,
        csv_path,
        onnx_path,
        training_type
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO training_history
            (
                csv_path,
                onnx_path,
                training_type,
                trained_at
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                csv_path,
                onnx_path,
                training_type,
                datetime.now()
            )
        )

        self.connection.commit()

        cursor.close()
    
    def get_all_history(self):

        cursor = self.connection.cursor()
    
        cursor.execute(
            """
            SELECT
                id,
                csv_path,
                onnx_path,
                training_type,
                trained_at
            FROM training_history
            ORDER BY id DESC
            """
        )
    
        rows = cursor.fetchall()
    
        cursor.close()
    
        history = []
    
        for row in rows:
    
            history.append(
                {
                    "id": row[0],
                    "csv_file": os.path.basename(row[1]),
                    "onnx_file": os.path.basename(row[2]),
                    "training_type": row[3],
                    "trained_at": str(row[4])
                }
            )

        return history


history_service = TrainingHistoryService()