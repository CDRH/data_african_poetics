require 'byebug'
class CsvToEsCommentaries < CsvToEs

  def assemble_collection_specific
    @json["html_k"] = get_value("Content")
  end

  def id
    get_id
  end

  def category
    "Commentaries"
  end

  def get_id
    id = @row["Unique ID"] ? @row["Unique ID"] : "blank"
    id = id.split(" ")[0]
    id
  end

  def title
    get_value("Name")
  end

  def person
    result = []
    people = get_value("person-poet", true)
    if people && people.length > 0
      people.each do |person|
        # markdown parsing
        name = parse_md_brackets(person)
        id = parse_md_parentheses(person)
        result << { name: name, id: id }
      end
    end
    result
  end

  def creator
    names = get_value("creator.name", true)
    if names
      names.collect{ |name| { "name": name }}
    end
  end

  def subjects
    get_value("events-subjects", true)
  end

  def medium
    get_value("news-items_medium", true)
  end

  def works
    get_value("works", true)
  end

end
