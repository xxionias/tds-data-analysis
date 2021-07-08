import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_users_file(cur, filepath):
    """
    Process users files and insert entries into the Postgres database.
    :param cur: cursor reference
    :param filepath: complete file path for the file to load
    """

    # open file
    df = pd.read_csv(filepath)

    # Insert entries
    for value in df.values:
        user_id, author, linkOfAuthorProfile, desc, followers = value
        users_data = (user_id, author, linkOfAuthorProfile, desc, followers)
        cur.execute(users_table_insert, users_data)

    print(f"Users entries inserted for file {filepath}")


def process_articles_file(cur, filepath):
    """
    Process articles files and insert entries into the Postgres database.
    :param cur: cursor reference
    :param filepath: complete file path for the file to load
    """
    # Open file
    df = pd.read_csv(filepath)

    # Insert entries
    for value in df.values:
        articletitle, articleLink, postingTime, minToRead, recommendations, responses, user_id = value
        articles_data = (articletitle, articleLink, user_id, postingTime, minToRead, recommendations, responses)
        cur.execute(articles_table_insert, articles_data)


def process_data(cur, conn, filepath, func):
    """
    Driver function to load data from articles and users files into Postgres database.
    :param cur: a database cursor reference
    :param conn: database connection reference
    :param filepath: parent directory where the files exists
    :param func: function to call
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.csv'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Driver function for loading articles and users data into Postgres database
    """
    conn = psycopg2.connect("host='localhost' dbname='tds' user='user0' password='7248'")
    cur = conn.cursor()

    process_data(cur, conn, filepath='cleaned_data/users/', func=process_users_file)
    process_data(cur, conn, filepath='cleaned_data/articles/', func=process_articles_file)

    conn.close()


if __name__ == "__main__":
    main()
    print("\n\nFinished processing!!!\n\n")
