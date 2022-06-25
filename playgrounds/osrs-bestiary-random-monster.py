import random
import requests
import shutil
# from urllib.request import urlopen
import cv2
import numpy as np
from bs4 import BeautifulSoup

BASEURL = "https://oldschool.runescape.wiki/"
bestiary_url = "w/Bestiary/"

LOWESTLEVEL = 1
SOFTCAPLEVEL = 200

# Scale image after
scale_percent = 100

#__Choose random bestiary level set ( sets of 10 )
level_set_start = random.randrange( 1, (SOFTCAPLEVEL-10), 10 ) # pick a number from 1-190 in intervals of 10 ( first num of set )
level_set_end = level_set_start + 9

level_set_url = "Levels_{}_to_{}".format( level_set_start, level_set_end )
print( level_set_url )

#__Retreive Page
full_url = BASEURL + bestiary_url + level_set_url
page = requests.get( full_url )

soup = BeautifulSoup( page.content, "html.parser" )

#__Analyze table
monster_container = soup.find( "div", class_="mw-parser-output" )
monster_table = monster_container.find( "table" )
table_rows = monster_table.find_all( "tr" )

#__Get random monster
print("test table length" )
print( len( table_rows ) )
monster = table_rows[ random.randrange( 0, len( table_rows ) ) ]
#__monster page
monster_anchor = monster.find( "a" )
monster_anchor_href = monster_anchor[ "href" ]
monster_page_url = BASEURL + monster_anchor_href
monster_page = requests.get( monster_page_url )
monster_soup = BeautifulSoup( monster_page.content, "html.parser" )
monster_image = monster_soup.find( "img" )
monster_image_url = monster_image[ "src" ]
print( monster_image )
#__monster thumbnail
monster_image_element = monster.find( "img" )
monster_name =  monster_image_element[ "alt" ]
monster_thumbnail_url =  monster_image_element[ "src" ]
#_monster image ( pick thumbnail or page )
# image_url =  monster_image_element[ "src" ] # for monster thumbnail
image_url = monster_image_url

# first_monster = table_rows[ 1 ]
# print( first_monster.prettify() )
# monster_image_element = first_monster.find( "img" )
# monster_name = monster_image_element[ "alt" ]
# image_url = monster_image_element[ "src" ]
# # print( monster_name )
# # print( image_url )

# urllib library = bad
# image_request = urllib.request.urlopen( BASEURL + image_url )
# image_request = urlopen( BASEURL + image_url )
image_request = requests.get( BASEURL + image_url, stream=True )
if image_request.status_code == 200:
  arr = np.asarray( bytearray( image_request.content ), dtype=np.uint8 )
  monster_image = cv2.imdecode( arr, -1 )
  r_width = int( monster_image.shape[1] * scale_percent / 100 )
  r_height = int( monster_image.shape[0] * scale_percent / 100 )
  r_dim = ( r_width, r_height )
  resized = cv2.resize( monster_image, r_dim, interpolation = cv2.INTER_AREA )
  cv2.imshow( monster_name, resized )
  if cv2.waitKey() & 0xff == 27: quit()

