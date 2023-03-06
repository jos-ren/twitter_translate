from project import get_tweets, translate, post_tweets
import pytest

def test_get_tweets():
    assert get_tweets(10, 2459609448) == "All Done"


def test_translate():
    assert translate('hello') == 'bonjour'
    assert translate('bye') == 'au revoir'



def test_post_tweets():
    with pytest.raises(NameError):
        post_tweets('«Les rêves sont si importants.Vous devez avoir de grands objectifs et vous attendre à beaucoup de vous-même, mais vous devez également profiter de la balade. »- Sidney Crosby, joueur canadien de hockey sur glace 🏒.#Thursdaythoughts','https://pbs.twimg.com/media/FYM2gKkWYAEaCaj.jpg') == Response(data={'id': '1550359721676197888', 'text': '«Les rêves sont si importants.Vous devez avoir de grands objectifs et vous attendre à beaucoup de vous-même, mais vous devez également profiter de la balade. »- Sidney Crosby, joueur canadien de hockey sur glace 🏒.#Thursdaythoughts https://t.co/uITohK9IQd'}, includes={}, errors=[], meta={})