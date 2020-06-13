import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import csv
import os
import argparse
headers = {
    'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
rawHTML = False


def get_posts(currentpageposts, thread_info):
    # Gets all of the posts on a page
    post_list = []
    for item in currentpageposts:
        user_item = item.find('div', class_='panel-body when-expanded-block')
        postdiction = {}
        postdiction.update(thread_info)
        postdiction['id'] = item.attrs['id']
        postdiction['user'] = user_item.find('div', class_='user-uname').text
        try:
            postdiction['date'] = item.select('abbr.ago')[0].attrs['title']
        except (IndexError, AttributeError):
            pass
        if rawHTML:
            postdiction['text'] = user_item.find(
                'div', class_='post-body-html').contents[0]
        else:
            postdiction['text'] = user_item.find(
                'div', class_='post-body-html').get_text("\n", strip=True)
        post_list.append(postdiction)
    return post_list


def get_thread_info(soup):
    thread_info = {}
    thread_info['title'] = soup.find('h2', class_='topic-heading').text
    thread_info['forum'] = soup.find('ol', class_='breadcrumb').text
    try:
        thread_info['page_count'] = soup.find(
            'ul', class_='pager').get_text("\n", strip=True)
        thread_info['page_count'] = int(thread_info['page_count'].split('of')[
                                        1].replace('\nNext →\nLast', '').strip())
    except AttributeError:
        thread_info['page_count'] = 1
    if soup.select(".page-header > ul:nth-child(3)"):
        thread_info['GM'] = soup.select(
            ".page-header > ul:nth-child(3)")[0].text
    else:
        thread_info['GM']='not an RP'

    return thread_info


def page_loop(page_n, base_url, thread_info, post_df):
    # Loops through all pages of a thread. First page was grabbed in outer loop
    for i in range(2, int(page_n)+1):
        resp = requests.get(base_url+'?page='+str(i))
        soup = BeautifulSoup(resp.text, 'html.parser')
        postdiction = {}
        postdiction.update(thread_info)
        time.sleep(.59)
        post_list = get_posts(soup.find_all(
            'div', class_='panel panel-default post visible-post expanded-post'), thread_info)
        post_df = post_df.append(post_list, ignore_index=True)

    return post_df


def get_all(url_list):
    post_data = pd.DataFrame()

    for url in url_list:
        resp = requests.get(url, headers=headers)

        url_base = resp.url
        if url_base[-3:] == '/ic':
            multi_tab = True
            url_base = resp.url[:-3]
        else:
            multi_tab = False
            url_base = resp.url[:-4]

        postdiction = {}
        soup = BeautifulSoup(resp.text, 'html.parser')
        thread_info = get_thread_info(soup)
        thread_info['page'] = 'IC/Base'
        postdiction.update(thread_info)
        post_list = get_posts(soup.find_all(
            'div', class_='panel panel-default post visible-post expanded-post'), thread_info)
        post_data = post_data.append(post_list)
        post_data = page_loop(
            thread_info['page_count'], url_base, thread_info, post_data)
        if multi_tab:
            thread_info['page'] = 'OOC'
            resp = requests.get(url_base+r'/ooc')
            soup = BeautifulSoup(resp.text, 'html.parser')
            try:
                thread_info['page_count'] = soup.find(
                    'ul', class_='pager').get_text("\n", strip=True)
                thread_info['page_count'] = int(thread_info['page_count'].split('of')[
                                                1].replace('\nNext →\nLast', '').strip())
            except AttributeError:
                thread_info['page_count'] = 1
            post_list = get_posts(soup.find_all(
                'div', class_='panel panel-default post visible-post expanded-post'), thread_info)
            post_data = post_data.append(post_list)
            post_data = page_loop(
                thread_info['page_count'], url_base+r'/ooc', thread_info, post_data)

            thread_info['page'] = 'Char'
            resp = requests.get(url_base+r'/char')
            soup = BeautifulSoup(resp.text, 'html.parser')
            try:
                thread_info['page_count'] = soup.find(
                    'ul', class_='pager').get_text("\n", strip=True)
                thread_info['page_count'] = int(thread_info['page_count'].split('of')[
                                                1].replace('\nNext →\nLast', '').strip())
            except AttributeError:
                thread_info['page_count'] = 1
            post_list = get_posts(soup.find_all(
                'div', class_='panel panel-default post visible-post expanded-post'), thread_info)
            post_data = post_data.append(post_list)
            post_data = page_loop(
                thread_info['page_count'], url_base+r'/char', thread_info, post_data)
    return post_data


def list_build(input_csv):
    url_list = []
    with open(input_csv, newline='') as csvfile:
        url_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in url_reader:
            try:
                if row[0][0] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    url_list.append(row[0])
                elif len(row)>1 and row[1] != '':
                    to_range = range(int(row[0]), int(row[1])+1)
                    for item in to_range:
                        url_list.append(
                            'https://www.roleplayerguild.com/topics/'+str(item))
                else:
                    url_list.append(
                        'https://www.roleplayerguild.com/topics/'+row[0])
            except IndexError:
                print(row)
                pass
    return url_list


def begin(resume=False, save=False, limit=0):
    if resume:
        url_list = list_build('in_progress.csv')
    else:
        url_list = list_build('threads.csv')
    if save:
        full_url_list = url_list
    if limit > 0:
        url_list = url_list[:limit]
    if save:
        for num, url in enumerate(url_list, start=1):
            if num == 1:
                get_all([url]).to_csv('posts.csv', header='column_names')
            else:
                get_all([url]).to_csv('posts.csv', mode='a', header=False)
            last_position = num
    else:
        if not os.path.isfile('posts.csv'):
            get_all(url_list).to_csv('posts.csv', header='column_names')
        else:
            get_all(url_list).to_csv('posts.csv', mode='a', header=False)
    if save:
        save_position(full_url_list, last_position)


def save_position(url_list, last_position):

    with open('in_progress.csv', 'w', newline='') as csvfile:
        list_writer = csv.writer(csvfile, delimiter=',',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for item in url_list[last_position:]:
            list_writer.writerow([item])


parser = argparse.ArgumentParser(description='scrape some threads.')
parser.add_argument('--resume', '--r', metavar='N', default=False, type=bool,
                    help='Whether to start from the in_progress CSV or start from scratch')
parser.add_argument('--save', '--s', metavar='N', default=False, type=bool,
                    help='Whether to save progress continually or only at the end')
parser.add_argument('--limit', '--l', metavar='N', default=0, type=int,
                    help='Wheter to proceed through a set number of threads or not')
parser.add_argument('--HTML', '--h', metavar='N', default=False, type=bool,
                    help='Whether to retrieve text or Raw HTML tags')

args = parser.parse_args()
rawHTML = args.HTML
begin(args.resume, args.save, args.limit)
