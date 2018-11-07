require 'mail'
require 'erb'
require 'ostruct'
require 'csv'
require 'optparse'
require 'yaml'
require 'parallel'

def send_mail options, project
    mail = Mail.new(
        from:    options.me.email,
        to:       project.person.email,
        subject:  project.subject,
        body:     project.body,
        cc:       options.email_settings['cc'],
    )
    result = mail.deliver!
    puts result.action
end

options = OpenStruct.new
OptionParser.new do |opts|
    opts.banner = "Usage: email_sender.rb [options]"

    opts.on('-s', '--settings [FILE]', String, 'Path to the settings.yml') do |path|
        options.email_settings = YAML.load_file path
        options.me = OpenStruct.new
        options.me.name = options.email_settings['name']
        options.me.email = options.email_settings['email']
        options.me.description = options.email_settings['description']
        mail_opt = { :address             => "smtp.gmail.com",
                    :port                 => 587,
                    :user_name            => options.email_settings['email'],
                    :password             => options.email_settings['password'],
                    :authentication       => 'plain',
                    :enable_starttls_auto => true  }
        Mail.defaults do
            delivery_method :smtp, mail_opt
	    retriever_method :pop3, :address    => "pop.gmail.com",
                          	    :port       => 995,
                                    :user_name  => options.email_settings['email'],
                          :password   => options.email_settings['password'],
                          :enable_ssl => true
        end
    end

    opts.on('-t', '--template [FILE]', String, 'Path to the template') do |path|
        options.template = ERB.new IO.read(path)
    end

    opts.on('-c', '--subjects-csv [FILE]', String, 'Path to the subjects CSV file') do |path|
        text = IO.read path
        options.subjects = CSV.parse text, {headers: true}
    end

    opts.on('-v', '--verbose', 'Enter in verbose mode') do |verbose|
        options.verbose = verbose
    end

    opts.on('-d', '--debug', 'Enter in debug mode') do |debug|
        options.debug = debug
    end
    
    opts.on('-l', '--download-to-local', 'Download recent emails') do |download|
	options.download = download
    end

end.parse!


if options.download
	
	mails = Mail.find(:what => :last, :count => 300,:order => :asc)
	nice_emails = []
	mails.each do |mail|
		puts mail.subject
		nice_emails << mail if mail.subject.include? 'parallel'
	end
	#`rm -r ~/home/lhsm/Documentos/Research/parallel-test/eval/rawdata/emails/*`
	nice_emails.each do |mail|
		text = "Subject: #{mail.subject}"
		project = mail.subject.split ':'
		project = project.last.strip
		text << "Project: #{project}"
		text << "From: #{mail.sender.address}"
		text << "==body=="
		text << mail.body.decoded
		puts text
	end

	exit 1
end

options.subjects.each do |subject|

    person = OpenStruct.new
    person.name = subject['name']
    person.email = subject['email']
    project = OpenStruct.new
    project.name = subject['project']
    project.url = subject['url']
    person.project = project

    bindings = OpenStruct.new person: person, me: options.me
    o_binding = bindings.instance_eval { binding }
    body = options.template.result o_binding

    project = OpenStruct.new
    project.body = body
    project.subject = ERB.new(options.email_settings['subject']).result o_binding
    project.person = person

    puts "Sending email to: #{person.email}" if options.debug or options.verbose
    puts "From: #{options.me.email}" if options.debug or options.verbose
    puts "Subject: #{project.subject}"  if options.debug or options.verbose
    puts "Cc: #{options.email_settings['cc'].join ', '}"  if options.debug or options.verbose
    puts "Body: #{project.body}" if options.debug

    send_mail options, project if not options.debug
end
