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
          if new_row
            es_doc << new_row
          end
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
      if row["Country"] == "Congo, Democratic Republic Of"
        doc["places"] = ["Congo, Democratic Republic Of"]
      else
        doc["places"]    = row["Country"].split(", ") if row["Country"]
      end
      doc["keywords"]    = row["Region"]
      doc["source"]      = row["Source"]

      # adding new fields from expanded spreadsheet as is for now
      #ID - previously done
      #Last Name - previously done
      #Given Name - previously done
      #Alternate Name - previously done
      #Née - skip for now
      #Featured - done, but may need to revisit
      #person_nationality_k - done
      #Country - previously done
      #Region - previously done
      #Gender - previously done
      #person_birth_date_k
      #spatial_name_birth_k
      #person_death_date_k
      #spatial_name_death_k
      #person_trait1_k
      #citation_title_k
      #Selected Works Year Published - skip for now
      #citation_publisher
      #citation_place_k
      #language
      #citation_role_k
      #Authority - previously done
      #description
      #contributor.name
      #Notes - skip for now
      #Bio Sources (MLA)
      #Contact
      #Status
      doc["person_nationality_k"]      = row["person_nationality_k"]
      doc["person_birth_date_k"]      = row["person_birth_date_k"]
      doc["patial_name_birth_k"]      = row["patial_name_birth_k"]
      doc["person_death_date_k"]      = row["person_death_date_k"]
      doc["spatial_name_death_k"]      = row["spatial_name_death_k"]
      doc["person_trait1_k"]      = row["person_trait1_k"]
      doc["citation_title_k"]      = row["citation_title_k"]
      doc["citation_publisher"]      = row["citation_publisher"]
      doc["citation_place_k"]      = row["citation_place_k"]
      doc["language"]      = row["language"]
      doc["citation_role_k"]      = row["citation_role_k"]
      doc["description"]      = row["description"]
      doc["contributor_name_k"]      = row["contributor.name"]
      
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
    elsif table == "people"
      if row["Major african poet"] == "True"
        CsvToEsPeople.new(row, options, @csv, self.filename(false)).json
      end
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
    when "contemporary_poets.csv"
      "contemporary_poets"
    when "commentaries.csv"
      "commentaries"
    when "events.csv"
      "events"
    when "news items.csv"
      "news_items"
    when "works.csv"
      "works"
    when "people.csv"
      "people"
    end
  end
end
