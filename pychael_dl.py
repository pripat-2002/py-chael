import requests
import os
from bs4 import BeautifulSoup

'''
URL of the archive web-page which provides link to
all video lectures. It would have been tiring to
download each video manually.
In this example, we first crawl the webpage to extract
all the links and then download videos.
'''

def get_video_links(archive_url):
	
	# create response object
	r = requests.get(archive_url)
	
	# create beautiful-soup object
	soup = BeautifulSoup(r.content,'html5lib')
	
	# find all links on web-page
	links = soup.findAll('a')

	# filter the link sending with .mp4
	video_links = [archive_url + link['href'] for link in links if link['href'].endswith('mp4')]

	return video_links


def download_video_series(video_links, save_path):

	for link in video_links:

		'''iterate through all links in video_links
		and download them one by one'''
		
		# obtain filename by splitting url and getting
		# last string
		file_name = link.split('/')[-1]
		file_name = file_name.replace('%20', ' ')
		file_name = file_name.replace('%27', "'")

		vid_files = os.listdir(save_path)
		if file_name in vid_files:
			print( "File:{} already in {}\n".format(file_name,save_path))
			continue
		
		s_path = os.path.join(save_path,file_name)

		print( "Downloading file:%s"%file_name)
		
		# create response object
		r = requests.get(link, stream = True)
		
		# download started
		with open(s_path, 'wb') as f:
			for chunk in r.iter_content(chunk_size = 1024*1024):
				if chunk:
					f.write(chunk)
		
		print( "{} downloaded at {}!\n".format(file_name, save_path) )

	print ("All videos downloaded!")
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
		video_links = get_video_links(archive_url)
		print( '\n\n{} {}\n'.format(len(video_links), video_links) )

		# download all videos
		download_video_series(video_links, save_path)
	
