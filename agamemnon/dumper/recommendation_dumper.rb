class RecommendationDumper
  def self.dump(recommendation)
    new(recommendation).dump
  end

  attr_reader :recommendation

  # @param recommendation
  def initialize(recommendation)
    @recommendation = recommendation
  end

  # @return [Array<Hash>]
  def dump
    index = 0
    recommendation.predictions.map do |prediction|
      index += 1
      {
        professional_id: prediction.professional.id,
        student_id: prediction.student.id,
        score: prediction.score,
        index: index
      }
    end
  end
end
