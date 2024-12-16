package com.gale.content.services;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.LineIterator;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.gale.content.services.util.JsonReader;

public class MetaDataExtractor {
	
	JsonReader reader = new JsonReader();
	final String METADATA_COLUMN_HEADERS = "document title^author^document type^content type^publication title^publication date^link^start page^citation^description\n";
	final String OUTPUT_COLUMNS = "%s^%s^%s^%s^%s^%s^%s^%s^%s^%s\n";
	
	public static void main(final String args) throws JSONException, IOException, URISyntaxException {
		run("ids.txt", "metadata.txt");
	}
	
	public static void run(final String inputFileName, final String outputFileName) throws JSONException, IOException, URISyntaxException {
		MetaDataExtractor extractor = new MetaDataExtractor();
		saveFile(extractor.fetchMetaData(inputFileName), outputFileName);
	}
	
	public String fetchMetaData(final String fileWithIds) throws JSONException, IOException, URISyntaxException {
		String metadata = METADATA_COLUMN_HEADERS;
		String apiKey = fetchApiKey();
		
		for (String docId : readDocumentIdsFromFile(fileWithIds)) {
			JSONObject resultsJson = reader.readJsonFromUrl(String.format("https://api.gale.com/api/v1/item/GALE|%s?api_key=%s", docId, apiKey));
			JSONObject docJson = resultsJson.getJSONObject("doc");
			String title = docJson.optString("title");
			String description = docJson.optString("description");
			String contentType = docJson.optString("contentType");
			JSONArray documentTypes = docJson.getJSONArray("documentTypes");
			String documentType = documentTypes.join("|");
			JSONObject publicationJson = docJson.getJSONObject("publication");
			String publicationTitle = publicationJson.optString("title");
			String publicationDate = publicationJson.optString("date");
			String startPage = docJson.optString("startPage");
			String author = docJson.optString("author");
			String link = docJson.optString("isShownAt");
			String citation = docJson.optString("citation");
			
			metadata += String.format(OUTPUT_COLUMNS, title, author, documentType, contentType, publicationTitle, publicationDate, link, startPage, citation, description);
			System.out.println("Document: " + docId + " processed.");
		}
		return metadata;
	}
	
	private List<String> readDocumentIdsFromFile(final String fileName) throws IOException, URISyntaxException {
		List<String> ids = new ArrayList<String>();
		LineIterator it = FileUtils.lineIterator(getFileFromResource(fileName), "UTF-8");
		try {
		    while (it.hasNext()) {
		    String id = it.nextLine();
		    		ids.add(id);
		    }
		} finally {
		    it.close();
		}
		return ids;
	}
	
	private File getFileFromResource(final String fileName) throws URISyntaxException{
        ClassLoader classLoader = getClass().getClassLoader();
        URL resource = classLoader.getResource(fileName);
        if (resource == null) {
            throw new IllegalArgumentException("file not found! " + fileName);
        } else {
        		return new File(resource.toURI());
        }
    }
	
	private static void saveFile(final String metadataCsv, final String fileName) {
		try {
			FileWriter myWriter = new FileWriter(fileName);
			myWriter.write(metadataCsv);
			myWriter.close();
			System.out.println("Successfully wrote to the file.");
		} catch (IOException e) {
			System.out.println("An error occurred.");
			e.printStackTrace();
		}
	}

	private String fetchApiKey() throws IOException {
		JSONObject apiKeyJson = reader.readJsonFromUrl("https://api.gale.com/api/tools/generate_key?user");
		String apiKey = apiKeyJson.getString("apiKey");
		return apiKey;
	}
}