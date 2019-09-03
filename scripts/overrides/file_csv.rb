class FileCsv < FileType

  def row_to_es(headers, row)
    doc = {}

    doc["collection"] = @options["collection"]
    doc["identifier"] = row["ID"]
    doc["person"]     = {"name" => row["Name"], "id" => row["Authority"], "role" => row["Gender"]}
    doc["places"]     = row["Country"]
    doc["keywords"]   = row["Region"]
    doc["source"]     = row["Source"]
    doc["works"]      = row["Bibliography"]

    # headers.each do |column|
    #   doc[column] = row[column] if row[column] && (column != "creator")
    #   if (column == "creator") 
    #     doc[column] = {"name" => row[column]}
    #   end
    # end
    if doc.key?("text") && doc.key?("title")
      doc["text"] << " #{doc["title"]}"
    end
    doc
  end
end
