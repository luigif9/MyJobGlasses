module Parsing
  extend self

  # @return [Array<Professional>]
  def parse_professionals(array)
    array.map { |hash| Professional.new(hash) } # Will be more complex when using real data
  end

  # @return [Array<Student>]
  def parse_students(array)
    array.map { |hash| Student.new(hash) } # Will be more complex when using real data
  end

  # @return [Array<Visit>]
  def parse_events(array)
    array.map { |hash| Event.new(hash) } # Will be more complex when using real data
  end
end
