class CsvToEsWorks < CsvToEs

  def assemble_collection_specific
    @json["page_k"] = get_value("Page no")
    @json["issue_k"] = get_value("Issue")
    @json["volume_k"] = get_value("Volume")
    @json["commentaries_k"] = get_value("[commentaries]")
    @json["complete_k"] = get_value("Complete")
    puts get_value("Page no"), get_value("Issue"), get_value("Volume"), get_value("[commentaries]"), get_value("Complete")
  end

  def id
    get_id
  end

  def category
    "Works"
  end

  def get_id
    id = @row["Unique ID"] ? @row["Unique ID"] : "blank"
    id = id.split(" ")[0]
    id
  end

  def title
    get_value("Primary Field")
  end

  def alternative
    get_value("Title")
  end

  def type
    get_value("Work type")
  end

  def date_display
    get_value("Year")
  end

  def publisher
    get_value("[publisher]")
  end

  def spatial
    if get_value("[location]")
      puts get_value("[location]")
    end
  end

  def source
    if get_value("[news item]")
      puts get_value("[news item]")
    end
  end

end
