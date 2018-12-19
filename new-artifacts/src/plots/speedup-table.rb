#!/usr/bin/env ruby
require 'csv'
require 'optparse'
require 'ostruct'
require 'rexml/document'
include REXML

options = OpenStruct.new
OptionParser.new do |opts|
  opts.on('-p', '--path [PATH]', String, 'Path of subjects\'s home') do |path|
    options.path = path
  end
end.parse!


PROJECTS_HOME = options.path

tex_entries = []
CSV.foreach('dataset-sanitized.csv', :headers => true) do |row|
  if is_valid?(row)
    project_path = File.join(PROJECTS_HOME, row['name'])
    if Dir.exist?(project_path) and is_valid?(row)
      puts 'Checking project ' + row['name']
      tex_entries << "test"
    else
      puts 'Skipping project ' + row['name'] + ' (missing directory)'
    end
  end
end


open('table-speed.tex', 'w') { |tex| tex.puts(tex_entries) }