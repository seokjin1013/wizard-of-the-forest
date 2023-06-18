from dataclasses import dataclass
import ww

@dataclass()
class Status:
    atk = 4
    atk_firerate = 6
    speed = 8
    mhp = 100
    atk_velocity = 40
    atk_duration = 20
    crit = 0.05
    crit_atk = 1.5
    gold_earn = 1.0

class Item:
	pass

items_tier3_name = [
	'토파즈',
	'정제된 토파즈',
	'루비',
	'정제된 루비',
	'크리스탈',
	'정제된 에메랄드',
	'에메랄드',
	'양초',
	'구리주괴',
	'흑요석',
	'은주괴',
	'다이아몬드',
	'진주',
	'정제된 사파이어',
	'횃불'
]

items_tier3_info = [
	['공격력+1'],
	['공격력+5%'],
	['체력+10'],
	['체력+5%'],
	['공격속도+10%'],
	['투사체', '속도+10%'],
	['투사체', '체공시간+10%'],
	['투사체', '체공시간-15%', '공격속도+15%'],
	['투사체', '속도-15%', '공격력+10%'],
	['적 처치시', '체력회복+1'],
	['공격속도+6%'],
	['치명타', '확률+8%'],
	['치명타', '데미지+5%'],
	['이속+10%'],
	['범위 100 내에', '적에게 입히는', '피해 증가 20%']
]

class ItemTier3(Item):
	def __init__(self, num):
		self.num = num

	@property
	def name(self):
		return items_tier3_name[self.num]

	@property
	def info(self):
		return items_tier3_info[self.num]

	@property
	def image(self):
		return ww.sprites['items_tier3'][self.num]

	@property
	def tier(self):
		return 3

	def rect(self, **kwargs):
		return ww.sprites['items_tier3'][0].get_rect(**kwargs)