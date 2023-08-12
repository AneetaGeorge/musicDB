import requests
import argparse
import json
import time
from argparse import RawTextHelpFormatter

#Given a file with artist names, return a python list of artists.
def get_artist(file):
    result = []
    with open(file) as fh:
        for artist in fh:
            result.append(artist.strip())
    return result

def print_to_file(data, file):
    json_object = json.dumps(data, indent=4)
    with open(file, 'w') as outfile:
        outfile.write(json_object)

def get_data(artists, type, output):

    limit = 100

    for artist in artists:
        print("Sending requests for artist: ", artist)
        total = 0
        count = 1
        out_data = []
        while total < count:
            url = 'http://musicbrainz.org/ws/2/'+ type +'/?query=artist:' + artist + '&limit=' + str(limit) + '&offset=' + str(total)
            # print(url)
            response = requests.get(url, headers={'Accept': 'application/json'})
            try:
                data = response.json()
                count = data['count']
                data_list = []
                if type == 'artist':
                    out_data.append(data['artists'][0])  
                else:
                    if type == 'release-group':
                        data_list = data['release-groups']
                    elif type == 'release':
                        data_list = data['releases']
                    elif type == 'recording':
                        data_list = data['recordings']
                    for item in data_list:
                        out_data.append(item)
                    
                    time.sleep(1)
            except Exception as e:
                print('Error occurred : ', e)
                print(data)
                break
            
            total += limit

        print('Response size: ', len(out_data))
        print_to_file(out_data, output + '-' + artist + '.json')
        print("Finished requests for artist: ", artist)
        # break

    return out_data

def main():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('--file', default='artists', help='File with artist names')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--type', default='all', help='Type of data to be fetched from MusicBrainz.\nPossible values are:\n1. artist \n2. release-group \n3. release \n4. recording \n5. all \nDefault value: all')

    try:
        args = parser.parse_args()
        if args.file:
            artists = get_artist(args.file)

            if args.type == 'all' or args.type == 'artitst':
                if args.verbose:
                    print('Fetching artist details')

                get_data(artists, 'artist', 'output/artists.json')

                if args.verbose:
                    print('Fetched artist details')
            
            if args.type == 'all' or args.type == 'release-group':
                if args.verbose:
                    print('Fetching release group details for artists')

                get_data(artists, 'release-group', 'output/release-group.json')

                if args.verbose:
                    print('Fetched release group details for artists')
            
            if args.type == 'all' or args.type == 'release':
                if args.verbose:
                    print('Fetching release details for artists')

                get_data(artists, 'release', 'output/release.json')

                if args.verbose:
                    print('Fetched release details for artists')
            
            if args.type == 'all' or args.type == 'recording':
                if args.verbose:
                    print('Fetching recording details for artists')

                get_data(artists, 'recording', 'output/recording')

                if args.verbose:
                    print('Fetched recording details for artists')

            pass
    except argparse.ArgumentError as e:
        print(e)

if __name__ == "__main__":
    main()
