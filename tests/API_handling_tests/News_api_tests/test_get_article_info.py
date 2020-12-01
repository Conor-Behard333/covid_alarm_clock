from api_handling.get_news_info import get_article_info


def test_expected_response():
    test_response = {
        "status": "ok",
        "totalResults": 1,
        "articles": [
            {
                "source": {
                    "id": "bbc-news",
                    "name": "BBC News"
                },
                "author": "https://www.facebook.com/bbcnews",
                "title": "Covid: Boris Johnson writes to MPs to quell anger over new tiers - BBC News",
                "description": "Facing a rebellion in his party, Boris Johnson tells MPs that England's new rules could end in nine weeks.",
                "url": "https://www.bbc.co.uk/news/uk-55118467",
                "urlToImage": "https://ichef.bbci.co.uk/news/1024/branded_news/D46A/production/_115687345_hi064531970.jpg",
                "publishedAt": "2020-11-29T10:22:00Z",
                "content": "England's new Covid tier system has a \"sunset\" expiry date of 3 February, Boris Johnson has told his MPs in a bid to prevent a Commons rebellion.\r\nThe current lockdown ends on Wednesday, and many Tor\u2026 [+7423 chars]"
            }
        ]
    }
    expected = [["Covid: Boris Johnson writes to MPs to quell anger over new tiers - BBC News",
                 "Facing a rebellion in his party, Boris Johnson tells MPs that England's new rules could end in nine weeks.",
                 "https://www.bbc.co.uk/news/uk-55118467", "BBC News"]]

    assert get_article_info(test_response) == expected


def test_none_response():
    test_response = None

    assert get_article_info(test_response) is None
