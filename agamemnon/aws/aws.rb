module AWS
  extend self

  ALL_FILES = [
    ENV['PROFESSIONALS_FILE'],
    ENV['STUDENTS_FILE'],
    ENV['VISITS_FILE'],
    ENV['CONTACTS_FILE'],
  ]

  def s3
    @s3 ||= Aws::S3::Client.new
  end

  def download_all
    ALL_FILES.each { |file| download(file) }
  end

  def download(file)
    s3.get_object({bucket: ENV['AWS_RECOMMENDATION_BUCKET'], key: ENV['AWS_EXTRACT_FOLDER'] + '/' + file},
      target: File.expand_path(file, ENV['DATA']))
  end
end
