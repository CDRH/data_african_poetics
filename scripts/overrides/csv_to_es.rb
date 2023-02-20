class CsvToEs

  def array_to_string (array,sep)
    return array.map { |i| i.to_s }.join(sep)
  end
  
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

  def text
    built_text = []
    @row.each do |column_name, value|
      built_text << value.to_s
    end
    return array_to_string(built_text, " ")
  end
end
