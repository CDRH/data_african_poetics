class FileCsv < FileType

  def row_to_es(headers, row)
    doc = {}

    doc["collection"]  = @options["collection"]
    doc["category"]    = "Person"
    doc["subcategory"] = "Contemporary Poet"
    doc["data_type"]   = "csv"

    authorname = [ row["Last Name"], row["Given Name"] ].compact.join(", ")
    titlename = "#{row["Given Name"]} #{row["Last Name"]}"

    doc["identifier"]  = row["ID"]
    doc["person"]      = {"name" => authorname, "id" => row["Authority"], "role" => row["Gender"]}
    doc["title"]       = titlename
    doc["title_sort"]  = authorname.downcase # need more sorting rules?
    doc["places"]      = row["Country"]
    doc["keywords"]    = row["Region"]
    doc["source"]      = row["Source"]
    if row["Bibliography"]
      doc["works"]       = row["Bibliography"].split("\n")
    end

    # add field for text with text from other fields

    if doc.key?("text") && doc.key?("title")
      doc["text"] << " #{doc["title"]}"
    end
    doc
  end
end
