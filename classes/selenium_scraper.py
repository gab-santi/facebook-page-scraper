from selenium import webdriver
from selenium.webdriver.common import keys
import pandas as pd

class SeleniumScraper:
    # initialize selenium driver
    def __init__(self, chromedriver_path, email, password):
        self.driver = webdriver.Chrome(chromedriver_path)
        
        # start fb
        self.startFacebook()

        # login
        self.loginFacebook(email, password)
        self.wait(seconds=5)
        
    def startFacebook(self):
        self.driver.get('http://www.facebook.com')
        print('opened browser')

    def loginFacebook(self, email, password):
        # input email
        elem = self.driver.find_element_by_name('email')
        elem.send_keys(email)

        #input password
        elem = self.driver.find_element_by_name('pass')
        elem.send_keys(password)

        #click login button
        elem = self.driver.find_element_by_id('u_0_b')
        elem.click()       

    #scrape fb comments found on url
    def scrapeFacebookComments(self, post_id, url):
        # initialize comments df
        comments_df = pd.DataFrame(columns=['post_id', 'comment_id', 'commenter_name', 'commenter_profile_link', 'text', 'time', 'reactions_count'], index=None)
        
        # put comments in rows
        replies = []
        self.driver.get(url)
        print('opened fb comment link: {}'.format(url))
        #self.wait()
        try:
            self.driver.find_element_by_class_name('_108_').click()
            print('clicked view more comments')
        except:
            pass

        #get comments from page
        # _2bo4
        comment_elements = self.driver.find_elements_by_class_name('_2b04')
        
        #comment contents
        #print(comment_elements)

        #comment_element
        if (len(comment_elements) > 0):
            # get comment details from each comment element then put to df
            for item in comment_elements:
                # _2bo6
                try:
                    comment_contents = item.find_element_by_class_name('_2b06')
                    comment_id = comment_contents.find_elements_by_tag_name('div')[1].get_attribute('data-commentid')
                
                    if (comment_id != None):
                        print('Comment ID: ', comment_id)

                        # click more replies
                        try:
                            more_replies = item.find_element_by_class_name('_2b1h.async_elem')
                            more_replies_href = more_replies.find_element_by_tag_name('a').click()
                        except:
                            pass

                        # get main comment element
                        # _2bo5
                        commenter_details = item.find_element_by_class_name('_2b05').find_element_by_tag_name('a')
                        
                        # get commenter name
                        commenter_name = commenter_details.text
                        print('Commenter name: ', commenter_name)

                        # get commenter profile link
                        commenter_profile_link = commenter_details.get_attribute('href')
                        print(commenter_profile_link)

                        # get comment text and comment ID
                        try:
                            comment_text = comment_contents.find_elements_by_tag_name('div')[1].text
                            print('Comment: ', comment_text)
                        except:
                            comment_text = ""

                        # get posted time

                        # get reactions
                        try:
                            comment_reactions_count = item.find_element_by_class_name('_14va').text
                            if (comment_reactions_count == ''):
                                comment_reactions_count = 0
                            print('Comment reactions: ', comment_reactions_count)
                        except:
                            comment_reactions_count = 0

                        # get replies
                        try:
                            # find replies element
                            # _2b1k
                            replies_element = item.find_element_by_class_name('_2b1k')

                            # click view next replies if exists
                            try:
                                replies_element.find_element_by_class_name('async_elem').click()
                                print('clicked view all replies')
                            except:
                                pass

                            # get all reply details
                            # _2a_i
                            replies = replies_element.find_elements_by_class_name('_2a_i')

                            for reply in replies:
                                # store replies data
                                # _2b06
                                reply_info = reply.find_element_by_class_name('_2b06')

                                # replyer name
                                # _2b05
                                replyer_info = reply_info.find_element_by_class_name('_2b05')
                                replyer_name = replyer_info.find_element_by_tag_name('a').text
                                print("Replyer name: {}".format(replyer_name))

                                # replyer url
                                replyer_profile_link = replyer_info.find_element_by_tag_name('a').get_attribute('href')
                                print('Replyer profile: {}'.format(replyer_profile_link))

                                # reply id
                                reply_id = reply_info.find_elements_by_tag_name('div')[1].get_attribute('data-uniqueid')
                                print('Reply ID: {}'.format(reply_id))

                                # time created

                                # reply text
                                try:
                                    reply_text = reply_info.find_elements_by_tag_name('div')[1].text
                                    print(reply_text)
                                except:
                                    reply_text = ""

                                try:
                                    reply_reactions = reply.find_element_by_class_name('_14va').text
                                except:
                                    reply_reactions = 0
                                
                                print('Reply reactions: ', reply_reactions)
                        except:
                            pass
                        
                        ids = comment_id.split('_')
                        # add comment row to temp df
                        comments_df = comments_df.append({'post_id': ids[0], 'comment_id': ids[1], 'commenter_name': commenter_name, 'commenter_profile_link': commenter_profile_link, 'text': comment_text, 'time': '', 'reactions_count': comment_reactions_count}, ignore_index=True)
                        print('current page comments:')
                        print(comments_df)
                except:
                    pass
        else:
            print('No comments found')

        return comments_df

    # make the webdriver implicitly wait
    def wait(self, seconds=3):
        self.driver.implicitly_wait(seconds)

    # close selenium driver
    def closeDriver(self):
        self.driver.close()
