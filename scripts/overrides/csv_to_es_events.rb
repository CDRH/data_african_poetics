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
end
