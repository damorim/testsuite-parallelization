def get_nice_variables variables
  filtered = {}
  variables.each do |k, v|
    if k.downcase.include? 'thread'
      filtered[k] = v
    end
    if k.downcase.include? 'parallel'
      filtered[k] = v
    end
    if k.downcase.include? 'fork'
      filtered[k] = v
    end
  end
  filtered = handle_values(filtered)
  get_parallel_level filtered
end

def handle_values variables
  v = variables.clone
  v['parallel'] = 'none' unless variables.has_key? 'parallel'
  v['perCoreThreadCount'] = 'true' unless variables.has_key? 'perCoreThreadCount'
  v['threadCount'] = '0' unless variables.has_key? 'threadCount'
  v['threadCountClasses'] = '0' unless variables.has_key? 'threadCountClasses'
  v['threadCountMethods'] = '0' unless variables.has_key? 'threadCountMethods'
  v['threadCountSuites'] = '0' unless variables.has_key? 'threadCountSuites'
  v['parallelOptimized'] = 'true' unless variables.has_key? 'parallelOptimized'
  v['forkCount'] = '0' unless variables.has_key? 'forkCount'
  return v
end

def is_test_parallel? variables
  return true if variables['forkCount'].downcase.include? 'c' or variables['forkCount'].to_i > 1
  return true if variables['parallel'] != 'none'
  return false
end


def is_valid? entry
  return true if entry['timecost_group'] != 'short' and entry['below_threshold'] == 'T'
  return false
end


def get_parallel_level variables
  parallel = variables['parallel'].downcase
  if variables['forkCount'].downcase.include? 'c' or variables['forkCount'].to_i > 1
    ['all', 'both', 'methods'].each do |method|
      return 'FC1' if parallel.include?(method) or parallel.eql?(method)
    end
    return 'FC0'
  else
    is_class_parallel = false
    ['suites', 'all', 'both', 'classes'].each do |method|
      if parallel.include?(method) or parallel.eql?(method)
        is_class_parallel = true
        break
      end
    end
    if is_class_parallel
      is_methods_parallel = false
      ['all', 'both', 'methods'].each do |method|
        if parallel.include?(method) or parallel.eql?(method)
          is_methods_parallel = true
          break
        end
      end
      return 'C3' if is_methods_parallel
      return 'C2'
    else
      return 'C1' if parallel.include? 'method'
      return 'C0' if parallel == 'none'
    end
  end
  "X"
end


def create_csv_entry row, configs, entries
  configs.each do |k, v|
    v.each do |mod|
      if k != 'C0'
        entries << [row['name'], mod, k]
      end
    end
  end
end


def create_table_entry row, configs, entries
  total = 0
  configs.each do |k, v|
    total += v.length
  end
  configs.each do |k, v|
    if v.length > 0 and k != 'C0'
      entries << '%s & %s & %d/%d & %s' % [row['timecost_group'], row['name'], v.length, total, k]
    end
  end
end

