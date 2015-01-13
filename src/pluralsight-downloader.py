import urllib.request
import urllib.parse
import json
import os
from urllib.parse import parse_qs
import sys
from datetime import datetime
import time

auth_cookie = "optimizelyEndUserId=oeu1416418471489r0.5932143593672663; mf_23f90557-90d2-4682-9764-9e0e1aa7dc97=-1; __uvt=; __utma=195666797.1071572145.1416418472.1418391652.1418391652.1; __utmc=195666797; __utmz=195666797.1418391652.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); newSiteVisited=true; _uslk_visits=1; _uslk_referrer=https%3A%2F%2Fwww.google.co.uk%2F; _uslk_bootstrapped=1; _uslk_ct=0; _uslk_co=0; _uslk_active=0; _uslk_page_impressions=4; _uslk_app_state=Idle%3B0; __RequestVerificationToken_L2E1=KvSnrAwdch34X0YXpW6QmO_dUi-f53f4-0Sl6xZo3S3Yse02rU2oxBpWZCNWRT2G4epu2FTH31i21GbP4kMR_wf7CaY1; _dc_gtm_UA-5643470-2=1; _gat_UA-5643470-2=1; PSM=79C440B1FD6441CFA6BDC4858DADC6B7DE120226402315ABD37A7E4D5CFC2FB6B8D30600CD70FEC6875F7D3E95D4980724F7F743C71AD53CBF0D3ABE52D997EFEECEFB943BC30986B7CAFCB40DC97EF43C4314C51D70191F506DB3D4289D6B867B110CF7A65C205CDC7736B975C33F0BE76DA7C20506F4F76D41DBDF0BBED7CA3EAAEC4750C88A107A9BA1958F8A73358561170B1E0B20FF84E7DB11AFFC719E670D4122454373B6762EE06B90E225E192FCBC5B; optimizelySegments=%7B%221227392893%22%3A%22search%22%2C%221248401246%22%3A%22gc%22%2C%221258181237%22%3A%22false%22%7D; optimizelyBuckets=%7B%222312010859%22%3A%222321470446%22%7D; _ga=GA1.2.1071572145.1416418472; __ar_v4=ALUY7XVFIBAENNNGZSQOT6%3A20150106%3A3%7CPHHEMWCT7RGRDFUHGCNCJV%3A20150106%3A4%7CBFLWHRV7W5FLTIZIQ4OSO6%3A20150106%3A24%7CNPTOMQSYYZABNNUIQDRAKL%3A20150106%3A24%7C4YCMENXFKFBQLNQCLOV3GS%3A20150106%3A8%7CDOMT5ESRMRH2PDG3LFNDCP%3A20150106%3A7%7CG2LTJRL5ORA4PICF7WRTYP%3A20150108%3A2; _we_wk_ss_lsf_=true; _gali=mfa92; optimizelyPendingLogEvents=%5B%5D; uvts=1dJohRWautxxAsDN; visitor_id36882=62000172; psPlayer=%7B%22videoScaling%22%3A%22Scaled%22%2C%22videoQuality%22%3A%22High%22%7D"

start_time = datetime.now()

def build_post_body(params, index):
	return "{a:\""+ params['author'][0] +"\", m:\""+ params['name'][0] +"\", course:\""+ params['course'][0] +"\", cn:"+ str(index) +", mt:\"mp4\"}"

def make_requests(url):
	response = [None]
	responseText = None

	if(request_www_pluralsight_com(response, url)):
		responseText = read_response(response[0])
		response[0].close()
		data = json.loads(responseText)
		id =1
		for item in data:
			print('Downloading: ' + item['title'])

			for clip in item['clips']:
				par = parse_qs(urllib.parse.urlparse('http://something.com?' + clip['playerParameters']).query, keep_blank_values=True)
				
				dir = os.getcwd() + "\\" + url + "\\"
				directory = dir + str(id) + "-" + item['title'] + "\\";
				title = "".join(x for x in clip['title'] if x.isalnum())
				filename = directory + clip['name'] + " - " + title + ".mp4"
				if os.path.exists(filename):
					print('File already downloaded')
					continue 
				if not os.path.exists(directory):
					os.makedirs(directory)
					
				time.sleep(1)
				print('Downloading: ' + filename)
				if(request_www_pluralsight_com_video(response, build_post_body(par, clip['clipIndex']))):
					responseText = read_response(response[0])
					response[0].close()
					urllib.request.urlretrieve(responseText, filename)
			id+=1			
	end_time = datetime.now()
	print('Duration: {}'.format(end_time - start_time))
	print("All done!! Enjoy :)")

def read_response(response):
	if response.info().get('Content-Encoding') == 'gzip':
		buf = BytesIO(response.read())
		return gzip.GzipFile(fileobj=buf).read().decode('utf8')

	elif response.info().get('Content-Encoding') == 'deflate':
		decompress = zlib.decompressobj(-zlib.MAX_WBITS)
		inflated = decompress.decompress(response.read())
		inflated += decompress.flush()
		return inflated.decode('utf8')

	return response.read().decode('utf8')


def request_www_pluralsight_com(response, url):
	response[0] = None

	try:
		req = urllib.request.Request("http://www.pluralsight.com/data/course/content/" + url)

		req.add_header("User-Agent", "Fiddler")

		response[0] = urllib.request.urlopen(req)

	except urllib.error.URLError as e:
		if not hasattr(e, "code"):
			return False
		response[0] = e
	except:
		return False

	return True
	
def request_www_pluralsight_com_video(response, body):
	response[0] = None
	
	try:
		req = urllib.request.Request("http://www.pluralsight.com/training/Player/ViewClip")

		req.add_header("Connection", "keep-alive")
		req.add_header("Accept", "application/json, text/plain, */*")
		req.add_header("X-Requested-With", "XMLHttpRequest")
		req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36")
		req.add_header("Content-Type", "application/json;charset=UTF-8")
		req.add_header("Accept-Encoding", "gzip, deflate")
		req.add_header("Accept-Language", "en-GB,en;q=0.8,en-US;q=0.6,pt;q=0.4,pt-PT;q=0.2")
		req.add_header("Cookie", auth_cookie)
		
		body = binary_data = body.encode()
		response[0] = urllib.request.urlopen(req, body)
	except urllib.error.URLError as e:
		if not hasattr(e, "code"):
			return False
		response[0] = e
	except ValueError:
		print(ValueError)
		return False
		
	return True

	
if len(sys.argv) <= 1:
	print('You need to pass the name of the module as parameter')
else:
	make_requests(sys.argv[1])