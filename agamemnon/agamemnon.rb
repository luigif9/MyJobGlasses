require_relative "config/initializer"

puts "Downloading data from AWS..."
Runtime.download_from_aws
puts "OK!"

puts "Parsing data..."
Runtime.parse
puts "OK!"

puts "Calculating projections..."
Runtime.calculate_projections
puts "OK!"

puts "Predicting..."
Runtime.predict_all
puts "OK!"

Runtime.dump_predictions
