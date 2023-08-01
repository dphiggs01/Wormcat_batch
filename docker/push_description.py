#!/usr/bin/env python

import os
import json
import requests
import argparse

def get_token(username):
    retval = None
    password = os.getenv('DOCKERHUB_API_TOKEN')

    url = f"https://hub.docker.com/v2/users/login"
    headers = {
            "Content-Type": "application/json"
        }
    
    body = {
            "username": username,
            "password": password
        }
    
    # print(f"{url=}")
    # print(f"{headers}")
    # print(f"{json.dumps(body)=}")
    response = requests.post(url, data=json.dumps(body), headers=headers)
    if response.status_code >= 200 and response.status_code < 300:
        response_json = response.json()
        retval = response_json['token']
    else:
        response.raise_for_status() 

    return retval

def update_image_description(image, readme, token, short_desc=None):
    readme_content = open(readme).read()
    data = {
        "registry": "registry-1.docker.io",
        "full_description": readme_content
    }

    if short_desc:
        data['description']=short_desc

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"JWT {token}"
    }
    url = f"https://hub.docker.com/v2/repositories/{image}/"

    
    response = requests.patch(url, data=json.dumps(data), headers=headers)
    if response.status_code >= 200 and response.status_code < 300:
        print(f"Description updated {response.status_code}")
    else:
        response.raise_for_status() 

    return response.status_code

def main():
     print("Push Dockerhub description")
     parser = argparse.ArgumentParser()
     help_statement="push_description.py --username <dockerhub username> --image <docker image name> --readme <path to readme description> --short_desc <Short description (<=100 Chars)>"
     parser.add_argument('-u', '--username', help='Dockerhub username')
     parser.add_argument('-i', '--image', help='Docker image name')
     parser.add_argument('-r', '--readme', help='Path to readme file')
     parser.add_argument('-s', '--short_desc',  required=False, help='Short description (<=100 Chars)')
     args = parser.parse_args()
     
     if not args.username:
        print(help_statement)
        print("Dockerhub username is missing.")
        return

     if not args.image:
        print(help_statement)
        print("Docker image name is missing.")
        return

     if not args.readme:
        print(help_statement)
        print("Path to readme file is missing.")
        return
     
     if args.short_desc and len(args.short_desc) >100:
        print(help_statement)
        print("Short description limit 100 Charactes exceeded.")
        return
     
     token = get_token(args.username)
     update_image_description(args.image, args.readme, token, args.short_desc)

if __name__ == "__main__":
    main()