require 'yaml'

# Load all keys from secrets.yml and create class methods (always lowercase) under ENV
# For instance, if 'secrets.yml' has a key/value pair `AWS_KEY: "abcdef123"`,
# You will be able to do `ENV["aws_key"]` and that returns "abcdef123"
YAML.load_file(File.expand_path('../secrets.yml', File.dirname(__FILE__))).each do |key, value|
  ENV[key.upcase] = value
end

# Paths to folders / files
ENV['AGAMEMNON_ROOT'] = File.expand_path('../../..', __FILE__)
ENV['DUMP'] = File.expand_path('../dump', ENV['AGAMEMNON_ROOT'])
ENV['DATA'] = File.expand_path('../data', ENV['AGAMEMNON_ROOT'])
ENV['PROFESSIONALS_FILE_PATH'] = File.expand_path(ENV['PROFESSIONALS_FILE'], ENV['DATA'])
ENV['STUDENTS_FILE_PATH'] = File.expand_path(ENV['STUDENTS_FILE'], ENV['DATA'])
ENV['EVENTS_FILE_PATH'] = File.expand_path(ENV['EVENTS_FILE'], ENV['DATA'])
