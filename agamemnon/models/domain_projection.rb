class DomainProjection
  attr_reader :entity, :domains_and_weights

  # @param entity [Professional, Student]
  # @param domains_and_weights [Array<Domain, Float> or Hash<Domain, Float>]
  def initialize(entity, domains_and_weights)
    @entity = entity
    @entity_id = entity.id
    @entity_type = entity.class
    @domains_and_weights = Hash[domains_and_weights]
  end

  # @return [Float]
  def [](domain)
    domains_and_weights[domain]
  end

  def to_vector
    domains_and_weights.map(&:last)
  end

  # @param domains_and_weights [Array<[Domain, Weight]>]
  def self.standardize_domains_weights(domains_and_weights)
    total_weight = domains_and_weights.map(&:last).reduce(:+)
    return domains_and_weights if total_weight.to_f == 0.0
    domains_and_weights.map{ |domain, weight| [domain, weight / total_weight]}
  end

  # @param hash [Hash]
  # @param float [Float]
  # @return [Hash]
  # example: `DomainProjection.multiply_hash({a: 1, b: 2}, 3.0)` returns `{a: 3.0, b: 6.0}`
  def self.multiply_hash(hash, float)
    hash.reduce({}) { |h, (k, v) | h[k] = v.to_f * float.to_f ; h }
  end

  # @param hash1, hash2 [Hash]
  # @return [Hash<Object, Float>]
  # example: `DomainProjection.addition_merge({a: 1, b: 2}, {b: 3, c: 4})` returns `{a: 1, b: 5, c: 4}`
  def self.addition_merge(hash1, hash2)
    hash1.merge(hash2) {|_key, val1, val2| val1 + val2}
  end


  # @param hashes [Array<Hash<Object, Float>>]
  # Adds-merges all the hashes in the given array (uses `addition_merge`)
  def self.add_hashes(hashes)
    hashes.reduce({}) { |h, hash2|  addition_merge(h, hash2)}
  end
end
