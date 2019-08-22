class Recommender
  attr_reader :professional

  # @param professional [Professional]
  def initialize(professional)
    @professional = professional
  end

  # @param r_best [Integer], defaults to 5
  # @param min_score [Float] between 0 & 1, defaults to 0.4
  # @return [Recommendation]
  def recommend(r_best: 5, min_score: 0.4)
    predictions = Predictor.predict(professional) # get raw predictions
    predictions.select! { |prediction| prediction.score >= min_score } # filter predictions with low scores
    predictions.select! { |prediction| Filters::TotalFilter.filter(prediction) } # custom filters
    predictions = predictions.sort_by(&:score).reverse[0..r_best - 1] # sort predictions by score
    Recommendation.new(predictions: predictions) # wrap in a recommendation object
  end
end
