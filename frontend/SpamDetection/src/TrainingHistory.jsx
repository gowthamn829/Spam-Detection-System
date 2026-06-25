import { useEffect, useState } from "react";

function TrainingHistory({ refresh }) {
    const [history, setHistory] =useState([]);

    useEffect(() => {
        fetchHistory();
    }, [refresh]);

    const fetchHistory =
        async () => {

        const response =
            await fetch(
                "http://127.0.0.1:8000/training-history"
            );

        const data =
            await response.json();

        setHistory(data);
    };

    return (

        <>
            <h2>
                Training History
            </h2>

            <table border="1">
            <thead>
                <tr >
                    <th>ID</th>
                    <th>CSV File</th>
                    <th>ONNX File</th>
                    <th>Type</th>
                    <th>Trained At</th>
                </tr>
             </thead>

        <tbody>
            {history.map(item => (
                <tr key={item.id}>
                    <td>{item.id}</td>
                    <td>{item.csv_file}</td>
                    <td>{item.onnx_file}</td>
                    <td>{item.training_type}</td>
                    <td>{item.trained_at}</td>
                </tr>
            ))}
        </tbody>
            </table>
            
        </>
    );
}

export default TrainingHistory;