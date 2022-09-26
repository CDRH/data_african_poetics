class CsvToEsNews < CsvToEs

  def assemble_collection_specific
    @json["page_k"] = get_value("Source page no")
    @json["identifier_original_k"] = get_value("Gale ID")
  end

  def id
    get_id
  end

  def category
    "News Items"
  end

  def get_id
    id = @row["unique_id"] ? @row["unique_id"] : "blank"
    id = id.split(" ")[0]
    id
  end

  def title
    get_value("title")
  end

  def alternative
    get_value("Article title")
  end

  def format
    get_value("Document type")
  end

  def type
    get_value("Content type")
  end

  def date(before=false)
    Datura::Helpers.date_standardize(@row["Article Date"], before)
  end

  def source
    get_value("source", true)
  end

  def rights_uri
    get_value("Source link")
  end

  def rights_holder
    get_value("right_holder")
  end

  def description
    get_value("Excerpt")
  end

  def works
    if get_value("works")
      get_value("works").split(";;;")
    end
  end

  def topics
    if get_value("topics")
      get_value("topics").split(";;;")
    end
  end

  def keywords
    get_value("Tags", true)
  end

  def rights
    get_value("Permissions")
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

  def get_value(name, parse=false)
    if @row[name] && @row[name].length > 0
      if parse
        JSON.parse(@row[name])
      else
        @row[name]
      end
    end
  end

  def date_not_after
    if @row["Source access date"]
      Datura::Helpers.date_standardize(@row["Source access date"], false)
    end
  end
end
