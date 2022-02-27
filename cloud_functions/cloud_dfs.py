## !/usr/bin/python3
"""
Author: BF, KC
Class: CS 467 Capstone
Project: Graphical Web Crawler
Description: Run a depth first search using BeautifulSoup starting with
a url, depth, and optional keyword
"""
import json
import random
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


class Crawler():
    """Crawler Class.

    Use BeautifulSoup to parse data from a web page.
    """

    def __init__(self, url, keyword):
        """Initialize everything to empty."""
        self.url = url
        self.keyword = keyword
        self.soup = None
        self.favicon = ''
        self.unique_links = []
        self.domain = ""
        self.title = ""

    def search_soup(self):
        """Search the soup for the keyword, return true if found."""
        check = self.soup.get_text().find(self.keyword)
        if check != -1:
            return True
        return False

    def check_url_allow_internal(self, url):
        """Check if url has a full scheme."""
        parse = urlparse(url)
        if parse.scheme == 'http' or parse.scheme == 'https':
            return True
        return False

    def create_soup(self):
        """Create the soup to be used in other methods."""
        try:
            req = requests.get(self.url)
            self.soup = BeautifulSoup(req.text, 'html.parser')
        except Exception as exception:
            print("line 55: error in create_soup(), exception: ", exception)

    def create_unique_link_list(self):
        """Create unique links.

        First add all links (determined by href in
        beautiful soup), check if they have data (some hrefs are empty), call
        check_url and then use set to remove duplicates and making that into a
        list of "good" links.
        """
        temp_list = []
        for link in self.soup.find_all('a'):
            if link is not None:
                if self.check_url_allow_internal(link.get('href')):
                    temp_list.append(link.get('href'))

        tset = set(temp_list)
        self.unique_links = list(tset)

    def get_domain(self):
        """Get the domain of a url."""
        temp = urlparse(self.url)
        self.domain = temp.netloc

    def get_favicon(self):
        """Append a favicon to the base url, does not verify there is one."""
        temp = urlparse(self.url)
        base = temp.netloc
        self.favicon = base + "/favicon.ico"

    def get_title(self):
        """Get the page title."""
        self.title = self.soup.title

    def strip_out_domain(self):
        """Strip a URL to its domain name.

        https://www.quora.com/How-do-I-extract-only-the-domain-name-from-an-URL
        """
        domain = self.url.split("//")[-1].split("/")[0]
        domain = domain.split(".")[-2]
        return domain


class Dfs():
    """Perform depth first search.

    Uses the crawler class to perform the search and return the JSON result.
    Stores nodes and edges as the search is performed, manages keyword search.
    """

    def __init__(self, url, keyword):
        """Initialize everything to empty."""
        self.nodes = []
        self.edges = []
        self.all_links = []
        self.next_link = url
        self.found_url = None
        self.keyword = keyword

    def run_crawl(self):
        """Execute a single crawl while employing an optional search."""
        crawl = Crawler(self.next_link, self.keyword)
        crawl.get_domain()
        crawl.get_favicon()
        crawl.create_soup()
        crawl.get_title()

        found = False
        # IF keyword AND if found
        if crawl.keyword is not None and crawl.search_soup() is True:
            found = True
            print("line 156: keyword found!")
            self.found_url = crawl.url

        # No Keyword OR not found
        else:
            # get unique list of links
            crawl.create_unique_link_list()
            self.all_links = crawl.unique_links

            # get the next link
            if len(crawl.unique_links) != 0:
                self.next_link = random.choice(self.all_links)
                # self.next_link = crawl.unique_links[0]

        source_edge = len(self.nodes)
        node_dict = {"url": crawl.url,
                     "domainName": crawl.strip_out_domain(),
                     "title": crawl.title.text,
                     "favicon": crawl.favicon}
        self.nodes.append(node_dict)
        target_edge = len(self.nodes)
        edge_dict = {"source": source_edge, "target": target_edge}
        self.edges.append(edge_dict)

        return found


def cloud_dfs(data_in):
    """Run dfs when an http request is sent to cloud function /DFS URL.

    It instantiates the dfs class which uses the crawler class to perform the
    search and return the JSON result. Method is wrapped in a try/except to
    help catch errors nd will return empty JSON if an exception is raised.
    Testing: Modify json input for local testing vs GCP deployement.
    """
    try:
        # j_input = json.loads(data_in)     # Testing
        j_input = data_in.get_json()      # Deployment
        keyword = None
        if j_input["keyword"] != "":
            keyword = j_input["keyword"]

        dfs = Dfs(j_input["url"], keyword)

        # Use a simple for loop to crawl to depth
        for i in range(0, j_input["depth"]):
            print("i:", i, " next_link: ", dfs.next_link)
            if dfs.run_crawl():
                break

        # Return data as json object, will be sent to a file read by front end
        export = {"nodes": dfs.nodes, "edges": dfs.edges[0:-1], "search": dfs.found_url}
        return json.dumps(export)

    except:
        # Sent empty object to alert that there was an error
        err_msg = {"ERROR: edges": [], "nodes": []}
        err_return = json.dumps(err_msg)
        return err_return


# TESTING: driver to test cloud function locally
# input_test = {"url": "https://www.target.com", "depth": 10, "keyword": ""}
# start = json.dumps(input_test)
# print("line 282 start: ", start)
# final = cloud_dfs(start)
# print("line 284", final)
# END TESTING
