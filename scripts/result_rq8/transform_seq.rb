#!/usr/bin/env ruby
require 'optparse'
require 'ostruct'
require 'rexml/document'
include REXML


def get_element xml, name
  child = xml.elements[name]
  if child.nil?
    child = Element.new name
    xml << child
  end
  child
end


def set_value xml, name, value
  element = get_element xml, name
  element.text = value
end


options = {}
OptionParser.new do |parser|
  parser.on("--path PATH", "The path to directory") do |v|
    options[:path] = v
  end
end.parse!

target_path = options[:path]

begin
  xml = Document.new IO.read(target_path)
  puts "Loading pom: #{target_path}"
  plugins = XPath.match xml, "//plugin/artifactId[. = 'maven-surefire-plugin']"
  if not plugins.nil? and plugins.to_a.size > 0
    plugins.each do |plugin|
      puts "Changing plugin in pom: #{target_path}"
      surefire = plugin.parent
      configuration = get_element surefire, 'configuration'
      set_value configuration, 'parallel', 'none'
      set_value configuration, 'forkCount', '1'
      set_value configuration, 'reuseForks', 'true'
      set_value configuration, 'useUnlimitedThreads', 'false'
      set_value configuration, 'threadCount', '1'
      set_value configuration, 'perCoreThreadCount', 'false'
    end
  else
    project = get_element xml, 'project'
    build = get_element project, 'build'
    plugins = get_element build, 'plugins'
    plugin = Element.new 'plugin'
    set_value plugin, 'groupId', 'org.apache.maven.plugins'
    set_value plugin, 'artifactId', 'maven-surefire-plugin'
    configuration = get_element plugin, 'configuration'
    set_value configuration, 'parallel', 'none'
    set_value configuration, 'forkCount', '1'
    set_value configuration, 'reuseForks', 'true'
    set_value configuration, 'useUnlimitedThreads', 'false'
    set_value configuration, 'threadCount', '1'
    set_value configuration, 'perCoreThreadCount', 'false'
    set_value configuration, 'fork', 'false'
    set_value configuration, 'forkMode', 'once'
    plugins << plugin
  end

  puts "Removing pom: #{target_path}"
  File.delete target_path
  file = ''
  puts "Recreating pom: #{target_path}"
  formatter = REXML::Formatters::Pretty.new(3)
  formatter.compact = true
  formatter.write(xml, file)
  IO.write target_path, file
rescue

end

