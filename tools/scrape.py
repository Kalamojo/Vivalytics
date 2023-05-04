import bs4
import requests

def get_img_link(url):
	print("why")
	r = requests.get(url)
	print("this")

	html = bs4.BeautifulSoup(r.text, 'html.parser')
	title = html.find("div", {"id": "meta"})
	print("slow")
	if title:
		image = title.find("img")
		print(image)
		if image == None:
			return "not_found"
		return image['src']
	return "not_found"