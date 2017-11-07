import photos, appex

def delete_tapped(sender):
	for i in albums:
		i.delete()
	widget_alert('Done')

def widget_alert(title_content, text_content = '', option = False):
	import ui
	view = ui.View()
	top_height = title_height = text_height = option_height = 0
	
	if title_content:
		title_line = len(title_content.split('\n'))
		title = ui.Label()
		title.font = ('<system-bold>', 15)
		title.flex = 'W'
		title.height = title_height = title_line * 20
		title.alignment = ui.ALIGN_CENTER
		title.number_of_lines = 0
		title.text = title_content
		view.add_subview(title)
		
	if text_content:
		text_line = len(text_content.split('\n'))
		text = ui.Label()
		text.font = ('<system>', 15)
		text.flex = 'W'
		text.height = text_height = text_line * 20
		text.alignment = ui.ALIGN_CENTER
		text.number_of_lines = 0
		text.text = text_content
		view.add_subview(text)
		
	if option:
		button = ui.Button()
		button.font = ('<system>', 15)
		button.background_color = (0.0, 0.0, 0.0, 0.3)
		button.tint_color = 'white'
		button.corner_radius = 5
		option_height = 25 + 5
		button.title = 'Delete'
		button.action = delete_tapped
		view.add_subview(button)
		
	view_height = title_height + text_height + option_height
	if view_height <= 125:
		view.height = 125
		top_height = (125 - view_height) /2
	else:
		top_height = 10
		view.height = view_height + 20
		
	if title_content:
		title.y = top_height
	if text_content:
		text.y = top_height + title_height
	if option:
		x = (ui.get_window_size()[0] - 120) / 2
		y = top_height + title_height + text_height + 5
		button.frame = (x, y, 130, 25)

	appex.set_widget_view(view)
	
def main():
	if appex.is_widget():
		global albums
		albums = photos.get_albums()
		albums_num = len(albums)
		if albums_num == 0:
			widget_alert('No User Album')
		else:
			albums_title = ''
			for i in albums:
				image_num = str(len(i.assets))
				albums_title += i.title + ': ' + image_num + ' Pieces\n'
			widget_alert(str(len(albums)) + ' User Albums', albums_title + '\nClick "Delete" to delete all albums.', True)
	
	else:
		import console
		albums = photos.get_albums()
		albums_num = len(albums)
		if albums_num == 0:
			console.hud_alert('No User Album')
		else:
			albums_title = ''
			for i in albums:
				image_num = str(len(i.assets))
				albums_title += i.title + ': ' + image_num + ' Pieces\n'
			console.alert(str(len(albums)) + ' User Albums', albums_title + '\nClick "Delete" to delete all albums.', 'Delete')
			for i in albums:
				i.delete()
			console.hud_alert('Done')
			
if __name__ == '__main__':
	main()