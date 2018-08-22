from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.selectableview import SelectableView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView, ListItemButton
from kivy.lang import Builder
from kivy.factory import Factory
import sys

import feedparser

Factory.register('SelectableView', cls=SelectableView)
Factory.register('ListItemButton', cls=ListItemButton)

Builder.load_string('''
[ThumbnailedListItem@SelectableView+BoxLayout]:
    name: ctx.text
    size_hint_y: ctx.size_hint_y
    height: ctx.height
    AsyncImage:   #Async
        size_hint_y: 1.0
        size_hint_x: 0.3
        source: ctx.imageurl
    ListItemButton:
        text: ctx.text
''')


news_list = {}
class NewsView(GridLayout):

    def __init__(self, **kwargs):#using kwargs we can pass variable no. of arguents
        kwargs['cols'] = 3
        super(NewsView, self).__init__(**kwargs)
        feedurl = sys.argv[1]
        if len(sys.argv)!=2:
            print("ERROR")
            exit()
        else: 
            feed = feedparser.parse(feedurl)
            numofentries = len(feed['entries'])
            for i in range(0, numofentries):
                news_list[i] = dict({
                   'index': str(i),
                   'title': feed['entries'][i]['title'],
                   'imageurl': feed['entries'][i]["media_thumbnail"][0]["url"]
                   })
    
            list_item_args_converter = \
                 lambda row_index, rec: {'text': rec['title'],
                                           'imageurl': rec['imageurl'],
                                           'size_hint_y': None,
                                           'height': 100}
            nlist = sorted(news_list.keys())
            news_list_adapter = \
            DictAdapter(
                       sorted_keys=nlist,
                       data=news_list,
                       args_converter=list_item_args_converter,
                       selection_mode='single',
                       allow_empty_selection=False,
                       template='ThumbnailedListItem')
    
        
                
            news_list_view = \
                    ListView(adapter=news_list_adapter)
            self.add_widget(news_list_view)
        
    

if __name__ == '__main__':

    from kivy.base import runTouchApp
    runTouchApp(NewsView(width=800))
