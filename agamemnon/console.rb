#!/usr/bin/env ruby
require 'pry'
require_relative 'config/initializer'

module Console
  extend self

  def memory_usage
    _pid, size = `ps ax -o pid,rss | grep -E "^[[:space:]]*#{$$}"`.strip.split.map(&:to_i)
    size
  end
end

Pry.start
