import requests
import argparse
import json
import time

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
    out_data = []
    for artist in artists:
        response = requests.get('http://musicbrainz.org/ws/2/'+ type +'/?query=artist:' + artist, headers={'Accept': 'application/json'})
        
        try:
            data = response.json()
            data_list = []
            # print(data)
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
                time.sleep(30)
        except Exception as e:
            print('Error occurred : ', e)
            print(data)
            break
        # break
    
    print_to_file(out_data, output)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='artists', help='File with artist names')
    parser.add_argument('--verbose', action='store_true', help='enable verbose output')

    try:
        args = parser.parse_args()
        if args.file:
            artists = get_artist(args.file)

            if args.verbose:
                print('Parsed artists: ', artists)

            # get_data(artists, 'artist', 'output/artists.json')
            # get_data(artists, 'release-group', 'output/release-group.json')
            get_data(artists, 'release', 'output/release.json')
            get_data(artists, 'recording', 'output/recording.json')

            pass
    except argparse.ArgumentError as e:
        print(e)

if __name__ == "__main__":
    main()
