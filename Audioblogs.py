import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from gtts import gTTS 
def app():
    st.set_page_config(page_title="Audio Blog",page_icon="🎧")
    st.title("Generates Audio for dev.to blogposts")
    url=st.text_area("Enter any DEV.TO blog url ").strip()
    if st.button("submit"):
        if len(url)!=0:
            with st.spinner('Miracles take time to happen \n Just kidding 😂 \n Generating audio..'):
                results = requests.get(url)
                soup = BeautifulSoup(results.text, "html.parser") 
                blog=[]
                try:
                    Article=soup.find("div",{"class":"crayons-article__header__meta"}).find('h1').get_text()
                    #st.write(Article)
                    Author=soup.find("div",{"class":"crayons-article__subheader"}).find('a').get_text()
                    #st.write(Author)
                    intro="This blogpost {article} is written by {author}".format(article = Article, author = Author)
                    blog.append(intro)
                    text=soup.find("div", {"id": "article-body"}).find_all(['p','h1','h2','h3','h4','h5','h6','ol','ul'])
                    def remove_html_tags(text):
                        for item in text:
                            try:
                                blog.append(item.get_text())
                            except:
                                pass

                    remove_html_tags(text)
                    Text=""
                    for ele in blog:  
                            Text +=ele+" "

                    myobj = gTTS(text=Text, lang='en', slow=False) 
                    
                    myobj.save("Audio.mp3")
                    audio_file = open('Audio.mp3', 'rb')
                    audio_bytes = audio_file.read()
                    st.success("Play or download the audio")
                    st.audio(audio_bytes, format='audio/mp3')
                except:
                    st.error("Enter a valid url")
        else:
            st.error("Enter a valid url")


if __name__ == "__main__":
	app()
