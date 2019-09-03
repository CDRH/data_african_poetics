class FileCsv < FileType

  def row_to_es(headers, row)
    doc = {}

    doc["collection"]  = @options["collection"]
    doc["category"]    = "Person"
    doc["subcategory"] = "Contemporary Poet"
    doc["data_type"]   = "csv"

    authorname = row["Name"]

    doc["identifier"]  = row["ID"]
    doc["person"]      = {"name" => authorname, "id" => row["Authority"], "role" => row["Gender"]}
    doc["title"]       = authorname
    doc["title_sort"]  = authorname.downcase # need more sorting rules?
    doc["places"]      = row["Country"]
    doc["keywords"]    = row["Region"]
    doc["source"]      = row["Source"]
    doc["works"]       = row["Bibliography"]

    # add field for text with text from other fields

    if doc.key?("text") && doc.key?("title")
      doc["text"] << " #{doc["title"]}"
    end
    doc
  end
end
