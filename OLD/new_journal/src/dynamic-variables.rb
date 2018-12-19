#!/usr/bin/env ruby
require 'csv'
require 'optparse'
require 'ostruct'
require_relative 'rbcommon.rb'

MAVEN_SKIPS = "-Drat.skip=true -Dmaven.javadoc.skip=true \
               -Djacoco.skip=true -Dcheckstyle.skip=true \
               -Dfindbugs=true -Dcobertura.skip=true"


def get_test_variables project_path
  if not File.exists? "#{project_path}/variables.log"
    variables = `cd #{project_path} && mvn test -X -DskipTests #{MAVEN_SKIPS}`
    IO.write "#{project_path}/variables.log", variables
  end
  regex = '"\[DEBUG\]   (.*) \(.*\) = \(.*\)"'
  variables = `cat #{project_path}/variables.log | grep #{regex} | awk '{print $3" ~> "$5}'`
  mods = []
  current_line = []
  variables.each_line do |line|
    if line.start_with? 'workingDirectory'
      current_line << line
      mods << current_line
      current_line = []
    else
      current_line << line
    end
  end
  configs = {'C0'=>[], 'C1'=>[], 'C2'=>[], 'C3'=>[], 'FC0'=>[], 'FC1'=>[]}
  mods.each do |mod|
    dict = {}
    mod.each do |line|
      opt = line.split '~>'
      dict[opt[0].strip] = opt[1].chomp.strip
    end
    module_name = File.basename dict['workingDirectory']
    level = get_nice_variables dict
    configs[level] << module_name
  end
  configs
end


options = OpenStruct.new
OptionParser.new do |opts|
  opts.on('-p', '--path [PATH]', String, 'Path of subjects\'s home') do |path|
    options.path = path
  end
end.parse!


PROJECTS_HOME = options.path

csv_entries = []
tex_entries = []
CSV.foreach('dataset-sanitized.csv', :headers => true) do |row|
  if is_valid?(row)
    project_path = File.join(PROJECTS_HOME, row['name'])
    if Dir.exist?(project_path)
      puts 'Checking project ' + row['name']
      configs = get_test_variables(project_path)
      create_csv_entry(row, configs, csv_entries)
      create_table_entry(row, configs, tex_entries)
    else
      puts 'Skipping project ' + row['name'] + ' (missing directory)'
    end
  end
end

CSV.open('dynamic-variables.csv', 'w') do |csv|
  csv << ['name', 'module', 'mode']
  csv_entries.each do |r|
    csv << r 
  end
end
open('table1.tex', 'w') { |tex| tex.puts(tex_entries) }

