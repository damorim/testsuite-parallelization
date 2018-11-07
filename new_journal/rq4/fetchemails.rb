#!/usr/bin/env ruby
projects = Dir.glob "#{options.path}/*"
folders = projects.select {|f| File.directory? f}
folders.sort!

puts "folder#{COLSEP}project#{COLSEP}url#{COLSEP}email#{COLSEP}name"
folders.each do |folder|
  raw = `cd #{folder} && git log --pretty=format:"%ae;%an"`
  url = `cd #{folder} && cat .git/config | grep 'url =' | awk '{print $3}'`        
  emails = []
  persons = []
  project_name = url.strip.split('/').last
  raw.each_line do |line|
    csv = line.strip
    csv = csv.split ';'
    if not emails.include? csv[0]
      emails << csv[0]
      persons << OpenStruct.new(email: csv[0].strip, name: csv[1].strip)
    end
  end

  persons.uniq.each do |email|
    puts "#{File.basename folder}#{COLSEP}#{project_name}#{COLSEP}#{url.strip}#{COLSEP}#{email.email}#{COLSEP}#{email.name}"
  end
end

