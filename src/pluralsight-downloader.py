import urllib.request
import urllib.parse
import json
import os
from urllib.parse import parse_qs
import sys
from datetime import datetime
import time
import string

#auth_cookie = "optimizelyEndUserId=oeu1416418471489r0.5932143593672663; mf_23f90557-90d2-4682-9764-9e0e1aa7dc97=-1; __uvt=; newSiteVisited=true; __RequestVerificationToken_L2E1=KvSnrAwdch34X0YXpW6QmO_dUi-f53f4-0Sl6xZo3S3Yse02rU2oxBpWZCNWRT2G4epu2FTH31i21GbP4kMR_wf7CaY1; psPlayer=%7B%22videoScaling%22%3A%22Scaled%22%2C%22videoQuality%22%3A%22High%22%7D; __cfduid=d8d3437c6ec1bfa3c6196ce8d60efe1291421233381; __utma=195666797.1071572145.1416418472.1418391652.1421233384.2; __utmc=195666797; __utmz=195666797.1421233384.2.2.utmcsr=pluralsight.com|utmccn=(referral)|utmcmd=referral|utmcct=/; mp_super_properties=%7B%22all%22%3A%20%7B%22%24initial_referrer%22%3A%20%22http%3A//www.pluralsight.com/%22%2C%22%24initial_referring_domain%22%3A%20%22www.pluralsight.com%22%7D%2C%22events%22%3A%20%7B%7D%2C%22funnels%22%3A%20%7B%7D%7D; ASP.NET_SessionId=05ahzev4oby3thxe0tnfp5mf; _dc_gtm_UA-5643470-2=1; _gat_UA-5643470-2=1; csAnnouncmentShown=true; PSM=687BDBA8680BA6D5D110E69F084B17E21749D61F4B83BF26E2B48FE9E0F0A8E35BFE6BA70736D3C4079B61A3D8FD7F9E2DD5572C190E70E0B6B401A3985441333314962006B020EAA1F824114CEE9B555C4DBB81DAC51F5C4568AEA9F75545C17B1DDCA30FB67647B14C7A74A0F88CAD104CE2B4; _uslk_visits=1; _uslk_referrer=https%3A%2F%2Fwww.google.co.uk%2F; _uslk_bootstrapped=1; _uslk_ct=0; _uslk_co=0; _uslk_active=0; _uslk_page_impressions=17; _uslk_app_state=Idle%3B0; _gali=mfa7; optimizelySegments=%7B%221227392893%22%3A%22search%22%2C%221248401246%22%3A%22gc%22%2C%221258181237%22%3A%22false%22%7D; optimizelyBuckets=%7B%222312010859%22%3A%222321470446%22%2C%222373390355%22%3A%222355640542%22%7D; optimizelyPendingLogEvents=%5B%5D; _ga=GA1.2.1071572145.1416418472; _we_wk_ss_lsf_=true; __ar_v4=ALUY7XVFIBAENNNGZSQOT6%3A20150106%3A3%7CPHHEMWCT7RGRDFUHGCNCJV%3A20150106%3A6%7CBFLWHRV7W5FLTIZIQ4OSO6%3A20150106%3A84%7CNPTOMQSYYZABNNUIQDRAKL%3A20150106%3A84%7C4YCMENXFKFBQLNQCLOV3GS%3A20150106%3A32%7CDOMT5ESRMRH2PDG3LFNDCP%3A20150106%3A36%7CG2LTJRL5ORA4PICF7WRTYP%3A20150108%3A7; uvts=1dJohRWautxxAsDN; visitor_id36882=62000172"
auth_cookie = "optimizelyEndUserId=oeu1422362575640r0.9676906249951571; newSiteVisited=true; mf_23f90557-90d2-4682-9764-9e0e1aa7dc97=-1; _dc_gtm_UA-5643470-2=1; _gat_UA-5643470-2=1; csAnnouncmentShown=true; __uvt=; __RequestVerificationToken_L2E1=Vjdcwdtf6TOJJ_X_BwQvicaEz_FSjeqO6YkyNeWpXTMingetslvQMnMokVNgN2Eri57fHLz7zfR_Vh44CyEZ_IPI6go1; PSM=92BB9C81692C8EF830E4FE1D85FB7C68008959D10397B8231F0D2BA0D19228546F5D2913A55CAD38AAE5E2CE02F04A2405EA664101D8680C5C7C72F52AC1506AF8C5EDDC3EEEF730776730C612D2EF6DD02D578666E0B6578699D0371CE6171CC7739CF37022558D6F0BC2EA75478F527DEF37F1A7A77836F15FF2667BE1D64B1EF6EDD4CB177AD70F5D7F0040F0AB4496F15B6BAAF9250B4976068C0B3EFF5C10609463BD81018D46D355DB463ABF6AD74A7BD2; visitor_id36882=73523072; _gali=mfa52; optimizelySegments=%7B%221227392893%22%3A%22direct%22%2C%221248401246%22%3A%22gc%22%2C%221258181237%22%3A%22false%22%7D; optimizelyReferrer=; optimizelyBuckets=%7B%222312010859%22%3A%222321470446%22%2C%222373390355%22%3A%222321861900%22%7D; _ga=GA1.2.390107053.1422362576; optimizelyPendingLogEvents=%5B%5D; _we_wk_ss_lsf_=true; __ar_v4=NCTBDPMUBNA2FPNKWLTYKE%3A20150126%3A1%7CBFLWHRV7W5FLTIZIQ4OSO6%3A20150126%3A11%7CNPTOMQSYYZABNNUIQDRAKL%3A20150126%3A11%7C4YCMENXFKFBQLNQCLOV3GS%3A20150126%3A8%7CPHHEMWCT7RGRDFUHGCNCJV%3A20150126%3A1%7CDOMT5ESRMRH2PDG3LFNDCP%3A20150126%3A1; uvts=2cqKX8fGhEEi90mS"

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
				
				title = "".join(x for x in clip['title'] if x.isalnum())
				name = "".join(x for x in clip['name'] if x.isalnum())
				itemTitle = "".join(x for x in item['title'] if x.isalnum())
				
				dir = os.getcwd() + "\\" + url + "\\"
				directory = dir + str(id) + "-" + itemTitle + "\\";
				
				filename = directory + name + " - " + title + ".mp4"
				if os.path.exists(filename):
					print('File already downloaded')
					continue 
				if not os.path.exists(directory):
					os.makedirs(directory)
					
				time.sleep(120)
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