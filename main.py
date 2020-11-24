'''
Author : Sharath.Aradhyamath
Description: Script to update the push the tag/commitid to staging branch.
Related To : CICD Spinnaker
'''
import argparse
import logging
import os

import ruamel.yaml

STAGING_BRANCH = "staging"

tag_records = {
    "Consumer": ["api", "celery"]
}

def parse_file(file_name):
    '''
    Parse YAML file
    :param file_name:
    :return:
    '''
    try:
        parsed_data = ruamel.yaml.load(open(file_name), Loader=ruamel.yaml.RoundTripLoader, preserve_quotes=True)
    except Exception as err:
        logging.exception(f"Unable to parse yaml file : {file_name}, ERROR : {err}")
    return parsed_data

def update_tag_for_consumer(parsed_yaml_file, tag, application_name, filename):
    '''
    Updates tag value
    :param parsed_yaml_file:
    :param tag:
    :param application_name:
    :param filename:
    :return:
    '''
    for application in tag_records[application_name.capitalize()]:
        logging.info(f"Updating [{application_name.capitalize()}][{application}]")
        try:
            parsed_yaml_file['Service'][application_name.capitalize()]['deploy'][application][application_name]['image']['tag'] = tag
        except Exception as err:
            logging.exception(f"unable to update the tag {tag} in file {filename} : ERROR {err}")
    return parsed_yaml_file


if __name__ == '__main__':
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

    parser = argparse.ArgumentParser(description="To modify tag and update the repo")
    parser.add_argument("--filename", type=str, help="pass the path of the file")
    parser.add_argument("--application", type=str, help="application to modify. Allowed keywords. (consumer, fleet, iot)")
    parser.add_argument("--tag", type=str, help="tag/commitID")
    parser.add_argument("--environment", type=str, help="environment. ie. staging, production")

    args = parser.parse_args()
    print(f"FileName : {args.filename}\n"
          f"Application : {args.application}\n"
          f"Environment : {args.environment}\n"
          f"Tag : {args.tag}\n")

    #Parse Yaml file
    parsed_yaml_file = parse_file(args.filename)

    #update the flag
    updated_yaml_data = update_tag_for_consumer(parsed_yaml_file, args.tag, args.application, args.filename)

    #write back the content
    with open(args.filename, 'w') as writer:
        try:
            ruamel.yaml.dump(updated_yaml_data, writer, Dumper=ruamel.yaml.RoundTripDumper)
        except Exception as err:
            logging.exception(f"Unable to write the content to {args.filename}")
