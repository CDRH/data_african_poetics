class CsvToEsNews < CsvToEs

  def assemble_collection_specific
    @json["page_k"] = get_value("Source page no")
    @json["identifier_original_k"] = get_value("Gale ID")
    if @row["has_part_image"]
      @json["has_part_image_k"] = @row["has_part_image"].split("; ").map { |filename|
        File.join(
          @options["data_base"],
          "data",
          @options["collection"],
          "source/images/gale",
          "#{filename}"
        )
      }.join("; ")
    end
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

  def type
    get_value("Document type")
  end

  # NOT CURRENTLY USED
  # def type
  #   get_value("Content type")
  # end

  def date(before=false)
    Datura::Helpers.date_standardize(@row["Article Date (formatted)"], before)
  end

  def publisher
    get_value("publisher", true)
  end

  def rights_uri
    get_value("Source link")
  end

  def rights_holder
    get_value("rights_holder", true)
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
    get_value("topics-decade")
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
          # markdown parsing
          name = /\[(.*)\]/.match(data[0])[1] if /\[(.*)\]/.match(data[0])
          id = /\((.*)\)/.match(data[0])[1] if /\((.*)\)/.match(data[0])
          role = data[1]
          result << { name: name, role: role, id: id }
        end
      end
    end
    result
  end

  def date_not_after
    if @row["Source access date"]
      Datura::Helpers.date_standardize(@row["Source access date"], false)
    end
  end

  def contributor
    names = get_value("contributor.name", true)
    if names
      names.collect{ |name| { "name": name }}
    end
  end

  def creator
    names = get_value("creator.name", true)
    if names
      names.collect{ |name| { "name": name }}
    end
  end

  def subjects
    if get_value("subjects")
      get_value("subjects").split(";;;")
    end
  end

  def relation
    get_value("commentaries_relation", true)
  end


end
