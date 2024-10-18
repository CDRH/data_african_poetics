class FileCsv < FileType



  def build_source_filepath(id)
    File.join(@options["collection_dir"], "source", "html", "#{id}.html")
  end

  # override to change encoding
  def read_csv(file_location, encoding="utf-8")
    CSV.read(file_location, **{
      encoding: encoding,
      headers: true,
      return_headers: true
    })
  end

  def transform_es
    # Calling `super` here uses Datura's FileType.transform_es rather
    # than its FileCsv.transform_es, so copying latter's code for now
    puts "transforming #{self.filename}"
    es_doc = []
    table = table_type
    @csv.each do |row|
        if !row.header_row? 
          begin
            new_row = row_to_es(@csv.headers, row, table)
          rescue => e
            puts "error for item " + row["Unique ID"]
            puts e.full_message
          end
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
    if table == "people" \
      && row["Completion Status"] == "Publish" \
      && row["Manual data entry complete"] == "True" \
      && JSON.parse(row["site section"]).include?("Index of Poets")
        doc = {}
        # See data repo readme file for description of use of fields
        doc["identifier"]  = row["Unique ID"]

        titlename = "#{row["Name given"]} #{row["Name last"]}"
        
        doc["title"]       = row["Name Built"]
        doc["title_sort"]  = row["Name Built"].downcase # need more sorting rules?
        doc["person_alternate_name_k"] = titlename
        doc["collection"]  = @options["collection"]
        doc["category"]    = "People"
        #may also be "In the News"
        doc["subcategory"] = get_value(row, "site section", true)
        doc["data_type"]   = "csv"
        #initializing the spatial field to put some location-oriented data into later
        doc["spatial"] = {}



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
        doc["person_gender_k"] = gender
        doc["places"]      = get_value(row, "nationality-country", true)
        doc["source"]      = row["Bio Sources (MLA)"]
        doc["keywords"] = get_value(row, "education", true)
        doc["date"]      = Datura::Helpers.date_standardize(row["Date birth"])
        doc["date_not_before"] = Datura::Helpers.date_standardize(row["Date birth"])
        doc["date_not_after"]      = Datura::Helpers.date_standardize(row["Date death"])
        if row["death_spatial.country"] && row["death_spatial.country"].length > 0
          country = get_value(row, "death_spatial.country", true)[0]
          if row["death_spatial.city"] && row["death_spatial.city"].length > 0
            city = get_value(row, "death_spatial.city", true)[0]
            doc["place_death_k"]      = "#{city}, #{country}"
          else
            doc["place_death_k"]      = country
          end
        end
        doc["language"]      = row["Languages spoken"]
        doc["description"]      = row["Biography"]
        if row["work roles"].length > 1
          doc["works"] = row["work roles"].split(";;;")
        end
        unless row["Name alt"].to_s.strip.empty?
          doc["people"]    = row["Name alt"]
        end
        # Featured authors have more information
        if row["Featured"] == "True"
          doc["type"]      = "Featured"
        end
        doc["alternative"] = row["name-letter"]
        doc["medium"] = get_value(row, "news item roles", true)
        doc["topics"] = row["birth-decade"]
        doc["subjects"] = get_value(row, "events", true)
        people = row["related-people"]
        if people
          people = people.split(";;;") if people
          unique = people.uniq
          result = []
          unique.each do |person|
            name = /\[(.*)\]/.match(person)[1] if /\[(.*)\]/.match(person)
            id = /\]\((.*)\)/.match(person)[1] if /\]\((.*)\)/.match(person)
            count = people.select{|p| p == person}.count
            if name
              result << { "name" => name, "role" => count, "id" => id }
            end
          end
          doc["person"] = result
        end

        places = []
        if row["nationality-region"] && row["nationality-region"].length > 0
          places << { "region" => JSON.parse(row["nationality-region"])[0], "type" => "nationality" }
        end
        if row["birth_spatial.country"] && row["birth_spatial.country"].length > 0
          birthplace = { "country" => JSON.parse(row["birth_spatial.country"])[0], "type" => "birth place" }
          if row["birth_spatial.city"] && row["birth_spatial.city"].length > 0
            birthplace["city"] = JSON.parse(row["birth_spatial.city"])[0]
          end
          places << birthplace
        end
        doc["spatial"] = places
        doc["ethnicity_k"] = get_value(row, "ethnicity.text", true)
        doc["country_residence_k"] = get_value(row, "country_residence.text", true)
        doc["poems_k"] = row["Poems"]
        doc["poetry_collections_k"] = row["Poetry Collections"]
        doc["speeches_k"] = row["speeches lectures"]
        textcomplete =  [ doc["title"], 
                          doc["places"], 
                          doc["keywords"],
                          gender
                        ] 

        doc["text"] = textcomplete.join(" ")
        doc
    elsif table == "commentaries"
      CsvToEsCommentaries.new(row, options, @csv, self.filename(false)).json
    elsif table == "events"
      CsvToEsEvents.new(row, options, @csv, self.filename(false)).json
    elsif table == "news_items"
      if row["Completion Status"] == "Publish"
        CsvToEsNews.new(row, options, @csv, self.filename(false)).json
      end
    elsif table == "works"
      CsvToEsWorks.new(row, options, @csv, self.filename(false)).json
    elsif table == "people" \
      && row["Completion Status"] == "Publish" \
      && row["Manual data entry complete"] == "True" \
      && JSON.parse(row["site section"]).include?("In the News")
      CsvToEsPeople.new(row, options, @csv, self.filename(false)).json
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
    when "contemporary poets.csv"
      "contemporary poets"
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

  def parse_md_parentheses(query)
    /\]\((.*)\)/.match(query)[1] if /\]\((.*)\)/.match(query)
  end

  def get_value(row, name, parse=false)
    #should be true if an array field that should be parsed as JSON, otherwise false
    if row[name] && row[name].length > 0
      if parse
        JSON.parse(row[name])
      else
        row[name]
      end
    end
  end
end
