TODO

#### To execute full script: `ruby agamemnon.rb` (bash)
This will:
  - Download data from AWS
  - Parse the downloaded data
  - Calculate all the matrices we need for prediction purposes
  - Calculate the predictions on all professionals
  - Dump the predictions in the dump folder

#### To launch the console: (bash)
`ruby agamemnon/console.rb`
OR
`pry -r ./agamemnon/config/initializer.rb`
OR
`irb -r ./agamemnon/config/initializer.rb` if Pry is unavailable

#### Prerequisites:

- Ruby 2.2.5
- config/secrets.yml Ask @Startouf or @Liboul for the file
- Make sure the following files are available on AWS, in the right bucket:
  - professionals.json
  - students.json
  - events.js

- Gems:
  - Bundler: `gem install bundler & bundle install`
