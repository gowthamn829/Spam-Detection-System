import { useEffect, useState } from "react";
function Evaluation() {

    const [report, setReport] =
        useState(null);

    useEffect(() => {

        fetchEvaluation();

    }, []);

    const fetchEvaluation =
        async () => {

        const response =
            await fetch(
                "http://127.0.0.1:8000/evaluation"
            );

        const data =
            await response.json();

        setReport(data);
    };

    if (!report) {

        return <p>Loading...</p>;
    }

    return (
        <div className="evaluation-page">
        <h2>Classification Report</h2>

     <table className="report-table">
    <thead>
        <tr>
            <th>Class</th>
            <th>Precision</th>
            <th>Recall</th>
            <th>F1 Score</th>
            <th>Support</th>
        </tr>
    </thead>
     
    <tbody>
        <tr>
            <td>HAM</td>
            <td>{report.ham.precision.toFixed(4)}</td>
            <td>{report.ham.recall.toFixed(4)}</td>
            <td>{report.ham["f1-score"].toFixed(4)}</td>
            <td>{report.ham.support}</td>
        </tr>

        <tr>
            <td>SPAM</td>
            <td>{report.spam.precision.toFixed(4)}</td>
            <td>{report.spam.recall.toFixed(4)}</td>
            <td>{report.spam["f1-score"].toFixed(4)}</td>
            <td>{report.spam.support}</td>
        </tr>
    </tbody>
</table>
    
     
    <div className="confusion-section">

            <h2>Confusion Matrix</h2>

            <table className="confusion-table">

                <thead>
                    <tr>
                        <th></th>
                        <th>Pred HAM</th>
                        <th>Pred SPAM</th>
                    </tr>
                </thead>

                <tbody>
                    <tr>
                        <th>Actual HAM</th>
                        <td>{report.confusion_matrix.matrix[0][0]}</td>
                        <td>{report.confusion_matrix.matrix[0][1]}</td>
                    </tr>

                    <tr>
                        <th>Actual SPAM</th>
                        <td>{report.confusion_matrix.matrix[1][0]}</td>
                        <td>{report.confusion_matrix.matrix[1][1]}</td>
                    </tr>
                </tbody>

            </table>

    </div>

</div>
    );
}

export default Evaluation;