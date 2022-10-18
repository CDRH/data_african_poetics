class CsvToEs
  def get_value(name, parse=false)
    if @row[name] && @row[name].length > 0
      if parse
        JSON.parse(@row[name])
      else
        @row[name]
      end
    end
  end

  def abstract
  end
end
