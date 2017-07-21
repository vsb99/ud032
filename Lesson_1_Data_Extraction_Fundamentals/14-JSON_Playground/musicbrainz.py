#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To experiment with this code freely you will have to run this code locally.
# We have provided an example json output here for you to look at,
# but you will not be able to run any queries through our UI.
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    results = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    pretty_print(results)

    for artist_data in results['artists']:
        art_name = artist_data.get('name')
        disamb = artist_data.get('disambiguation')
        if "life-span" in artist_data:
            begin_life_span = artist_data['life-span'].get('begin', 'Not available')
        else:
            begin_life_span = 'Not available'
        print(u"Nome: {:s}, Disambiguation: {:s}, Formed in: {:s}".format(art_name,\
                                                                          disamb,\
                                                                          begin_life_span))

    # artist_id = results["artists"][1]["id"]
    # print "\nARTIST:"
    # pretty_print(results["artists"][1])

    # artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    # releases = artist_data["releases"]
    # print "\nONE RELEASE:"
    # pretty_print(releases[0], indent=2)
    # release_titles = [r["title"] for r in releases]

    # print "\nALL TITLES:"
    # for t in release_titles:
    #     print t


if __name__ == '__main__':
    main()
