"""Sample data to test the pubsub internals"""
from pubsub import set_user, post_message, follow
from pprint import pprint
from time import time


set_user('oscar', displayname='Oscar Wilde', password='osloman123', email='oscar@philosophers.com',
         bio='Irish poet and playwright', photo='oscar.jpg')
set_user('jrr', displayname='J.R.R. Tolkien', password='ringlord456', email='jrrt@writers.com',
         bio='English writer, poet, philologist, and university professor', photo='jrr.jpg')
set_user('rene', displayname='René Descartes', password='europa789', email='rene@philosophers.com',
         bio='French philosopher, mathematician, and scientist', photo='rene.jpg')
set_user('anais', displayname='Anaïs Nin', password='tosee012', email='anais@writers.com',
         bio='American diarist, essayist, novelist, and writer of short stories and erotica', photo='anais.jpg')
set_user('kongzi', displayname='Confucius', password='lu2yu3', email='confucius@philosophers.com',
         bio='Chinese teacher, editor, politician, and philosopher', photo='confucius.jpg')
set_user('albert', displayname='Albert Einstein', password='e=mc**2', email='einstein@science.com',
         bio='German-born theoretical physicist who developed the theory of relativity', photo='einstein.jpg')
set_user('gsantayana', displayname='George Santayana', password='spainp543', email='gsantayana@spain.europe',
         bio='Prolific 20th-century Spanish philosopher', photo='gsantayana.jpg')


now = time()

post_message('oscar', 'Work is the curse of the drinking classes')
post_message('jrr', 'Not all those who wander are lost.')
post_message('rene', 'There is nothing so strange and so unbelievable that it has been said by one philosopher or another.')
post_message('anais', "We don't see things as they are, we see them as we are.")
post_message('kongzi', 'To study and not think is a waste. To think and not study is dangerous.')
post_message('kongzi', 'What you do not want done to yourself, do not do to others.')
post_message('kongzi', 'Is it not a joy to have friends come from afar?')
post_message('kongzi', 'The things which men greatly desire are comprehended in meat and drink and sexual pleasure.')
post_message('albert', 'Insanity is repeating the same mistakes and expecting different results.')
post_message('albert', 'Experts are just trained dogs.')
post_message('gsantayana', 'Those who cannot remember the past are condemened to repeat it.')

follow('oscar', followed_user='Anaïs Nin')
follow('oscar', followed_user='René Descartes')
follow('oscar', followed_user='Confucius')
follow('kongzi', followed_user='albert')
follow('kongzi', followed_user='jrr')
follow('jrr', followed_user='albert')



if __name__ == '__main__':
    pprint(posts)
    pprint(user_posts['Anaïs Nin'])

    follow('Oscar Wilde', followed_user='Anaïs Nin')
    follow('Oscar Wilde', followed_user='René Descartes')
    follow('Oscar Wilde', followed_user='Confucius')

    pprint(following)
    pprint(followers)

    pprint(posts_by_user('Confucius', 2))

    print('\n<<<post_for_user()>>>')
    pprint(posts_for_user('Oscar Wilde', limit=2))

    print('\n<<<search()>>>')
    pprint(search('it', limit=2))
