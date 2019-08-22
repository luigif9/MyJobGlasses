require 'pry'
require 'active_model'

# require ENV variable first
require_relative 'initializers/env'

# require all files in 'config/initializers' folder
Dir[File.expand_path('initializers/*.rb', File.dirname(__FILE__))].each { |file| require file }

# require all models
Dir[File.expand_path('models/*.rb', ENV['AGAMEMNON_ROOT'])].each { |file| require file }

# require custom libraries. Add your own to the following array. The base folder is the root of Agamemnon.
CUSTOM_LIBRARIES = []

# download data from aws
CUSTOM_LIBRARIES << 'aws/aws'

# load objects in memory
CUSTOM_LIBRARIES << 'parsing/parsing'

# projection
CUSTOM_LIBRARIES << 'projectors/professional_projector'
CUSTOM_LIBRARIES << 'projectors/student_projector'

# prediction
CUSTOM_LIBRARIES << 'prediction/predictor'
CUSTOM_LIBRARIES << 'prediction/recommender'

# runtime
CUSTOM_LIBRARIES << 'runtime/runtime'

# filters
CUSTOM_LIBRARIES << 'filters/filter_base'
CUSTOM_LIBRARIES << 'filters/previous_contact'
CUSTOM_LIBRARIES << 'filters/total_filter'

# dump predictions
CUSTOM_LIBRARIES << 'dumper/recommendation_dumper'

CUSTOM_LIBRARIES.each { |file| require_relative File.expand_path(file, ENV['AGAMEMNON_ROOT']) }
