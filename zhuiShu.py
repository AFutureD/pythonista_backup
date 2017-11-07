#coding: utf-8
import requests,json,console,ui,dialogs,time,io,os,re,sys
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
head={"User-Agent":"YouShaQi/2.25.1 (iPhone; iOS 10.3.1; Scale/2.00)","X-User-Agent":"YouShaQi/2.25.1 (iPhone; iOS 10.3.1; Scale/2.00)"}
requests.adapters.DEFAULT_RETRIES=5
def cdn():
	cdn='http://api.zhuishushenqi.com/config/cdns'
	cdn=requests.get(cdn)
	print(cdn.text)
	cdn=json.loads(cdn.text)['cdns'][0]['domain']
	return cdn
q=console.input_alert('请输入关键字','支持书名或作者名搜索')
if not q:
	exit()
url1='http://api.zhuishushenqi.com/book/fuzzy-search?query='+q+'&start=0&limit=100'
book=requests.get(url1)
books_data=json.loads(book.text)['books']
if not books_data:
	console.hud_alert('没有搜到相关小说，请重试！','error',1)
	exit()
else:
	pass
books_list=[]
for book in books_data:
	books_list.append(str(book['title'])+ ' — '+str(book['author'])+'\n'+'书名:'+str(book['title'])+'\n作者:'+str(book['author'])+'\n分类:'+str(book['cat'])+'\n总字数:'+str(book['wordCount'])+'\n最新章节:'+str(book['lastChapter'])+'\n内容简介:'+str(book['shortIntro'])+'\n'+str(book['_id']))
book_menu=dialogs.list_dialog('请选择你要看的小说',books_list,)
if not book_menu:
	console.hud_alert('未选择小说！','erorr',1)
	exit()
else:
	pass
book=book_menu.split('\n')
book_title='-'.join(book[0:1]).replace(' ','')
book_id=book[-1]
book_info='\n'.join(book[2:-1])
console.alert('小说信息',book_info,'确定')

url2='http://api.zhuishushenqi.com/toc?view=summary&book='+book_id
source=requests.get(url2)
sources_data=json.loads(source.text)
sources_list=[]
for source in sources_data:
	sources_list.append(source['name']+'\n'+source['_id'])
source_menu=dialogs.list_dialog('请选择小说源',sources_list)
if not source_menu:
	console.hud_alert('未选择小说源！','erorr',1)
	exit()
else:
	pass
book_id=source_menu.split('\n')[1]

url3='http://api.zhuishushenqi.com/toc/'+book_id+'?view=chapters'
chapter=requests.get(url3)
if not chapter.text:
	console.hud_alert('获取章节失败，请重试！','error',1)
	exit()
else:
	console.hud_alert('获取章节成功！','success',0)
chapters_data=json.loads(chapter.text)['chapters']
down_mode=console.alert('请选择下载方式','','全部章节下载','选择章节下载')
chapters_list=[]
for chapter in chapters_data:
	chapters_list.append(chapter['title']+'\n'+chapter['link'])
if down_mode==1:
		down_list=chapters_list
else:
	chapter_menu=dialogs.list_dialog('请选择下载章节',chapters_list[::-1],multiple=True)
	if not chapter_menu:
		console.hud_alert('未选择下载章节！','erorr',1)
		exit()
	else:
		down_list=chapter_menu[::-1]	
list_count=len(down_list)
down_count=0
dp_count=0
cdn=cdn()
path=os.path.abspath('.')
path_match=re.findall('(?<=/Documents).*',path)
path=path.replace(path_match[0],'')
books_path=path+'/Books'
if os.path.isdir(books_path):
	pass
else:
	os.mkdir(books_path)
file_path=books_path+'/'+book_title+'.txt'
t=int(time.time())+7200
def download(x):
	chapter_info=x.split('\n')
	chapter_title=chapter_info[0]
	chapter_url=chapter_info[1]
	global down_count,dp_count
	down_count=down_count+1
	dp_count=dp_count+1
	console.set_color(.2,.8,.2)
	dp='□'*15
	status='Loading'
	if dp_count>14:
		dp_count=0
	elif down_count==list_count:
		console.set_color(1,0,.8)
		dp_count=15
		status='Finish!'
	else:
		pass
	dp=dp.replace('□','■',dp_count)
	sys.stdout.write('\r'+status+dp+'('+str(down_count)+'/'+str(list_count)+')')
	sys.stdout.flush()
	chapter_url=requests.utils.quote(chapter_url)
	down_url=str(cdn)+'/chapter/'+chapter_url+'?t='+str(t)
	try:
		dr=requests.get(down_url,headers=head,timeout=3)
	except:
		dr=requests.get(down_url,headers=head,timeout=10)
	chapter_body=json.loads(dr.text)['chapter']['body']
	chapter_txt=chapter_title+'\n'+chapter_body
	return chapter_txt
console.clear()
console.set_color(1,0,.8)
console.set_font('Menlo',17)
print('《'+book_title+'》')
t1=int(time.time())
pool=ThreadPool(6)
txts=pool.map(download,down_list)
pool.close()
pool.join()
t2=int(time.time())
book_file=open(file_path,'w+',encoding='utf8')
txt='\n'.join(txts)
book_file.write(txt+'\n')
book_file.close()
del txt,txts,chapters_data,chapters_list,down_list,books_list
size=os.path.getsize(file_path)
if size//1024>=1024:
	size=str(round(size//1024//1024,1))+'MB'
else:
	size=str(size//1024)+'KB'
print('\n共计下载'+str(list_count)+'章，耗时'+str(t2-t1)+'秒。\n文件大小:'+size+'，文件默认保存在根目录下Books文件夹内。')
console.hud_alert('下载完成','succes',1)
console.open_in(file_path)
exit()
