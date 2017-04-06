from subprocess import Popen, PIPE

hashtags = (
    '#BVB',
    '#FCBayern',
    '#Atleti',
    '#FCBarcelona',
    '#realmadrid',
    '#SevillaFC',
    '#acmilan',
    '#ASRoma',
    '#inter',
    '#juventusfc',
    '#ChelseaFC',
    '#lfc',
    '#mcfc',
    '#mufc',
    '#thfc',
    '#PSG_inside',
    '#OL',
    '#AFC'
)

for hashtag in hashtags:
    cmd = ['python', 'gnip_hadoop.py', '{}'.format(hashtag)]
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
