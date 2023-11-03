from flask import Flask, render_template, url_for,request,redirect, session
import pickle
import os
import re
from newsapi import NewsApiClient

app=Flask(__name__)
model=pickle.load(open('goldnewsanalysis.pkl','rb'))

@app.route('/',methods=['POST', 'GET'])
def homepage():
    return render_template('index.html')

@app.route('/prediction',methods=['POST', 'GET'])
def predictionpage():
    if request.method == 'POST':
        newsline = request.form["newheadline"]
        # if(newsline == ""):
        #     return render_template('index.html', input=0)    
            # return redirect(url_for('home', input=0))    
        pred=[newsline]
        output=model.predict(pred)
        print(output)
        if output==['positive']:
            return render_template('index.html',output='upward movement in gold price')
        if output==['negative']:
            return render_template('index.html',output='downward movement in gold price')
        if output==['neutral']:
            return render_template('index.html',output='steady movement in gold price')
        if output==['none']:
            return render_template('index.html',output='this news headline is not related to gold news')
    return render_template('index.html')


@app.route('/news')
def newspage():
    newsapi=NewsApiClient(api_key="43ffea2aa8d84b4fbbe2fe18538d8fa7")
    topheadlines=newsapi.get_top_headlines(sources='bbc-news')
    # topheadlines = newsapi.get_top_headlines(category='business', country='us')

    # for article in topheadlines['articles']:
        # if 'commodity' in article['title'].lower() or 'commodity' in article['description'].lower():
        #     print(article['title'])

    # topheadlines=newsapi.get_top_headlines(q='sport')
    toparticles=topheadlines['articles']
    news=[]
    desc=[]
    image=[]
    url=[]
    # print(url)
    # toparticles = str(toparticles)
    # print(toparticles)
    for i in range(len(toparticles)):
        print(len(toparticles))
        # for item in news
        # print(toparticles[i]['title'])
        # if 'Gold' in toparticles['title'] or 'Gold' in toparticles['description']:
        # if 'commodity ' in toparticles[i]['title'] or 'commodity' in toparticles[i]['description']:
        mainarticle=toparticles[i]
        news.append(mainarticle['title'])
        desc.append(mainarticle['description'])
        image.append(mainarticle['urlToImage'])
        url.append(mainarticle['url'])
        contents=zip(news,desc,image,url)
        # print(mainarticle)
        if i >= 3:
            break    
    return render_template("index.html",contents=contents)
    # return render_template("index.html")

if __name__=='__main__':
    app.run(debug=True)