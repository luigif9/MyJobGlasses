class Event
  SCORE_MAPPING = {
    visit: 1,
    conversation: 3,
    meeting: 5,
    like: 10
  }

  include ActiveModel::Model
  attr_accessor :type, :student_id, :professional_id

  def score
    SCORE_MAPPING[type.to_sym]
  end

  def professional
    @professional ||= Professional.find_by_id(professional_id)
  end

  def student
    @student ||= Professional.find_by_id(professional_id)
  end

  def self.all=(events_array)
    @all = events_array
  end

  def self.all
    @all
  end

  def self.all_by_student_id
    @all_by_student_id ||= all.group_by(&:student_id)
  end

  # @param student_id [ObjectId]
  def self.find_by_student_id(student_id)
    Event.all.select{ |event| event.student_id == student_id }
  end
end
