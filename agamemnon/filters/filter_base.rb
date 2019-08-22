module Filters
  class FilterBase
    def self.filter(prediction)
      new(prediction).filter
    end

    attr_reader :prediction

    # @param prediction [Prediction]
    def initialize(prediction)
      @prediction = prediction
    end

    # Must be overridden by child classes
    # @return [Boolean] whether the prediction passed the filter
    def filter
      raise NotImplementedError
    end
  end
end
