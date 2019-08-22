class Predictor
  def self.predict(professional)
    new(professional).predict
  end

  attr_reader :professional, :distance, :p, :predictions

  # @param professional [Professional]
  # @param distance [Symbol] in [:euclid]
  def initialize(professional, distance: 'Lp', p: 2)
    @professional = professional
    @distance = distance.to_s
    @p = p.to_f
    raise BadInitializationError.new("You need a p (Float > 0) when using an Lp distance") if @distance == 'Lp' && @p == 0.0
  end

  # @return [Array<Prediction>]
  def predict
    @predictions = Runtime::Entities.students.map do |student|
      score = calculate_similarity(student.domain_projection.to_vector, professional.domain_projection.to_vector)
      Prediction.new(professional: professional, student: student, score: score)
    end
  end

  private

  # @param vector1, vector2 [Array<Float>]
  # # @return [Float]
  def calculate_distance(vector1, vector2)
    raise NotImplementedDistanceError.new("The distance #{distance} is not supported") unless distance == 'Lp'
    vector1.zip(vector2).map { |a, b| (a - b).abs ** p }.reduce(:+) ** (1/p)
  end

  # @param vector1, vector2 [Array<Float>]
  # @return [Float] between 0.0 and 1.0
  def calculate_similarity(vector1, vector2)
    1 - calculate_distance(vector1, vector2) / (2.0 ** (1/p))
  end

  class NotImplementedDistanceError < StandardError; end
  class BadInitializationError < StandardError; end
end
