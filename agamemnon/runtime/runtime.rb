require_relative "entities"
require_relative "events"
require_relative "projections"

module Runtime
  extend self

  def download_from_aws
    AWS.download_all
  end

  def parse
    Runtime::Entities.setup
    Runtime::Events.setup
  end

  # Needs to be done after `parse`
  def calculate_projections
    Runtime::Projections.setup
  end

  # Needs to be done after `calcule_matrices`
  # @return [True]
  def predict_all
    @recommendations = Professional.all.map do |professional|
      Recommender.new(professional).recommend
    end
    true
  end

  # Needs to be done after `predict_all`
  # Creates a file in the /dump folder
  def dump_predictions
    file_name = predictions_dump_file_name
    file_path = File.expand_path(file_name, ENV['DUMP'])
    recommendations_json = JSON.dump(@recommendations.map { |x| RecommendationDumper.dump(x) }.reduce(:+))
    File.open(file_path, 'w') { |file| file.write(recommendations_json) }
    puts "The results have been dumped in this file: dump/#{file_name}"
  end

  private

  def predictions_dump_file_name
    "agamemnon_predictions_#{Time.now.strftime('%Y_%m_%d_%H%M%S')}.json"
  end
end
