# Web Crawler Visualizer

This project allows a user to enter a starting point for the program and visually see a web crawling
program in action. The simulation will give the end user basic insight on how a web crawler, such as a
Googlebot, might visit pages on the Surface Web in a real life scenario. The user will ultimately view a
high level map of all the pages that were visited by the web crawler, in an organized, coherent way.


## Getting Started
This program was developed using Angular and the D3 Javascript library on the front end, Node.js on the back end and Python for crawling the web. This application has been optimized for use on the Google Cloud Platform and with the use of Google Cloud Functions. The index.js file is currently set to use existing Google Cloud Functions for the appropriate search. To implement any changes with the search functions would require creating their own Google Account and to Create their own Functions and replace the URL(s) in index.js.

### Requirements
- [Angular.js](https://angular.io/)

- [Node.js](https://nodejs.org/)
  - Express
  - Body-Parser
  - CORS
  - D3
  - Path
- [Python 3.5](https://www.python.org/)
  - Beautiful Soup 4
  - lxml
  - numpy

## Usage

### Full Deployment
1. Enter a starting URL for the web crawler to start.
2. Choose the depth of the crawl.
3. Choose either Breadth First Search or Depth First Search.
4. Click Crawl!
5. Look at the visualization, hover over nodes for URL tooltip
6. Repeat steps 1 - 5 (currently showing the static data)

**Example Graph**

<img width="661" alt="sample_graph" src="https://github.com/quantumscript/crawler-visualization/assets/60626826/b567e03a-4e65-49e7-9230-5b7309615769">


### Crawler Only
**Testing Python**
The separeate search functions are composed of individual Python files. The entire file is designed to be used a Google Cloud Function. However they can still be tested locally by first installing these libraries:
```shell
$pip install beautifulsoup
$pip install python3-lxml
```

**Testing  Functions**
Both Breadth First and Depth First Search functions can be easily tested locally. After installing the libraries and downloading the files, one can create a "main" to call the appropriate function and check the results:

```python
out = {"url": "https://en.wikipedia.org/wiki/Macaroni_penguin", "depth": 23, "keyword": "twitter"}
expo = json.dumps(out)
final = cloud_dfs(expo)
print(final)
```
Depending on Python environment, one may need to switch how the function parses the JSON input:
```python
#j_input = input.get_json() #use on cloud function
j_input = json.loads(input) #use on local development
```

Result will be a list of Nodes and Edges as in sample below.

**Sample json Output**
```json
{
    "nodes": [{
        "url": "https://www.google.com/",
        "domainName": "google",
        "title": "Google",
        "favicon": "https://www.google.com/s2/favicons?domain=www.google.com"
    }, {
        "url": "https://www.wikipedia.org/",
        "domainName": "wikipedia",
        "title": "wikipedia",
        "favicon": "https://en.wikipedia.org/favicon.ico"
    }, {
        "url": "https://twitter.com/",
        "domainName": "twitter",
        "title": "Twitter",
        "favicon": "https://twitter.com/"
    }],
    "edges": [{
        "source": 0,
        "target": 1
    }, {
        "source": 2,
        "target": 0
    }]
}
```

