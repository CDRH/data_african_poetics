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
    get_value("Primary Field")
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

  def abstract
    get_value("Bibliography")
  end

  def extent
    get_value("Name [Gender]")
  end

  def type
    if @row["Major african poet"] == "True"
      "Major African poet"
    end
  end
end
