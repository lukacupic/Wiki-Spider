from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from random import randint

base_url = "https://en.wikipedia.org"
max_hops = 25
visited = []


# Returns a URL representing Spider's next hop
def get_next_url(url):
    req = Request(url)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, "lxml")

    links = []
    for link in soup.findAll('a'):
        href = str(link.get('href'))

        if href.startswith("/wiki/") and not ":" in href:
            current_url = base_url + href
            if not current_url in links:
                links.append(base_url + href)

    links = [n for n in links if n not in visited]
    return links[randint(0, len(links) - 1)]


def main():
    input_phrase = input("Enter a phrase to find: ")

    current_url = ""
    found_url = ""

    count = 1
    while count < max_hops:
        if count == 1:
            current_url = base_url + "/wiki/Special:Random"
        else:
            current_url = get_next_url(current_url)

        req = Request(current_url)
        html_page = urlopen(req)
        soup = BeautifulSoup(html_page, "lxml")

        current_url = html_page.geturl()

        print("Searching " + current_url)

        found = input_phrase.lower() in soup.text.lower()
        if found:
            found_url = current_url
            break

        count+=1

    if count >= max_hops:
        print("The spider got tired with hopping and couldn't locate the phrase :(")
    else:
        print("The spider has found the phrase '" + input_phrase + "' on " + found_url + " in " + str(count) + " hop(s).")


main()
