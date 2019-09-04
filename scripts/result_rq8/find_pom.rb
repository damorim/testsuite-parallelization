#!/usr/bin/env ruby
require "optparse"
require "rexml/document"
include REXML


options = {}
OptionParser.new do |parser|
  parser.on("--path PATH", "The path to directory") do |v|
    options[:path] = v
  end
  parser.on("--file FILE", "The file path to directory") do |v|
    options[:file] = v
  end
end.parse!

target_path = options[:path]
file_path = options[:file]

if !target_path.nil? and Dir.exists? target_path
  poms = `find #{target_path} -name "#{file_path}.java" -type f`
  line_file = ""
  poms.each_line do |pom|
  	split_file = pom.strip.split("/")
    position_file = split_file.index("src") - 1	
    result_url = split_file[0..position_file].join("/")
    line_file = "#{result_url}/pom.xml"
  end

  poms_cmd = `find #{target_path} -name "pom.*xml" -type f`
  flag_line = false
  poms_cmd.each_line do |pom|
  	if pom.strip == line_file
  	  flag_line = true
  	end
  end

  if flag_line
  	puts line_file
  else
  	puts ""
  end

  
end
