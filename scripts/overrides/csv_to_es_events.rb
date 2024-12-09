require "byebug"
class CsvToEsEvents < CsvToEs
  def id
    get_id
  end

  def category
    "Events"
  end

  def get_id
    id = @row["Unique ID"] ? @row["Unique ID"] : "blank"
    id = id.split(" ")[0]
    id
  end

  def title
    get_value("Name")
  end

  def date(before=false)
    Datura::Helpers.date_standardize(@row["Date"], before)
  end

  def date_not_before
    if @row["Date not before"]
      Datura::Helpers.date_standardize(@row["Date not before"], false)
    end
  end

  def description
    get_value("Summary")
  end

  def type
    get_value("Event type")
  end

  def person
    people = []
    #non-poets just have a name, poets also have id and role
    nonpoets = get_value("person-notpoet", true)
    poets = get_value("person-poet", true)
    if nonpoets && nonpoets.length > 0
      nonpoets.each do |nonpoet|
        # markdown parsing
        name = parse_md_brackets(nonpoet)
        people << { "name" => name }
      end
    end
    if poets && poets.length > 0
      poets.each do |poet|
        # markdown parsing
        name = parse_md_brackets(poet)
        id = parse_md_parentheses(poet)
        role = "African Poet"
        people << { "name" => name, "role" => role, "id" => id }
      end
    end
    people
  end

  def topics
    get_value("topics-decade")
  end

  def spatial
    locations = []
    if get_value("spatial.country")
      event_location = { "country" => JSON.parse(get_value("spatial.country"))[0], "role" => "event location" }
      if get_value("spatial.city")
        event_location["city"] = JSON.parse(get_value("spatial.city"))[0]
      end
      if get_value("spatial.region")
        event_location["region"] = JSON.parse(get_value("spatial.region"))[0]
      end
      locations << event_location
    end
    if get_value("places")
      placename = { "short_name" => get_value("places"), "role" => "placename" }
      locations << placename
    end
    locations
  end

  def has_relation
    {
      "title" => get_value("commentaries_relation", true)
    }
  end

  def medium
    get_value("news_items", true)
  end

end
