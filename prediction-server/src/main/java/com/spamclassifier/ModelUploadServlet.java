package com.spamclassifier;

import java.io.File;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.MultipartConfig;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.Part;

@WebServlet("/upload-model")
@MultipartConfig
public class ModelUploadServlet extends HttpServlet {


    @Override
    protected void doPost(HttpServletRequest request,
                          HttpServletResponse response)
            throws ServletException, java.io.IOException {

        Part filePart = request.getPart("model");

        String modelPath =
                "/Users/pandu/Downloads/spam_model.onnx";

        try (InputStream input =
                     filePart.getInputStream()) {

            Files.copy( 
                    input,
                    new File(modelPath).toPath(),
                    StandardCopyOption.REPLACE_EXISTING
            );
        }

        try {
            ModelService.reloadModel();
        } catch (Exception e) {
            throw new ServletException(e);
        }

        response.getWriter().write(
                "MODEL UPLOADED SUCCESSFULLY"
        );
    }
}