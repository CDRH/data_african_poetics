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

  def date_display
    get_value("Year")
  end

  def publisher
    get_value("publisher", true)
  end

  def spatial
    locations = []
    if get_value("spatial.country")
      JSON.parse(get_value("spatial.country")).each do |country|
        location = { "country" => JSON.parse(get_value("spatial.country")) }
        if get_value("spatial.city")
          location["city"] = JSON.parse(get_value("spatial.city"))
        end
        locations << location
      end
    end
    locations
  end

  def rights_uri
    if get_value("Source link")
      get_value("Source link")
    end
  end

  def topics
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
        if data[0]
          name = /\[(.*)\]/.match(data[0])[1] if /\[(.*)\]/.match(data[0])
          id = /\((.*)\)/.match(data[0])[1] if /\((.*)\)/.match(data[0])
          role = data[1]
          result << { name: name, role: role, id: id }
        end
      end
    end
    result
  end

end