Notes taken from:


Process Overview:
- Pull in URL from our "To-Crawl" list
- check if we have already crawled it
- check if crawling it is compliant with its host's robots.txt file.(Example mentioned is Wikipedia)
- get the IP address of the host via DNS 
- make an HTTP request to load the contents  of the site
- check if we have already processed a different URL with identical content
- parse the content
- store the results somewhere
- adding any referenced URLs to our "To-Crawl" list
Fetching URL to crawl
- Can we reduce networking calls on the frontier?
problems to solve:
- Avoid Duplicate fetches
- 
