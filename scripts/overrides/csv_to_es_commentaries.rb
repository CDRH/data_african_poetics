require 'byebug'
class CsvToEsCommentaries < CsvToEs
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

  def text
    get_value("Content")
  end
end
