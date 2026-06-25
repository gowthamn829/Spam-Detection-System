package com.spamclassifier;

import java.io.BufferedReader;
import java.io.IOException;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
public class PredictionServlet extends HttpServlet {
	private static final Logger logger =
	        LogManager.getLogger(PredictionServlet.class);

	protected void doPost(HttpServletRequest request,
	                      HttpServletResponse response)
	        throws ServletException, IOException {

		response.setHeader(
		        "Access-Control-Allow-Origin",
		        "http://localhost:5173"
		    );

		    response.setHeader(
		        "Access-Control-Allow-Methods",
		        "POST, GET, OPTIONS"
		    );

		    response.setHeader(
		        "Access-Control-Allow-Headers",
		        "Content-Type"
		    );
		    
	    logger.info("REQUEST RECEIVED");
	    BufferedReader reader = request.getReader();

	    StringBuilder message = new StringBuilder();
	    String line;

	    while ((line = reader.readLine()) != null) {
	        message.append(line);
	    }

	    try {

	        logger.info("Request received");

	        String prediction =
	                ModelService.predict(message.toString());

	        logger.info("Prediction: " + prediction);

	        response.setContentType("application/json");

	        response.getWriter().write(
	                "{\"prediction\":\"" +
	                prediction +
	                "\"}");

	    } catch (Exception e) {

	        logger.error("Prediction failed", e);
	        throw new ServletException(e);
	    }
	}
}