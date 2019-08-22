module Filters
  ALL_FILTERS = [PreviousContact]

  class TotalFilter < FilterBase

    # @return [Boolean] whether the prediction matches all filters in `Predictions::Filters::ALL_FILTERS`
    def filter
      Filters::ALL_FILTERS.all? { |filter| filter.filter(prediction) }
    end
  end
end
