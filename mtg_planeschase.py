import wx, os, random
class Mtg_PC_App(wx.App):

	""" We simply derive a new class of Frame. """
	def __init__(self, redirect=False, filename=None):
		wx.App.__init__(self, redirect, filename)
		self.frame = wx.Frame(None, title="Magic, The Gathering - Planeschase!") 
		self.panel = wx.Panel(self.frame) 
		self.PhotoMaxSize = 1000
		self.shuffled = range(1, 87)
		random.shuffle(self.shuffled)
		self.currcard = 0
		self.played = []
		self.deckdata = open("pc_decklist.txt", "r")
		self.deck_list = self.deckdata.readlines()
		self.deckdata.close()
		print len(self.deck_list)
		# self.deck_list = [item.strip() for item in a]

		# IMAGE FILEPATHS
		self.cwd = os.getcwd()
		self.card_path = self.cwd + "\\mtg_pc_imgs\\mtg_pc_"+str(self.currcard)+".jpg"
		self.die_path = self.cwd + "\\mtg_pc_imgs\\die.jpg"
		self.donothing_path = self.cwd + "\\mtg_pc_imgs\\donothing.jpg"
		self.chaos_path = self.cwd + "\\mtg_pc_imgs\\chaos.jpg"
		self.planeswalk_path = self.cwd + "\\mtg_pc_imgs\\planeswalk.jpg"

		# INTIALIZE FRAME & WIDGETS
 		self.initializeWidgets()
		self.frame.Maximize()
		self.frame.Show()



	def initializeWidgets(self):
		img = self.Image(self.card_path, self.PhotoMaxSize)
		self.card = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(img))
		self.card_list = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)

		# NEXT & PREVIOUS BUTTONS
		self.next_btn = wx.Button(self.panel, 1, "NEXT CARD")
		self.prev_btn = wx.Button(self.panel, 1, "PREVIOUS CARD")
		self.next_btn.Bind(wx.EVT_BUTTON, self.onNext)
		self.prev_btn.Bind(wx.EVT_BUTTON, self.onPrev)

		self.next_sz = wx.BoxSizer(wx.HORIZONTAL)
		self.next_sz.Add(self.prev_btn, 1, wx.EXPAND)
		self.next_sz.Add(self.next_btn, 1, wx.EXPAND)
		

		# ROLL & RESET BUTTONS
		self.roll_btn = wx.Button(self.panel, -1, "ROLL DIE")
		self.reset_btn = wx.Button(self.panel, wx.ID_RESET, "RESHUFFLE")
		self.roll_btn.Bind(wx.EVT_BUTTON, self.onRoll)
		self.reset_btn.Bind(wx.EVT_BUTTON, self.onReset)


		self.reset_sz = wx.BoxSizer(wx.HORIZONTAL)
		self.reset_sz.Add(self.roll_btn, 1, wx.EXPAND)
		self.reset_sz.Add(self.reset_btn, 1, wx.EXPAND)


		self.btn_bay = wx.BoxSizer(wx.VERTICAL)
		self.btn_bay.Add(self.next_sz, 1, wx.EXPAND)
		self.btn_bay.Add(self.reset_sz, 1, wx.EXPAND)


		die_img = self.Image(self.die_path, 175)
		self.die = wx.StaticBitmap(self.panel, wx.ID_ANY, wx.BitmapFromImage(die_img), style = wx.SUNKEN_BORDER)
		self.counter = wx.SpinCtrl(self.panel, -1, style=wx.ALIGN_CENTRE_HORIZONTAL)
		counter_font = wx.Font(80, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		self.counter.SetFont(counter_font)
		self.counter_label = wx.StaticText(self.panel, label="COUNTERS", style=wx.ALIGN_CENTER)
		counter_label_font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
		self.counter_label.SetFont(counter_label_font)
		self.counter_box = wx.BoxSizer(wx.VERTICAL)
		self.counter_box.Add(self.counter, 1, wx.EXPAND)
		self.counter_box.Add(self.counter_label, 0, wx.EXPAND)


		self.disp_box = wx.BoxSizer(wx.HORIZONTAL)
		self.disp_box.Add(self.die, 1)
		self.disp_box.Add(self.counter_box, 1, wx.EXPAND)


		self.rightpane = wx.BoxSizer(wx.VERTICAL)
		self.rightpane.Add(self.card_list, 6, wx.EXPAND|wx.BOTTOM, border = 10)
		self.rightpane.Add(self.btn_bay, 2, wx.EXPAND|wx.BOTTOM, border =10)
		self.rightpane.Add(self.disp_box, 1, wx.EXPAND|wx.ALL)

		self.outer_box = wx.BoxSizer(wx.HORIZONTAL)
		self.outer_box.Add(self.card, 1, wx.EXPAND)
		self.outer_box.Add(self.rightpane, 1, wx.EXPAND)


		self.panel.SetSizer(self.outer_box)
		self.panel.SetAutoLayout(1)
		self.outer_box.Fit(self.frame)
		print help(wx.TextCtrl)


	def rescale(self, img, maxwidth):
		W = img.GetWidth()                               
		H = img.GetHeight()
		if W > H:
			NewW = maxwidth
			NewH = maxwidth * H / W
		else:
			NewH = maxwidth
			NewW = maxwidth * W / H
		return NewW, NewH

	def Image(self, filepath, maxwidth):
		img = wx.Image(filepath, wx.BITMAP_TYPE_ANY, wx.ALL)
		card_w, card_h = self.rescale(img, maxwidth)
		return img.Scale(card_w, card_h)


	def onNext(self, event):
		if len(self.shuffled) == 0:
			self.card_list.AppendText("No more cards left! Press 'RESHUFFLE' to Continue.\n")
			return

		self.played.append(self.currcard)
		self.currcard = self.shuffled.pop()
		self.card_path = self.cwd + "\\mtg_pc_imgs\\mtg_pc_"+str(self.currcard)+".jpg"
		img = self.Image(self.card_path, self.PhotoMaxSize)
		self.card.SetBitmap(wx.BitmapFromImage(img))
		self.card_list.AppendText(self.deck_list[self.currcard])
		self.panel.Refresh()
		return

	def onPrev(self, event):
		if len(self.played) == 0:
			self.card_list.AppendText("No more cards left to flip back! Press 'NEXT CARD' to Continue.\n")
			return

		self.shuffled.append(self.currcard)
		self.currcard = self.played.pop()
		self.card_path = self.cwd + "\\mtg_pc_imgs\\mtg_pc_"+str(self.currcard)+".jpg"
		img = self.Image(self.card_path, self.PhotoMaxSize)
		self.card.SetBitmap(wx.BitmapFromImage(img))
		self.card_list.AppendText(self.deck_list[self.currcard])
		self.panel.Refresh()
		return


	def onRoll(self, event):
		roll = random.randint(1,6)
		if roll == 1:
			self.card_list.AppendText("Planar Die Rolled CHAOS: Activate Additional Effect.\n")
			die_img = self.Image(self.chaos_path, 175)

		elif roll == 2:
			self.card_list.AppendText("Planar Die Rolled PLANESWALK: Press 'NEXT CARD' to Move On.\n")
			die_img = self.Image(self.planeswalk_path, 175)

		else:
			self.card_list.AppendText("Planar Die Rolled DO NOTHING: Sucks to be you.\n")
			die_img = self.Image(self.donothing_path, 175)

		self.die.SetBitmap(wx.BitmapFromImage(die_img))
		self.panel.Refresh()
		return

	def onReset(self, event):
		self.shuffled = range(1, 87)
		random.shuffle(self.shuffled)
		self.currcard = 0
		self.played = []

		self.card_path = self.cwd + "\\mtg_pc_imgs\\mtg_pc_"+str(self.currcard)+".jpg"
		img = self.Image(self.card_path, self.PhotoMaxSize)
		self.card.SetBitmap(wx.BitmapFromImage(img))
		self.card_list.Clear()
		self.card_list.AppendText("Deck Reshuffled. Press 'NEXT CARD' to Travel to a Plane.\n")
		self.panel.Refresh()
		return


if __name__ == '__main__':
	app = Mtg_PC_App()
	app.MainLoop()