class StudentProjector

  delegate :add_hashes, :multiply_hash, to: DomainProjection

  def self.project(student)
    new(student).project
  end

  attr_reader :student

  # @param student [Student]
  def initialize(student)
    @student = student
  end

  # @return [Array<DomainProjection>]
  def project
    @projection = DomainProjection.new(student, standardized_domains_and_weights)
  end

  private

  # @return [Array<Hash<Domain, Float>>], see example below
  # [
  #  {#<Domain:0x007fdcd4985158 @id="banque", @name="banque"> => 0.3333333333333333,
  #   #<Domain:0x007fdcd4985068 @id="finance", @name="finance"> => 0.3333333333333333,
  #   #<Domain:0x007fdcd4984f78 @id="assurance", @name="assurance"> => 0.3333333333333333,
  #   #<Domain:0x007fdcd4984e88 @id="marketing", @name="marketing"> => 0.0,
  #   #<Domain:0x007fdcd4984d98 @id="digital", @name="digital"> => 0.0,
  #   #<Domain:0x007fdcd4984ca8 @id="industrie", @name="industrie"> => 0.0,
  #   #<Domain:0x007fdcd4984bb8 @id="supply_chain", @name="supply_chain"> => 0.0,
  #   #<Domain:0x007fdcd4984ac8 @id="production", @name="production"> => 0.0,
  #   #<Domain:0x007fdcd49849d8 @id="beton", @name="beton"> => 0.0},
  #
  #  {#<Domain:0x007fdcd4985158 @id="banque", @name="banque"> => 0.0,
  #   #<Domain:0x007fdcd4985068 @id="finance", @name="finance"> => 0.0,
  #   #<Domain:0x007fdcd4984f78 @id="assurance", @name="assurance"> => 0.0,
  #   #<Domain:0x007fdcd4984e88 @id="marketing", @name="marketing"> => 1.5,
  #   #<Domain:0x007fdcd4984d98 @id="digital", @name="digital"> => 1.5,
  #   #<Domain:0x007fdcd4984ca8 @id="industrie", @name="industrie"> => 0.0,
  #   #<Domain:0x007fdcd4984bb8 @id="supply_chain", @name="supply_chain"> => 0.0,
  #   #<Domain:0x007fdcd4984ac8 @id="production", @name="production"> => 0.0,
  #   #<Domain:0x007fdcd49849d8 @id="beton", @name="beton"> => 0.0}
  #   ]
  def weighted_projections
    student.events.group_by(&:professional).map do |professional, events_array|
      multiply_hash(professional.calculate_projection.domains_and_weights, events_array.map(&:score).max)
    end
  end

  # @return [Hash<Domain, Float>], see example below
  # {
  #  #<Domain:0x007fdcd4985158 @id="banque", @name="banque"> => 0.3333333333333333,
  #  #<Domain:0x007fdcd4985068 @id="finance", @name="finance"> => 0.3333333333333333,
  #  #<Domain:0x007fdcd4984f78 @id="assurance", @name="assurance"> => 0.3333333333333333,
  #  #<Domain:0x007fdcd4984e88 @id="marketing", @name="marketing"> => 1.5,
  #  #<Domain:0x007fdcd4984d98 @id="digital", @name="digital"> => 1.5,
  #  #<Domain:0x007fdcd4984ca8 @id="industrie", @name="industrie"> => 0.0,
  #  #<Domain:0x007fdcd4984bb8 @id="supply_chain", @name="supply_c ha in">=>0.0,
  #  #<Domain:0x007fdcd4984ac8 @id="production", @name="production"> => 0.0,
  #  #<Domain:0x007fdcd49849d8 @id="beton", @name="beton"> => 0.0
  # }
  def domains_and_weights
    add_hashes(weighted_projections)
  end

  # @return [Hash<Domain, Float>], see example below, same format as domains_and_weights
  def standardized_domains_and_weights
    DomainProjection.standardize_domains_weights(domains_and_weights)
  end
end
