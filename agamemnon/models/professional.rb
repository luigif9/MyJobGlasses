class Professional
  include ActiveModel::Model
  attr_accessor :id, :tags, :school, :presentation, :job_title

  delegate :domains_and_weights, to: :domain_projection

  # @return [Array<DomainProjection>]
  def domain_projection
    @domain_projection ||= calculate_projection
  end

  def calculate_projection
    @domain_projection = ProfessionalProjector.project(self)
  end

  def self.all=(professionals_array)
    @all = professionals_array
  end

  def self.all
    @all
  end

  def self.find_by_id(id)
    all.find { |pro| pro.id == id }
  end
end
