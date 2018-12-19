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


options = OpenStruct.new
OptionParser.new do |opts|
  opts.on('-p', '--path [PATH]', String, 'Path of subject') do |path|
    options.path = path
  end
end.parse!

poms = `find #{options.path} -name "pom.*xml" -type f`
pom_paths = []
poms.each_line do |pom|
    pom_paths << pom.strip
end

pom_paths.each do |pom|
  begin
    xml = Document.new IO.read(pom.strip)
    puts "Loading pom: #{pom.strip}"
    plugins = XPath.match xml, "//plugin/artifactId[. = 'maven-surefire-plugin']"
    if not plugins.nil? and plugins.to_a.size > 0
      plugins.each do |plugin|
        puts "Changing plugin in pom: #{pom}"
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

    puts "Removing pom: #{pom}"
    File.delete pom.strip
    file = ''
    puts "Recreating pom: #{pom}"
    formatter = REXML::Formatters::Pretty.new(3)
    formatter.compact = true
    formatter.write(xml, file)
    IO.write pom.strip, file
  rescue

  end
end
