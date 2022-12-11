import os
import re
import requests
from bs4 import BeautifulSoup
from clint.textui import progress

'''
URL of the archive web-page which provides link to
all video lectures. It would have been tiring to
download each video manually.
In this example, we first crawl the webpage to extract
all the links and then download videos.
'''

def get_video_dic(archive_url):
	
	# create response object
	r = requests.get(archive_url)
	
	# create beautiful-soup object
	soup = BeautifulSoup(r.content,'html5lib')
	
	# find all links on web-page
	links = soup.findAll('a')

	# filter the link sending with .mp4
	video_links = [archive_url + link['href'] for link in links if link['href'].endswith('mp4')]

	# get video sizes
	video_sizes = []
	text = soup.get_text()
	text = text.split('\n')
	for elem in text:
		s = re.findall(f'\d+$',elem)
		if s:
			video_sizes.append(s[0])

	if len(video_links)!=len(video_sizes):
		print("\n\nFATAL ERROR: number of video links and video sizes mismatch! \nCode execution is terminated.")
		exit()

	# create a dictionary of video link and video size
	video_dic = {}
	for i in range(len(video_links)):
		video_dic[video_links[i]]=video_sizes[i]

	return video_dic


def download_video_series(video_dic, save_path):

	video_links = list(video_dic.keys())

	for link in video_links:

		'''iterate through all links in video_links
		and download them one by one'''
		
		# obtain filename by splitting url and getting
		# last string
		file_name = link.split('/')[-1]
		file_name = file_name.replace(r'%20', r' ')
		file_name = file_name.replace(r'%27', r"'")
		file_name = file_name.replace(r'%2b', r'+')

		# file size
		file_size = int(video_dic[link])

		# download chunk size
		chunk_size = 1024*1024

		# checking if video file is already present in directory
		vid_files = os.listdir(save_path)
		if file_name in vid_files:
			print( "File:{} already present in {}\n".format(file_name,save_path))
			continue
		
		s_path = os.path.join(save_path,file_name)

		print( "Downloading file:%s"%file_name)
		
		# create response object
		r = requests.get(link, stream = True)
		
		# download started
		with open(s_path, 'wb') as f:
			for chunk in progress.bar(r.iter_content(chunk_size = 1024*1024),expected_size=(file_size/chunk_size) + 1):
				if chunk:
					f.write(chunk)
					f.flush
		
		print( "{} downloaded at {}!\n".format(file_name, save_path) )

	print ("All videos of this season downloaded!\n\n")
	return


if __name__ == "__main__":

	start_season = 1
	end_season = 9

	main_path = r"/home/shuno/Downloads/The Office"

	for x in range(start_season,end_season+1):

		save_path = os.path.join(main_path,'S0{}'.format(x))

		try:
			os.mkdir(save_path)
		except:
			pass


		# specify the URL of the archive here
		archive_url = "http://51.158.153.210/the-office/season-{}/".format(x)

		# getting all video links
		video_dic = get_video_dic(archive_url)
		print('{}\t{}\n'.format(len(video_dic),video_dic))

		# download all videos
		download_video_series(video_dic, save_path)
	
