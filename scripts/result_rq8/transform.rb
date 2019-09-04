#!/usr/bin/env ruby
require "optparse"
require "rexml/document"
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

def poolSettings configuration
  set_value configuration, 'forkCount', '1'
  set_value configuration, 'useUnlimitedThreads', 'false'
  set_value configuration, 'perCoreThreadCount', 'true'
  set_value configuration, 'threadCount', '1'
end

def c0 configuration
  set_value configuration, 'forkCount', '1'
  set_value configuration, 'useUnlimitedThreads', 'false'
  set_value configuration, 'perCoreThreadCount', 'false'
  set_value configuration, 'threadCount', '0'
  set_value configuration, 'parallel', 'none'
end

def c1 configuration
  poolSettings configuration
  set_value configuration, 'parallel', 'methods'
end

def c2 configuration
  poolSettings configuration
  set_value configuration, 'parallel', 'classes'
end

def c3 configuration
  poolSettings configuration
  set_value configuration, 'parallel', 'both'
end

def fc0 configuration
  set_value configuration, 'forkCount', '1C'
  set_value configuration, 'useUnlimitedThreads', 'false'
  set_value configuration, 'perCoreThreadCount', 'false'
  set_value configuration, 'threadCount', '0'
  set_value configuration, 'parallel', 'none'
end

def fc1 configuration
  c1 configuration
  set_value configuration, 'forkCount', '1C'
end

def check pom
  xml = Document.new IO.read(pom.strip)
  puts "Loading pom: #{pom.strip}"
  plugins = XPath.match xml, "//plugin/artifactId[. = 'maven-surefire-plugin']/"
  if not plugins.nil? and plugins.to_a.size > 0
    plugins.each do |node|
      puts get_element node.parent, "version"
    end
  end
end

# Copied from luis' code
def transform pom
  xml = Document.new IO.read(pom.strip)
  puts "Loading pom: #{pom.strip}"
  plugins = XPath.match xml, "//plugin/artifactId[. = 'maven-surefire-plugin']"
  if not plugins.nil? and plugins.to_a.size > 0
    plugins.each do |plugin|
      #puts "Changing plugin in pom: #{pom}"
      surefire = plugin.parent
      configuration = get_element surefire, 'configuration'
      #puts pom if get_element(surefire, 'version').to_s.include? '2.6'
      c0 configuration if pom.include? '_C0'
      c1 configuration if pom.include? '_C1'
      c2 configuration if pom.include? '_C2'
      c3 configuration if pom.include? '_C3'
      fc0 configuration if pom.include? '_FC0'
      fc1 configuration if pom.include? '_FC1'
    end

  else
    project = get_element xml, 'project'
    build = get_element project, 'build'
    plugins = get_element build, 'plugins'
    plugin = Element.new 'plugin'
    set_value plugin, 'groupId', 'org.apache.maven.plugins'
    set_value plugin, 'artifactId', 'maven-surefire-plugin'
    configuration = get_element plugin, 'configuration'
    c0 configuration if pom.include? '_C0'
    c1 configuration if pom.include? '_C1'
    c2 configuration if pom.include? '_C2'
    c3 configuration if pom.include? '_C3'
    fc0 configuration if pom.include? '_FC0'
    fc1 configuration if pom.include? '_FC1'
    plugins << plugin
  end
  File.delete pom.strip
  file = ''
  formatter = REXML::Formatters::Pretty.new(3)
  formatter.compact = true
  formatter.write(xml, file)
  IO.write pom.strip, file
end

options = {}
OptionParser.new do |parser|
  parser.on("--path PATH", "The path to directory") do |v|
    options[:path] = v
  end
end.parse!
target_path = options[:path]
if !target_path.nil? and Dir.exists? target_path
  poms = `find #{target_path} -name "pom.*xml" -type f`
  pom_files = []
  poms.each_line do |pom|
    next if pom.include? '/resources/'
    next if pom.include? '/test/'
    next if pom.include? '/target/'
    pom_files << File.absolute_path(pom.strip)
  end
  pom_files.each do |pom|
    puts pom
    begin
      #check pom
      transform pom
    rescue
      puts "Something bad occurred while processing \"#{pom}\""
    end
  end
end
