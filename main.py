from flask import Flask, jsonify, request
import re
from pixivpy3 import *
import random

app = Flask(__name__)
api = AppPixivAPI()
api.auth(refresh_token='VMne--uMWqwawZl_17_dhxsE4uc5RAhG_1wGQz5LGkY')

def replace_origin_url(url):
    return url.replace('https://i.pximg.net/c/600x1200_90/img-master/img', 'https://i.pixiv.re/img-master/img')

@app.route('/')
def welcome():
    return render_template('index.html')
    
@app.route('/getpixiv', methods=['GET'])
def get_pixiv():
    illust_id = request.args.get('id')
    json_result = api.illust_detail(illust_id)
    illust = json_result.illust
    image_url = illust.image_urls['large']
    replaced_url = replace_origin_url(image_url)
    return jsonify({'origin_url': replaced_url})

@app.route('/search', methods=['GET'])
def search_pixiv():
    query = request.args.get('q')
    json_result = api.search_illust(query, search_target='partial_match_for_tags')
    illusts = json_result.illusts
    if illusts:
        random_illusts = random.sample(illusts, min(10, len(illusts)))
        results = []
        for illust in random_illusts:
            image_url = illust.image_urls['large']
            replaced_url = replace_origin_url(image_url)
            results.append({'title': illust.title, 'origin_url': replaced_url})
        return jsonify(results)
    else:
        return jsonify({'error': 'No results found for the query'})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
