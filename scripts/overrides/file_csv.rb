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

    gender = 
      case
      when row["Gender"] == "F" 
        "Female"
      when row["Gender"] == "M"
        "Male"
      else
        "Unknown"
      end

    doc["person"]      = {"name" => authorname, "id" => row["ID"], "role" => gender}
    doc["title"]       = authorname
    doc["title_sort"]  = authorname.downcase # need more sorting rules?
    doc["alternative"] = titlename
    doc["places"]      = row["Country"]
    doc["keywords"]    = row["Region"]
    doc["source"]      = row["Source"]
    
    unless row["Alternate Name"].to_s.strip.empty?
      doc["people"]    = row["Alternate Name"]
    end

    if row["Featured"] == "Y"
      doc["type"]      = "Featured"
    end

    if row["Bibliography"]
      doc["works"]       = row["Bibliography"].split("\n")
    end

    textcomplete =  [ doc["title"], 
                      authorname, 
                      doc["places"], 
                      doc["keywords"],
                      gender, 
                      row["Text"]
                    ] 

    doc["text"] = textcomplete.join(" ")

    doc
  end
end
