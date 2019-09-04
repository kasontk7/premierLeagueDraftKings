from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import io
import csv
from operator import itemgetter

score_likelihood = []
cs_likelihood = []

def add_spaces(f_str, num_spaces):
    while len(f_str) != num_spaces:
        f_str += " "
    return f_str
def print_game(home, away):
    game_string = home + " vs. " + away
    print(game_string)
    separator = ""
    for i in game_string:
        separator += "-"
    print(separator)

def get_cs(browser, link):
    results = []
    browser.get(link)
    yes_cs = browser.find_element_by_xpath("//*[@id=\"t1\"]/tr[2]")
    no_cs = browser.find_element_by_xpath("//*[@id=\"t1\"]/tr[1]")
    results.append(yes_cs.get_attribute("data-best-dig"))
    results.append(no_cs.get_attribute("data-best-dig"))
    return results

def update_lists(home, away, home_link, away_link, browser):
    home_cs = get_cs(browser, home_link)
    away_cs = get_cs(browser, away_link)
    # print(home + " Clean Sheet:")
    # print("Yes: " + home_cs[0] + " No: " + home_cs[1])
    # print(away + " Clean Sheet:")
    # print("Yes: " + away_cs[0] + " No: " + away_cs[1])
    home_score_entry = [float(away_cs[1]), home]
    away_score_entry = [float(home_cs[1]), away]
    home_cs_entry = [float(home_cs[0]), home]
    away_cs_entry = [float(away_cs[0]), away]
    score_likelihood.append(home_score_entry)
    cs_likelihood.append(home_cs_entry)
    score_likelihood.append(away_score_entry)
    cs_likelihood.append(away_cs_entry)


weblink = "https://www.oddschecker.com/football/english/premier-league/"
options = Options()
options.add_argument("--headless")
browser = webdriver.Chrome(options=options)
f = io.open("matchups.csv", "r", encoding='utf-8-sig')
reader = csv.reader(f, delimiter=',')
for row in reader:
    home = row[0]
    away = row[1]
    # print_game(home, away)
    homef = home.lower().replace(" ", "-")
    awayf = away.lower().replace(" ", "-")
    match_link = weblink + homef + "-v-" + awayf
    home_clean_sheet_link = match_link + "/away-team-to-score"
    away_clean_sheet_link = match_link + "/home-team-to-score"
    update_lists(home,away,home_clean_sheet_link,away_clean_sheet_link, browser)

sorted_scores = sorted(score_likelihood, key=itemgetter(0))
cs_scores = sorted(cs_likelihood, key=itemgetter(0))
print()
print(add_spaces("Likelihood to Score", 30) + "Likelihood to keep CS")
print()
for x in range(len(sorted_scores)):
    first = sorted_scores[x][1] + ": " + str(sorted_scores[x][0])
    second = cs_scores[x][1] + ": " + str(cs_scores[x][0])
    print(add_spaces(first, 30) + second)

f.close()
browser.quit()

    

