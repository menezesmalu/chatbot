### How to setup Elasticsearch
First you need to get a container up and running. For that, use: 

```
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.14.0
```

If everything went ok, you must have Elasticsearch running in `localhost:9200`. Then you can execute the `indexer.ipynb` file (that's the only notebook that should be executed). It will get the json file exported by the `scrapper.ipynb`file (already done), create the `movies_index` and index all the documents. 



### How data was collected

The data was scrapped from the [Movie Stack Exchange](https://movies.stackexchange.com/) website using BeautifulSoup and Selenium libraries in Python. Iniitally, we grabbed the questions in the most voted questions. We got 426 questions: The question itself and the reference to the answers page. Then we iterated through thoses pages and saved the answers in memory. The collected data was then exported to a json file `result.json`. 

### How data was indexed

The set up an Elastisearch environment with Docker and created a single index `movies_index` and sent all the collected data to that index. 




