Read me

#################################################################
General Information

 - Folder Description
>ES-Setup Files: Contains files needed for loading data into elastic search
>fraudEmail: input dataset and other source code for geoparser 
>Mimecraft_BigdataViz: Webpage design source code
>Zipped Files: Contains the tarred up gzipped files as required in Step5 of assignment
>faces: input dataset for ImageSpace
>featureTable_withCluster.csv: input dataset for generating_input_for_D3.ipynb jupyter notebook
>generating_input_for_D3.ipynb: jupyter notebook for generating input datasets for d3
>new_attacks.tsv: input dataset for generating_input_for_D3.ipynb jupyter notebook

#################################################################

1. generating_input_for_D3.ipynb
  - Generate inputs for d3 visualizations using data files from HW1 and HW2
      > inputs: featureTable_withCluster.csv (from HW1)
                new_attacks.tsv (from HW2)
      > Detailed descriptions are in the jupyter notebook file.
###==========================================================================
2. Running the Data Visualization Webpage (Requires “Mimecraft_BigdataViz” folder and “ES-Setup Files” folder)
	- Installation Requirements:
	  > Install ElasticSearch (https://www.elastic.co/downloads/elasticsearch)
		 - Download and unzip Elasticsearch
		 - Run bin/elasticsearch (or bin\elasticsearch.bat on Windows)
		 - To verify go to “http://localhost:9200” and check if it works fine
	  > Install Logstash (https://www.elastic.co/downloads/logstash)
		 - Download and unzip Logstash

	- PreRequisite: Load data into ElasticSearch index using below steps:
	  > Start elastic search by running bin/elasticsearch (or bin\elasticsearch.bat on Windows)
	  > Edit path (path_to_folder as shown below) variable in logstash.conf file to direct to your system specific path
		path => "C:/path_to_folder/ES-SetupFiles/*.csv"
	  > In a separate cmd execute
		cd to folder ES-SetupFiles 
		execute “C:\path_to_folder\logstash-7.12.0\bin\logstash -f logstash.conf”
	  > Your elastic search index is now ready and loaded onto piechart_es
	  > You can verify by visiting: http://localhost:9200/piechart_es

	- Steps:
	  1. Disable CORS for chrome using methods from    
		  https://alfilatov.com/posts/run-chrome-without-cors/ 
	  2. Run ElasticSearch by running bin/elasticsearch (or bin\elasticsearch.bat on Windows)
	  3. In folder “Mimecraft_BigdataViz”, run the index file (base webpage)
	  4. Click on “Explore Visualization” tab to view the dashboard

3. Elasticsearch Index:
	- Pre-requisite: Install npm (https://www.npmjs.com/get-npm)
	- Download the git https://github.com/elasticsearch-dump/elasticsearch-dump
	- In a cmd window execute
	(local)
	 npm install elasticdump
	 ./bin/elasticdump
	OR (global)
	 npm install elasticdump -g
	 elasticdump
	- Now Execute below commands for obtaining mapping file
		> “elasticdump --input=http://127.0.0.1:9200/piechart_es  --output=/data/piechart_es_mapping.json --type mapping”
	- Now Execute below commands for obtaining data file
		> “elasticdump --input=http://127.0.0.1:9200/piechart_es  --output=/data/piechart_es_data.json --type data”
	- Save output json files in separate folders named “piechart_es_data” and “piechart_es_mapping”
	- Now Execute below for tarring
		> tar -zcvf piechart_es_mapping.tar.gz piechart_es_mapping
		> tar -zcvf piechart_es_data.tar.gz piechart_es_data

###==========================================================================
4. Geo-Parser
	  1. download the git
		  > git clone https://github.com/nasa-jpl-memex/GeoParser.git
	  2. move to Docker folder from GeoParser
		  > cd GeoParser\Docker
	  3. Install GeoParser using Docker
		  > docker pull nasajplmemex/geo-parser
		  > docker-compose up -d
	  4. visit the browser using http://localhost:8000
	  5. go to "fraudEmail" folder which we submitted and run below codes
		  > cd $HOME/fraudEmail
		  > ./create-core.sh (or try sh create-core.sh)
		  > ./add-fields.sh (or try sh add-fields.sh)
	  6. open jupyter notebook and run Ingest fraudEmail data.ipynb
	  7. go back to geoParser (http://localhost:8000)
	  8. click on “Configure Index” Tab
		- set Domain Name as "emailcontents"
		- set Indexed Engine Path as "http://localhost:8983/solr/emailcontents/
		- click on "Add Index"
	  9. click on "Add/View Index" tab
		- select the Domain name and Indexed Engine Path
		- click on "View"
		- click on "Geoparse"
5. To get index files of Geo-Parser:
	  1. In desktop docker, open CLI of container, docker_memex-geoparser_1, and go to folder at: /home/Solr/solr-5.3.1/server/solr; tar imagespace folder by “tar -zcvf emailcontents.tar.gz emailcontents”.
	  2. Transfer the tar file from docker to local by “docker cp docker_memex-geoparser_1:/home/Solr/solr-5.3.1/server/solr/emailcontents.tar.gz .”

###==========================================================================
6. Image Space (using MacOS)
	  1. “git clone https://github.com/nasa-jpl-memex/image_space.git”
	  2. Put ingested image folder inside the same directory as above folder (In our case, it’s named as faces; please unzip the file named faces.zip to use)
	  3. Open docker and run (please replace “/Users/lilythegirl/Documents/image_space-master” and “/Users/lilythegirl/Documents/image_space-master/faces” with your local path):
		 a. “cd /Users/lilythegirl/Documents/image_space-master/imagespace_smqtk && ./smqtk_services.run_images.sh --docker-network deploy_imagespace-network --images /Users/lilythegirl/Documents/image_space-master/faces”
		 b. “cd /Users/lilythegirl/Documents/image_space-master/scripts/deploy && IMAGE_DIR=/Users/lilythegirl/Documents/image_space-master/faces docker-compose up -d”
		 c. “cd /Users/lilythegirl/Documents/image_space-master/scripts/deploy && sh ./imagespace/enable-imagespace.sh”
		 d. Run “./solr/import-images.sh deploy_imagespace-solr_1 imagespace /Users/lilythegirl/Documents/image_space-master/faces” to make solr start to write index files. 
7. To get index files:
	  4. In desktop docker, open CLI of container, deploy_imagespace-solr_1, and go to folder at: /server/solr/mycores; tar imagespace folder by “tar -zcvf imagespace.tar.gz ./imagespace”.
	  5. Transfer the tar file from docker to local by “docker cp deploy_imagespace-solr_1:/opt/solr/server/solr/mycores/imagespace.tar.gz .”

###==========================================================================
ZippedFiles Folder:
  - piechart_es_mapping.tar.gz : This is the gzipped elasticsearch index mapping file
  - piechart_es_data.tar.gz : This is the gzipped elasticsearch index data file
  - imagespace.tar.gz : This is the gzipped imagespace solr searching index 
  - emailcontents.tar.gz : This is the gzipped geo-parser solr searching index 
