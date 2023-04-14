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

  def parse_md_brackets(query)
    if /\[(.*)\]/.match(query)
      /\[(.*?)\]/.match(query)[1]
    else
      query
    end
  end

  def parse_md_parentheses(query)
    /\]\((.*)\)/.match(query)[1] if /\]\((.*)\)/.match(query)
  end

  def abstract
  end

  def text
    built_text = []
    @row.each do |column_name, value|
      excluded_columns = ["related-people", "airtableID", "Primary Field", "Complete", "Source page no", "Source link", "Gale ID", "Source access date", "rights_holder", "Major african poet", "name-letter", "Page no", "Issue", "Volume"]
      if excluded_columns.include?(column_name) || /\[.*\]/.match(column_name)
        next
      end
      if valid_json?(value) && JSON.parse(value).is_a?(Array)
        built_text << parse_array(JSON.parse(value))
      elsif value.include?(";;;")
        built_text << parse_array(value.split(";;;"))
      else
        built_text << parse_value(value)
      end
    end
    return array_to_string(built_text, " ")
  end

  def parse_array(arr)
    arr.map { |value|
      parsed = parse_md_brackets(value)
      check_markdown(parsed) ? parsed : next
    }.join(" ")
  end

  def parse_value(value)
    parse_md_brackets(value)
  end

  def valid_json?(json)
    JSON.parse(json)
    true
  rescue JSON::ParserError, TypeError => e
    false
  end

  def check_markdown(value)
    !(value == nil || value[0] == "|")
  end
end
