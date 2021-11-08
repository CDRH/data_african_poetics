package com.gale.content.services.util;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.Map;
import java.util.Map.Entry;

import org.apache.commons.io.IOUtils;
import org.json.JSONException;
import org.json.JSONObject;

public class JsonReader {
	
	public JSONObject readJsonFromUrl(final String serviceRequestUrl) throws IOException, JSONException {
		return readJsonFromUrl(serviceRequestUrl, null);
	}
	
	public JSONObject readJsonFromUrlPost(final String serviceRequestUrl, final JSONObject postData) throws IOException, JSONException {

		HttpURLConnection connection = connectTo(serviceRequestUrl);
		
		try {
			connection.setDoOutput(true);
			connection.setDoInput(true);
			
			connection.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
			connection.setRequestProperty("Accept", "application/json");
			connection.setRequestMethod("POST");
			
			OutputStreamWriter wr = new OutputStreamWriter(connection.getOutputStream());
			String string = postData.toString();
			wr.write(string);
			wr.flush();

			if (connection.getResponseCode() != 200) {
				return new JSONObject("{}");
			}

			BufferedReader reader = getReader(connection);
			String jsonText = wrapInvalidJson(readAll(reader));
			
			return new JSONObject(jsonText);

		} finally {
			connection.disconnect();
		}
	}

	public JSONObject readJsonFromUrl(final String serviceRequestUrl, final Map<String, String> apiKeyHeader) throws IOException, JSONException {
		HttpURLConnection connection = connectTo(serviceRequestUrl);

		try {
			connection.setRequestMethod("GET");
			connection.setRequestProperty("Accept", "application/json");
			
			if(null != apiKeyHeader) {
				for (Entry<String, String> header : apiKeyHeader.entrySet()) {
					connection.setRequestProperty(header.getKey(), header.getValue());
				}
			}

			if (connection.getResponseCode() != 200) {
				return new JSONObject("{}");
			}

			BufferedReader reader = getReader(connection);
			String jsonText = wrapInvalidJson(readAll(reader));
			
			return new JSONObject(jsonText);

		} finally {
			connection.disconnect();
		}
	}

	private String wrapInvalidJson(String jsonText) {
		if(!jsonText.startsWith("{")) {
			jsonText = "{ items: " + jsonText + "}"; 
		}
		return jsonText;
	}
	
	public JSONObject readJsonFromFile(final String fileName) {
		ClassLoader classLoader = getClass().getClassLoader();
		JSONObject jsonObject = null;
		try {
			String json = IOUtils.toString(classLoader.getResourceAsStream(fileName));
			jsonObject = new JSONObject(json);
		} catch (IOException e) {
			e.printStackTrace();
		}

		return jsonObject;
	}

	protected BufferedReader getReader(final HttpURLConnection connection) throws IOException {
		return new BufferedReader(new InputStreamReader((connection.getInputStream())));
	}

	protected HttpURLConnection connectTo(final String serviceRequestUrl) throws MalformedURLException, IOException {
		return (HttpURLConnection) new URL(serviceRequestUrl).openConnection();
	}

	private String readAll(final Reader reader) throws IOException {
		StringBuilder stringBuilder = new StringBuilder();
		int cp;
		while ((cp = reader.read()) != -1) {
			stringBuilder.append((char) cp);
		}
		return stringBuilder.toString();
	}
}