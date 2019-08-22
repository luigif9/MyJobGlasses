class Domain
  ALL_DOMAINS = %w(banque finance assurance marketing digital industrie supply_chain production beton)

  include ActiveModel::Model
  attr_accessor :id, :name

  def self.all=(domains_array)
    @all = domains_array
  end

  def self.all
    @all ||= ALL_DOMAINS.map { |domain| Domain.new(id: domain, name: domain) }
  end

  # @param name [String, Symbol]
  # @return [Domain, nil]
  def self.find_by_name(name)
    all.find { |domain| domain.name.to_s == name.to_s }
  end
end
