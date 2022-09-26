class FileCsv < FileType

  def build_source_filepath(id)
    File.join(@options["collection_dir"], "source", "html", "#{id}.html")
  end

  def transform_es
    # Calling `super` here uses Datura's FileType.transform_es rather
    # than its FileCsv.transform_es, so copying latter's code for now
    puts "transforming #{self.filename}"
    es_doc = []
    table = table_type
    @csv.each do |row|
        if !row.header_row? # && (row["Case ID"] || row["unique_id"])
          new_row = row_to_es(@csv.headers, row, table)
          es_doc << new_row
        end
    end
    if @options["output"]
        filepath = "#{@out_es}/#{self.filename(false)}.json"
        File.open(filepath, "w") { |f| f.write(pretty_json(es_doc)) }
    end
    es_doc
  end

  def row_to_es(headers, row, table)
    if table == "contemporary_poets"
      doc = {}

      # See data repo readme file for description of use of fields

      id = row["ID"]
      doc["identifier"]  = id

      doc["collection"]  = @options["collection"]
      doc["category"]    = "Person"
      doc["subcategory"] = "Contemporary Poet"
      doc["data_type"]   = "csv"

      authorname = [ row["Last Name"], row["Given Name"] ].compact.join(", ")
      titlename = "#{row["Given Name"]} #{row["Last Name"]}"

      # Will potentially need to add more code to deal with more genders later
      gender = 
        case
        when row["Gender"] == "F" 
          "Female"
        when row["Gender"] == "M"
          "Male"
        else
          "Unknown"
        end

      doc["person"]      = {"name" => authorname, "id" => row["Authority"], "role" => gender}
      doc["title"]       = authorname
      doc["title_sort"]  = authorname.downcase # need more sorting rules?
      doc["alternative"] = titlename
      doc["places"]      = row["Country"]
      doc["keywords"]    = row["Region"]
      doc["source"]      = row["Source"]
      
      unless row["Alternate Name"].to_s.strip.empty?
        doc["people"]    = row["Alternate Name"]
      end

      # Featured authors have more information
      if row["Featured"] == "Y"
        doc["type"]      = "Featured"
        # if this is a featured author, then
        #   grab their HTML file and populate the text search
        #   add uri_html pointing at that location
        html_in = build_source_filepath(id)
        if File.file?(html_in)
          # gets the text of the html
          html_file_contents = File.read(html_in)
          html = Nokogiri::HTML(html_file_contents).remove_namespaces!
          html_text = html.xpath("/html").text()

          # adds reference
          output_path = File.join(@options["data_base"], "data", @options["collection"], "output", @options["environment"], "html", "#{id}.html")
          doc["uri_html"] = output_path
        else
          raise "did not find HTML for featured author: #{id}"
        end
      end

      if row["Bibliography"]
        doc["works"]       = row["Bibliography"].split("\n")
      end

      textcomplete =  [ doc["title"], 
                        authorname, 
                        doc["places"], 
                        doc["keywords"],
                        gender
                      ] 

      doc["text"] = textcomplete.join(" ")
      doc["text"] += " #{html_text}" if html_text

      doc
    elsif table == "commentaries"
      CsvToEsCommentaries.new(row, options, @csv, self.filename(false)).json
    elsif table == "events"
      CsvToEsEvents.new(row, options, @csv, self.filename(false)).json
    elsif table == "news_items"
      CsvToEsNews.new(row, options, @csv, self.filename(false)).json
    elsif table == "works"
      CsvToEsWorks.new(row, options, @csv, self.filename(false)).json
    end
  end

  def transform_html
    @csv.each do |row|
      next if row.header_row?
      # copy featured poet HTML files
      if row["Featured"] == "Y"
        id = row["ID"]
        html_in = build_source_filepath(id)
        if File.file?(html_in)
          puts "copying #{id} to html output"
          html_out = File.join(@options["collection_dir"], "output", @options["environment"], "html", "#{id}.html")
          FileUtils.cp(html_in, html_out)
        end
      end
    end
    {}
  end
  def table_type
    case self.filename
    when "African_Poetics_Contemporary_Poet_DB - Master List.csv"
      "contemporary_poets"
    when "commentaries.csv"
      "commentaries"
    when "events.csv"
      "events"
    when "news items.csv"
      "news_items"
    when "works.csv"
      "works"
    end
    
  end
end
