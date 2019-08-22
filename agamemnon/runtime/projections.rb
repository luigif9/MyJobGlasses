module Runtime
  module Projections
    extend self

    # @return [True]
    # Needs to habe entities and events already set up
    def setup
      puts "Calculating professionals projections..."
      calculate_professionals_projections
      puts "OK!"
      puts "Calculating students projections..."
      calculate_students_projections
      puts "OK!"
      true
    end

    def calculate_professionals_projections
      Professional.all.each(&:calculate_projection)
    end

    def calculate_students_projections
      Student.all.each(&:calculate_projection)
    end
  end
end
