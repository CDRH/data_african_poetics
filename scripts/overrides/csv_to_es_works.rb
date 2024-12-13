class CsvToEsWorks < CsvToEs

  def assemble_collection_specific
    @json["page_k"] = get_value("Page no")
    @json["issue_k"] = get_value("Issue")
    @json["volume_k"] = get_value("Volume")
  end

  def id
    get_id
  end

  def category
    "Works"
  end

  def get_id
    id = @row["Unique ID"] ? @row["Unique ID"] : "blank"
    id = id.split(" ")[0]
    id
  end

  def title
    get_value("Primary Field")
  end

  def alternative
    get_value("Title")
  end

  def type
    if get_value("Work type")
      get_value("Work type").split("|")
    end
  end

  def date(before=false)
    if @row["Year"]
      Datura::Helpers.date_standardize(@row["Year"], before)
    end
  end

  def date_display
    get_value("Year")
  end

  def citation
    {
      "publisher" => get_value("publisher", true)
    }
  end

  def spatial
    if get_value("spatial.country")
      location = { 
        "country" => JSON.parse(get_value("spatial.country"))[0] 
      }
      if get_value("spatial.city")
        location["city"] = JSON.parse(get_value("spatial.city"))
      end
      if get_value("spatial.region")
        location["region"] = JSON.parse(get_value("spatial.region"))
      end
      location
    end
  end

  def rights_uri
    if get_value("Source link")
      get_value("Source link")
    end
  end

  def medium
    if get_value("news_items")
      get_value("news_items").split(";;;")
    end
  end

  def person
    result = []
    people = get_value("person")
    if people && people.length > 0
      people = people.split(";;;")
      people.each do |person|
        data = person.split("|")
        if data && data[0]
          # markdown parsing
          name = parse_md_brackets(data[0])
          # removing the itn id which is now not used in the Rails site, it was included for Omeka
          id = parse_md_parentheses(data[0]).gsub('.itn','')
          # remove stray quotes
          role = data[1] ? data[1].gsub('"', '') : nil
          result << { "name" => name, "role" => role, "id" => id }
        end
      end
    end
    result
  end

  def contributor
    names = get_value("name-major-name", true)
    if names
      names.collect{ |name| { "name" => name }}
    end
  end

  def creator
    names = get_value("person-author", true)
    if names
      names.collect{ |name| { "name" => name }}
    end
  end

  def topics
    get_value("topics-decade")
  end

  def has_relation
    {
      "title" => get_value("commentaries_relation", true)
    }
  end

end
