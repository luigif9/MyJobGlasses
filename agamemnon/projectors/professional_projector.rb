require File.expand_path('models/domain_projection', ENV['AGAMEMNON_ROOT'])

class ProfessionalProjector
  def self.project(professional)
    new(professional).project
  end

  attr_reader :professional, :projection

  # @param professional [Professional]
  def initialize(professional)
    @professional = professional
  end

  # @return [Array<DomainProjection>]
  def project
    domains_and_weights = Domain.all.map { |domain| add_weight_to_domain(domain) }
    @projection = DomainProjection.new(professional, DomainProjection.standardize_domains_weights(domains_and_weights))
  end

  private

  # @return [Array<String>]
  def standardized_professional_tags
    @standardized_professional_tags ||= professional.tags.map{ |tag| standardize_tag(tag)}
  end

  # @param tag [String, Symbol]
  # @return [String]
  def standardize_tag(tag)
    ActiveSupport::Inflector.transliterate(tag.to_s.downcase)
  end

  # @param domain [Domain]
  # @return [[Domain, Weight]]
  def add_weight_to_domain(domain)
    weight = standardized_professional_tags.include?(standardize_tag(domain.name)) ? 1.0 : 0.0
    [domain, weight]
  end
end
