import os
import json
import pprint
import subprocess
from datetime import datetime
import io

pp = pprint.PrettyPrinter(indent=4)

def clean_files(file_directories): # clears existing data in a file and creates it if it doesn't exist
    for file in file_directories:
        open(file, 'w').close()

def run(config):
    # 0. define temp files
    # temp_catalog = os.path.abspath(os.path.join(os.path.dirname(__file__), "temp_catalog.json"))
    # temp_e3 = os.path.abspath(os.path.join(os.path.dirname(__file__), "temp_e3.json"))
    # temp_ratings_raw = os.path.abspath(os.path.join(os.path.dirname(__file__), "temp_ratings_raw.json"))
    # temp_ratings = os.path.abspath(os.path.join(os.path.dirname(__file__), "temp_ratings.json"))
    lsf_data = os.path.abspath(os.path.join(os.path.dirname(__file__), config['scraped_lsf_data_directory']))
    lsf_data_post_processed = os.path.abspath(os.path.join(os.path.dirname(__file__), config['post_processed_lsf_data_directory']))
    vdb_data = os.path.abspath(os.path.join(os.path.dirname(__file__), config['scraped_vdb_data_directory']))
    vdb_data_post_processed = os.path.abspath(os.path.join(os.path.dirname(__file__), config['post_processed_vdb_data_directory']))

    merged_data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), config['merged_data_directory']))
    merge_data_post_processing_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), config['merge_data_post_processing_directory']))

    clean_files([lsf_data, lsf_data_post_processed, vdb_data, vdb_data_post_processed, merged_data_directory])

    lsf_scraper_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), config['lsf_scraper_directory']))
    vdb_scraper_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), config['vdb_scraper_directory']))

    lsf_post_processing_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), config['lsf_post_processing']))
    vdb_post_processing_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), config['vdb_post_processing']))

    upload_orm_data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), config['upload_orm_data']))

    # 1. run both scrapers: lsf_scraper for LSF data and vdb_scraper for Vorlesungsdatenbank data
    os.chdir(lsf_scraper_directory)
    subprocess.call(f"scrapy crawl main -o lecture_results.json", shell=True)

    os.chdir(vdb_scraper_directory)
    subprocess.call(f"scrapy crawl vdb-scraper -o description_results.json", shell=True)

    # 2a. post-process and save the insight data
    # os.chdir(os.path.join(config["courseScraper"], "course_catalog", "post_processing"))
    # subprocess.call(f"python process_data.py {temp_catalog} {config['courseInsightsTargetFile']}", shell=True)
    os.chdir(lsf_post_processing_directory)
    subprocess.call(f"python process_data.py", shell=True)

    os.chdir(vdb_post_processing_directory)
    subprocess.call(f"python process_data.py", shell=True)

    os.chdir(merge_data_post_processing_directory)
    subprocess.call(f"python merge_lsf_and_vdb.py", shell=True)

    os.chdir(upload_orm_data_directory)
    subprocess.call(f"python upload_orm_data.py", shell=True)

    # 2b. post-process and save the ratings data
    # os.chdir(os.path.join(config["ratingsScraper"], "course_ratings", "post_processing"))
    # subprocess.call(f"python derive_attributes.py {temp_ratings_raw} {temp_ratings}", shell=True)

    # 3. load the data from the temp files
    # with open(temp_e3, encoding='utf-8') as file:
    #     e3_courses = json.load(file)
    #
    # with open(temp_ratings, encoding='utf-8') as file:
    #     ratings = json.load(file)

    # 4. process e3 data & ratings, write to target files
    # e3_processed, avg_ratings = process_e3(e3_courses, ratings)

    # with open(config["e3TargetFile"], "w") as file:
    #     file.write(json.dumps(e3_processed))
    #
    # with open(config["e3RatingsFile"], "w") as file:
    #     file.write(json.dumps(avg_ratings))
    #
    # # 5. remove temp files
    # os.remove(temp_catalog)
    # os.remove(temp_e3)
    # os.remove(temp_ratings)
    # os.remove(temp_ratings_raw)

    # 6. update statusMessage in config
    # config["statusMessage"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    # with open(os.path.join(os.path.dirname(__file__), "config.yaml"), "w") as file:
    #     file.write(yaml.dump(config))

if __name__ == "__main__":
    # with open("config.yaml", "r") as file:
    #     config = file.read()
    # config = yaml.safe_load(config)
    #
    # run(config, "https://campus.uni-due.de/lsf/rds?state=wtree&search=1&trex=step&root120211=280741%7C276367&P.vx=kurz",
    # "https://campus.uni-due.de/lsf/rds?state=wtree&search=1&trex=step&root120211=280741%7C276221%7C276682&P.vx=kurz")

    with io.open('config.json', 'r') as config_file:
        config_json = json.load(config_file)
        run(config_json)
        config_file.close()