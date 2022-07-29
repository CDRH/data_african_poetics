class CsvToEsPeople < CsvToEs
  def id
    get_id
  end

  def category
    "People"
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
    get_value("Short biography")
  end

  def type
    if @row["Major african poet"] == "True"
      "Major African poet"
    end
  end

  def spatial
    places = []
    if get_value("nationality-region")
      places << { "region" => JSON.parse(get_value("nationality-region"))[0], "type" => "nationality" }
    end
    if get_value("birth_spatial.country")
      birthplace = { "country" => JSON.parse(get_value("birth_spatial.country"))[0], "type" => "birth place" }
      if get_value("birth_spatial.city")
        birthplace["city"] = { "city" => JSON.parse(get_value("birth_spatial.city"))[0] }
      end
      places << birthplace
    end
    places
  end

  def places
    get_value("nationality-country", true)
  end

  def keywords
    get_value("year_degree_institution", true)
  end

  def alternative
    get_value("name-letter")
  end

  def works
    works = get_value("work roles")
    works.split(";;;") if works
  end

  def medium
    news_items = get_value("news item roles")
    news_items.split(";;;") if news_items
  end

  def topics
    get_value("birth-decade")
  end

  def subjects
    get_value("events", true)
  end

  def relation
    get_value("Title markdown")
  end

  def person
    people = get_value("related-people")
    if people
      people = people.split(";;;") if people
      unique = people.uniq
      result = []
      unique.each do |person|
        name = /\[(.*)\]/.match(person)[1] if /\[(.*)\]/.match(person)
        id = /\((.*)\)/.match(person)[1] if /\((.*)\)/.match(person)
        count = people.select{|p| p == person}.count
        if name
          result << { name: name, role: count, id: id }
        end
      end
      result
    end
  end

end
