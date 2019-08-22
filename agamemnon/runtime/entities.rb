require_relative "./../parsing/parsing.rb"

module Runtime
  module Entities
    extend self

    # @return [true]
    def setup
      puts "Parsing professionals..."
      professionals
      puts "Finished parsing professionals!"

      puts "Parsing students..."
      students
      puts "Finished parsing students!"
      true
    end

    # @return [Array<Professional>]
    def professionals
      return @professionals if @professionals
      array = JSON.parse(File.open(ENV['PROFESSIONALS_FILE_PATH']).read)
      Professional.all = Parsing.parse_professionals(array)
    end

    # @return [Array<Student>]
    def students
      return @students if @students
      array = JSON.parse(File.open(ENV['STUDENTS_FILE_PATH']).read)
      Student.all = Parsing.parse_students(array)
    end
  end
end
