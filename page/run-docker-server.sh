#!/bin/bash
docker run -dit --name my-apache-app -v "$PWD":/usr/local/apache2/htdocs/ -p "8080:80" httpd:2.4
