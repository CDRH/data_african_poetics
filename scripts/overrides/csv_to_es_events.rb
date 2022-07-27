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
    nonpoets = get_value("person-notpoet", true)
    poets = get_value("person-poet", true)
    if nonpoets && nonpoets.length > 0
      nonpoets.each do |nonpoet|
        name = /\[(.*)\]/.match(nonpoet)[1] if /\[(.*)\]/.match(nonpoet)
        people << { name: name }
      end
    end
    if poets && poets.length > 0
      poets.each do |poet|
        name = /\[(.*)\]/.match(poet)[1] if /\[(.*)\]/.match(poet)
        id = /\((.*)\)/.match(poet)[1] if /\((.*)\)/.match(poet)
        role = "African Poet"
        people << { name: name, role: role, id: id }
      end
    end
    people
  end

  def topics
    get_value("topics-decade")
  end

  def places
    get_value("places")
  end

  def spatial
    locations = []
    if get_value("spatial.country")
      JSON.parse(get_value("spatial.country")).each do |country|
        location = { "country" => JSON.parse(get_value("spatial.country")) }
        if get_value("spatial.city")
          location["city"] = JSON.parse(get_value("spatial.city"))
        end
        if get_value("spatial.region")
          location["region"] = JSON.parse(get_value("spatial.region"))
        end
        locations << location
      end
    end
    locations
  end

  def relation
    get_value("commentaries_relation", true)
  end

  def medium
    get_value("news_items", true)
  end

end
