#!/usr/bin/env ruby
require 'csv'
require 'optparse'
require 'ostruct'

csv_entries = []
output_header = ["full_name", "fork", "size", "stargazers_count",
                     "default_branch", "created_at", "pushed_at",
                     "ismaven", "rev"]
csv_entries << [1,2,3,4,5,6,7,8,9]

CSV.open('testando.csv', 'w') do |csv|

  csv << output_header
  csv_entries.each do |r|
    csv << r 
  end
end