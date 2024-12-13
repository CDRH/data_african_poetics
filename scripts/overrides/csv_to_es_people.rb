class CsvToEsPeople < CsvToEs
  def id
    get_id
  end

  def category
    "People"
  end

  def subcategory
    "In the News"
  end

  def get_id
    id = @row["Unique ID"] ? @row["Unique ID"] : "blank"
    id = id.split(" ")[0]
    id
  end

  def title
    get_value("Name Built")
  end

  def date(before=false)
    Datura::Helpers.date_standardize(@row["Date birth"], before)
  end

  def date_not_after
    if @row["Date death"]
      Datura::Helpers.date_standardize(@row["Date death"], false)
    end
  end

  def description
    get_value("Biography")
  end

  def type
    if @row["Major african poet"] == "True"
      "Major African poet"
    end
  end

  def spatial
    places = []
    if get_value("nationality-country", true)
      places << {
        "short_name" => get_value("nationality-country", true),
        "role" => "placename"
      }
    end
    if get_value("nationality-region")
      places << { "region" => JSON.parse(get_value("nationality-region"))[0], "role" => "nationality" }
    end
    if get_value("birth_spatial.country")
      birthplace = { "country" => JSON.parse(get_value("birth_spatial.country"))[0], "role" => "birth place" }
      if get_value("birth_spatial.city")
        birthplace["city"] = JSON.parse(get_value("birth_spatial.city"))[0]
      end
      places << birthplace
    end
    places
  end

  def keywords
    if get_value("year_degree_institution", true)
      educations = []
      get_value("year_degree_institution", true).each do |school|
        educations << school.split(":")[1].strip
      end
      educations
    end
  end

  def alternative
    get_value("name-letter")
  end

  def citation
    # not in the schema
    works = works.split(";;;") if get_value("work roles")
    {
      "works" => works
    }
  end

  def medium
    get_value("news item roles", true)
  end

  def topics
    get_value("birth-decade")
  end

  def subjects
    get_value("events", true)
  end

  def has_relation
    {
      "title" => get_value("commentaries_relation", true)
    }
  end

  def person
    result = []
    people = get_value("related-people")
    if people && people.length > 0
      people = people.split(";;;").uniq
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

end
