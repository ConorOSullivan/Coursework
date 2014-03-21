__author__ = 'conorosullivan'

'''
This assignment had me opening the included file,
gameslist.csv, and scraping their Amazon.com pages
to gather review information
'''


import mysql.connector
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import os
import time
import random
import csv
import sys
from datetime import datetime


def question1():
    game_list = list(csv.reader(open("gamelist.csv", "r")))
    for i in range(0, len(game_list)):
        # Open the initial URL for the game's reviews and get the text
        review_url = game_list[i][1]

        #-------------------------------------------------------------------------
        # Scrape the ratings
        #-------------------------------------------------------------------------
        page_no = 1
        sum_total_reviews = 0
        more = True

        while (more):
            # Open the URL to get the review data
            request = urllib2.Request(review_url)

            try:
                page = urllib2.urlopen(request)
            except urllib2.URLError, e:
                if hasattr(e, 'reason'):
                    print 'Failed to reach url'
                    print 'Reason: ', e.reason
                    sys.exit()
                elif hasattr(e, 'code'):
                    if e.code == 404:
                        print 'Error: ', e.code
                        sys.exit()

            content = page.read()
            soup = BeautifulSoup(content)

            # Results is list of star ratings, some we will not print though
            results = soup.findAll('span', {'class': re.compile(r's_star_\d_0')})
            # p is the list of reviews
            p = soup.findAll('div', {'style':'margin-left:0.5em;'})
            # Get star rating
            count = 0
            totalcounter = 0
            for result in results:
                totalcounter+=1
                if result.parent.get('style') is None:
                    continue
                else:
                    if re.match('margin-right:5px;', result.parent.get('style')) is None:
                        continue
                    else:
                        print result.get('title')
                        newReview = re.sub(r'(\d+\sof\s\d+\speople\sfound\sthe\sfollowing\sreview\shelpful)',' ',p[count].text)
                        newReview = re.sub(r'Help\sother.+','',newReview)
                        newReview = re.sub(r'^\d+\sout\sof\s\d\sstars','',newReview)
                        newReview = re.sub(r'(\d.0)\sout\sof\s\d\sstars','',newReview)
                        newReview = re.sub('\n','',newReview)
                        print newReview
                        print "\n"
                        #print "this is the number of review we just printed: %d"%totalcounter
                        count += 1
            # Accumulate the total number of ratings.
            sum_total_reviews += count


            # check for the next results, if they exist
            # find all URL links in the source
            more = False
            for link in soup.findAll('a'):
                if re.match('Next', link.text) <> None:
                    review_url = link.get('href')
                    more = True
                    break

            # Print some status info

            current_time = datetime.now().strftime('%I:%M:%S%p')

            print '\n\n\n'

            print '%s - %s - Page: %s - Ratings: %s - Total Ratings: %s' % (current_time,
                                game_list[i][0], page_no, len(results), sum_total_reviews)

            # Generate a random waiting time to avoid being detected and banned
            wait_time = round(max(0, 1 + random.gauss(0,0.5)), 2)
            time.sleep(wait_time)
            # Increment the page number
            page_no += 1

def question2(duration, username):
    # Make sure duration is passed as a string, e.g., '36' for 36 months
    class MySQLCursorDict(mysql.connector.cursor.MySQLCursor):
      def fetchone(self):
        row = self._fetch_row()
        if row:
          return dict(zip(self.column_names, self._row_to_python(row)))
        return None

    cnx = mysql.connector.connect(user=username, database='MSAN692db')

    query = "select A.loan_id, A.state from loanstats A,  " \
            "(select state, avg(5*ascii(substr(credit_grade,1,1))-65+substr(credit_grade,2,1)) state_grade from loanstats where loan_duration="+duration+" group by state) B, " \
            "(select state, avg(interest_rate) state_rate from loanstats where loan_duration="+duration+" group by state) C " \
            "where (5*ascii(substr(A.credit_grade,1,1))-65+substr(A.credit_grade,2,1)) < B.state_grade " \
            "and A.interest_rate > C.state_rate " \
            "and A.state=B.state " \
            "and A.state=C.state " \
            "and A.loan_duration="+duration+" " \
            "order by A.state, A.loan_id;"

    cursor = cnx.cursor(cursor_class=MySQLCursorDict, buffered=True)
    cursor.execute(query)

    for row in cursor:
       print row
    cursor.close()
    cnx.close()
