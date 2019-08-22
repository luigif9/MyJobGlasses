class Student
  include ActiveModel::Model
  attr_accessor :id

  delegate :domains_and_weights, to: :domain_projection

  # @return [Array<DomainProjection>]
  def domain_projection
    @domain_projection ||= calculate_projection
  end

  def calculate_projection
    @domain_projection = StudentProjector.project(self)
  end

  def events
    @events ||= Event.all_by_student_id[id]
  end

  def self.all=(students_array)
    @all = students_array
  end

  def self.all
    @all
  end

  def self.find_by_id(id)
    all.find{ |pro| pro.id == id }
  end
end
