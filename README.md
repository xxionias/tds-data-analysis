`tds/spiders/article_spider.py`: web scraper for articles  
`tds/spiders/user_spider.py`: web scraper for authors' profiles  
`myscript.sh`: perform web scraping tasks and store outputs in corresponding S3 bucket  
`raw_data`: each subfolder consists web scraped output files and std.err outputs generated    
`etl.ipynb`: procedures to process raw data and output `cleaned_data`  
`cleaned_data`: output of `etl.ipynb`  
`etl.py`: read and process `cleaned_data` to Postgres DB  
`sql_queries.py`: contains sql queries for dropping and creating tables. Also contains insertion query template  
`create_tables.py`: contains code for setting up database
`app.py`: web app
