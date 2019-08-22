require_relative "./../parsing/parsing.rb"

module Runtime
  module Events
    extend self

    # @return [true]
    def setup
      puts "Parsing events..."
      events
      puts "Finished parsing events!"
      true
    end

    def events
      return @events if @events
      array = JSON.parse(File.open(ENV['EVENTS_FILE_PATH']).read)
      Event.all = Parsing.parse_events(array)
    end
  end
end
