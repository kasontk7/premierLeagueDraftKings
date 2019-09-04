from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from operator import itemgetter

num_matches = 10

weblink = "https://www.oddsportal.com/soccer/england/premier-league/"
options = Options()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
browser.get(weblink)
matchups = browser.find_element_by_xpath("//*[@id=\"tournamentTable\"]/tbody")
match = matchups.find_elements_by_xpath("*")
match_links = []
for elt in match[3:num_matches+3]:
    table_tag = elt.find_element_by_css_selector("td.name.table-participant")
    href_tag = table_tag.find_element_by_tag_name("a")
    match_links.append(href_tag.get_attribute("href"))
    
for link in match_links:
    browser.get(link+"#cs;2")
    page_content = browser.find_element_by_xpath("//*[@id=\"col-content\"]")
    matchup = page_content.find_element_by_tag_name("h1")
    table = browser.find_element_by_xpath("//*[@id=\"odds-data-table\"]")
    scores = table.find_elements_by_xpath("*")
    scores_list = []
    for score in scores:
        if score.get_attribute("class") == "table-container":
            div = score.find_element_by_tag_name("div")
            strong = div.find_element_by_tag_name("strong")
            num_ops = div.find_element_by_css_selector("span.odds-cnt")
            num_ops = num_ops.text
            if num_ops:
	            num_ops = float(num_ops.strip("(").strip(")"))
	            if num_ops > 0:
		            span = div.find_element_by_css_selector("span.avg.nowrp")
		            exact = strong.find_element_by_tag_name("a")
		            odds = span.find_element_by_tag_name("a")
		            bet = []
		            bet.append(int(odds.text.strip('+')))
		            bet.append(exact.text)
		            scores_list.append(bet)
    sorted_scores = sorted(scores_list, key=itemgetter(0))
    best3 = sorted_scores[0:3]
    print(matchup.text)
    for elt in best3:
	    lowest_odds = '+' + str(elt[0])
	    score_pred = elt[1]
	    print(score_pred + ": " + lowest_odds)


