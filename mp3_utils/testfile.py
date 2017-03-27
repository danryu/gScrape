import fileinput
import re
import pprint

miniindex = []
with fileinput.input(files=('lateJunc_tag_index.txt')) as f:
    count = 1
    for line in f:
#        print ("LINE IS %s" % line)
        m = re.match("^(.+ Mixtape.*) - (.*)$", line)
        if m is not None:
            mixtape = {
                        'mixname' : m.group(1),
                        'mixdate' : m.group(2),
#                        'index' : count
                      }
            miniindex.append({'index' : count, 'mixtape' : mixtape})
#            print ("NEW MIXTAPE: %s" % mixtape)
        n = re.match("Genre hashtags: (.*)", line)
        if n is not None:
            taglist = n.group(1).split(',')
            miniindex[count-1]['mixtape']['mixtags'] = taglist
#            print ("ADDED TAGS %s " % taglist)
            count = count + 1
    
    for entry in miniindex:
        if entry['mixtape']['mixdate'] == '14/4/16':            
            for num, tag in enumerate(entry['mixtape']['mixtags']):
                print (str(num+1) + ":" + tag)