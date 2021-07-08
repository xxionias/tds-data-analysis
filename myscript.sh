#!/bin/bash

_now=$(date +"%m_%d_%Y")
_firstfile="./raw_data/articles/article_$_now.json"
_firstoutput="./raw_data/articles/article_command_output_$_now.txt"
_secondfile="./raw_data/users/profile_$_now.json"
_secondoutput="./raw_data/users/profile_command_output_$_now.txt"
_bucket_name=$(date +"%m-%d-%Y")

# Add a spinner display
spinner()
{
    local pid=$!
    local delay=0.75
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

_start_1=$(date +%s)
# Both the standard output and standard error stream will be redirected to the
# file only, nothing will be visible in the terminal. If the file already exists,
# it gets overwritten.
echo "Running first spider and writing output to $_firstoutput..."
(scrapy crawl article -O "$_firstfile" &> "$_firstoutput") & spinner
printf "First scraping task succeeded!\n"
_duration_1=$(echo "$(date +%s) - $_start_1" | bc)
_execution_time_1=`printf "%.2f seconds" $_duration_1`
echo "First task execution time: $_execution_time_1"

_start_2=$(date +%s)
echo "Running second spider and writing output to $_secondfile..."
(scrapy crawl profile -O "$_secondfile" &> "$_secondoutput") & spinner
printf "Second scraping task succeeded!\n"
_duration_2=$(echo "$(date +%s) - $_start_2" | bc)
_execution_time_2=`printf "%.2f seconds" $_duration_2`
echo "Second task execution time: $_execution_time_2"

_start_3=$(date +%s)
echo "Uploading files to S3 bucket $_bucket_name..."
(python upload.py) & spinner
printf "Uploading task succeeded!\n"
_duration_3=$(echo "$(date +%s) - $_start_3" | bc)
_execution_time_3=`printf "%.2f seconds" $_duration_3`
echo "Uploading execution time: $_execution_time_3"

_duration_total=$(echo "$(date +%s) - $_start_1" | bc)
_execution_time_total=`printf "%.2f seconds" $_duration_total`
echo "Total execution time: $_execution_time_total"
