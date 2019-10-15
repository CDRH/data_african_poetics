# NOTE: We don't use this class at all except to override the default behavior
# because we want this handled entirely via CSV not HTML script

class FileHtml < FileType

  def post_es(url=nil)
    { "docs" => [] }
  end

  def transform_es
  end

  def transform_html
  end

end
