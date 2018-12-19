#!/usr/bin/env ruby
require 'csv'
require 'optparse'
require 'ostruct'
require 'rexml/document'
include REXML

require_relative 'rbcommon.rb'

def get_test_variables project_path
  configs = {'C0'=>[], 'C1'=>[], 'C2'=>[], 'C3'=>[], 'FC0'=>[], 'FC1'=>[]}
  project_name = File.basename project_path
  poms = `find #{project_path} -name "pom.*xml" -type f`
  poms.each_line do |pom|

    next if pom.include? '/resources/'
    next if pom.include? '/test/'
    next if pom.include? '/target/'

    xml = Document.new IO.read(pom.strip)
    plugins = XPath.match xml, "//plugin/artifactId[. = 'maven-surefire-plugin']/../configuration"
    if not plugins.nil? and plugins.to_a.size > 0
      plugins.each do |configuration|
        dict = {}
        dict['parallel'] = get_element configuration, 'parallel'
        dict['reuseForks'] = get_element configuration, 'reuseForks'
        dict['useUnlimitedThreads'] = get_element configuration, 'useUnlimitedThreads'
        dict['threadCount'] = get_element configuration, 'threadCount'
        dict['perCoreThreadCount'] = get_element configuration, 'perCoreThreadCount'
        dict['threadCountClasses'] = get_element configuration, 'threadCountClasses'
        dict['parallelOptimized'] = get_element configuration, 'parallelOptimized'
        dict['threadCountMethods'] = get_element configuration, 'threadCountMethods'
        dict['forkCount'] = get_element configuration, 'forkCount'
        dict.keys.to_a.each do |key|
          if dict[key].nil?
            dict.delete key
          end
        end

        has_var = false
        dict.keys.each do |k|
          if dict[k].include? '{'
            has_var = true
            break
          end
        end

        dict['inferred'] = false
        possible = []
        if has_var
          if dict['parallel'] != nil and dict['parallel'].include? '{'
            ['methods', 'classes', 'both', 'suites', 'suitesAndClasses', 'suitesAndMethods', 'classesAndMethods', 'all'].each do |v|
              c = dict.clone
              c['inferred'] = true
              c['parallel'] = p
              possible << c
            end
          end
          if dict['forkCount'] != nil and dict['forkCount'].include? '{'
            new_possibles = []
            if possible.size > 0
              possible.each do |p|
                p2 = p.clone
                p2['forkCount'] = '1C'
                new_possibles << p2
                p2 = p.clone
                p2['forkCount'] = '1'
                new_possibles << p2
              end
              possible = new_possibles
            else
              c = dict.clone
              c['inferred'] = true
              c['forkCount'] = '1C'
              possible << c
              c = dict.clone
              c['inferred'] = true
              c['forkCount'] = '1'
              possible << c
            end
          end
          if dict['threadCount'] != nil and dict['threadCount'].include? '{'
            new_possibles = []
            if possible.size > 0
              possible.each do |p|
                p2 = p.clone
                p2['threadCount'] = '2'
                new_possibles << p2
                p2 = p.clone
                p2['threadCount'] = '1'
                new_possibles << p2
              end
              possible = new_possibles
            else
              c = dict.clone
              c['inferred'] = true
              c['threadCount'] = '2'
              possible << c
              c = dict.clone
              c['inferred'] = true
              c['threadCount'] = '1'
              possible << c
            end
          end
        else
          possible << dict
        end
        possible.each do |varia|
          level = get_nice_variables dict
          configs[level] << varia['inferred']
        end
      end    # /plugins.each
    end      # /if
  end        # /poms.each
  configs
end


def get_element xml, name
  child = xml.elements[name]
  if child.nil?
    return nil
  end
  child.text
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
    if Dir.exist?(project_path) and is_valid?(row)
      puts 'Checking project ' + row['name']
      configs = get_test_variables(project_path)
      create_csv_entry(row, configs, csv_entries)
      create_table_entry(row, configs, tex_entries)
    else
      puts 'Skipping project ' + row['name'] + ' (missing directory)'
    end
  end
end

CSV.open('static-variables.csv', 'w') do |csv|
  csv << ['name', 'inferred', 'mode']
  csv_entries.each do |r|
    csv << r 
  end
end

open('table1-static.tex', 'w') { |tex| tex.puts(tex_entries) }

