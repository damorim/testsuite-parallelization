#!/usr/bin/env ruby
require 'csv'
require 'optparse'
require 'ostruct'
require 'rexml/document'
include REXML
require_relative 'rbcommon.rb'
require_relative 'service_tex.rb'


PROJECTS_HOME = "src/downloads/projects"  #options.path

tex_entries = []
avg_speed = 0
count_project = 0
total_time = 0
generate_header_and_body_tex(tex_entries)
CSV.foreach('./src/dataset-sanitized.csv', :headers => true) do |row|
  if is_valid?(row)
    project_path = File.join(PROJECTS_HOME, row['name'])
    if Dir.exist?(project_path) and is_valid?(row)
      puts 'Checking project ' + row['name']
      count_project += 1
      total_time += row['ts_tp'].to_f
      tex_entries << '%s & %s & %s & %s & %s ' % [row['timecost_group'], row['name'], row['ts'], row['tp'], row['ts_tp'] + ' \\\\%']
    else
      puts 'Skipping project ' + row['name'] + ' (missing directory)'
    end
  end
end
generate_footer_tex(tex_entries,total_time,count_project)


open('./src/table-speed.tex', 'w') { |tex| tex.puts(tex_entries) }