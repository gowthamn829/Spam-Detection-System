package com.spamclassifier;

import java.util.Collections;

import ai.onnxruntime.OnnxTensor;
import ai.onnxruntime.OrtEnvironment;
import ai.onnxruntime.OrtSession;

public class ModelService {

    private static OrtEnvironment env;
    private static OrtSession session;

    static {

        try {

            env = OrtEnvironment.getEnvironment();

            session = env.createSession(
                    "/Users/pandu/Downloads/spam_model.onnx",
                    new OrtSession.SessionOptions());

            System.out.println("MODEL LOADED SUCCESSFULLY");

        } catch (Exception e) {

            e.printStackTrace();

            throw new RuntimeException(
                    "Failed to load ONNX model", e);
        }
    }

    public static String predict(String text) throws Exception {

        String[][] inputData = { { text } };

        OnnxTensor inputTensor =
                OnnxTensor.createTensor(env, inputData);

        OrtSession.Result result =
                session.run(
                        Collections.singletonMap(
                                "input",
                                inputTensor));

        String[] labels =
                (String[]) result.get("output_label")
                                 .get()
                                 .getValue();

        return labels[0].toUpperCase();
    }

    public static void reloadModel() throws Exception {

        if (session != null) {
            session.close();
        }

        session = env.createSession(
                "/Users/pandu/Downloads/spam_model.onnx",
                new OrtSession.SessionOptions());

        System.out.println("MODEL RELOADED");
    }
}