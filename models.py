from django.db import models
from django.db.utils import OperationalError
try:
  from gearitem.models import GearItem, Gem
except:
  pass

from calcs.tools import RACES, SPECS, REGIONS, SERVERS, TIER1, TIER2, TIER3, TIER4, TIER5, TIER6, TIER7

tier1=[(TIER1.index(t),t) for t in TIER1]
tier2=[(TIER2.index(t),t) for t in TIER2]
tier3=[(TIER3.index(t),t) for t in TIER3]
tier4=[(TIER4.index(t),t) for t in TIER4]
tier5=[(TIER5.index(t),t) for t in TIER5]
tier6=[(TIER6.index(t),t) for t in TIER6]
tier7=[(TIER7.index(t),t) for t in TIER7]

class HunterModel(models.Model):
    race = models.IntegerField(default=4, # Night Elf
                            choices=RACES,
                            max_length=20)
    spec = models.IntegerField(default=0,
                               verbose_name="Specialization",
                               choices=SPECS)
    talent4 = models.IntegerField(default=tier4[0],
                               verbose_name="Talents - level 60",
                               choices=tier4,max_length=30)
    talent5 = models.IntegerField(default=tier5[0],
                               verbose_name="Talents - level 75",
                               choices=tier5,max_length=30)
    talent6 = models.IntegerField(default=tier6[0],
                               verbose_name="Talents - level 90",
                               choices=tier6,max_length=30)
    talent7 = models.IntegerField(default=tier7[0],
                               verbose_name="Talents - level 100",
                               choices=tier7,max_length=30)

class ArmoryModel(models.Model):
    region = models.CharField(choices=REGIONS,
                              default='us',
                              max_length=30)
    server = models.CharField(choices=SERVERS,
                              default='whisperwind',
                              max_length=30)
    character = models.CharField(max_length=30)
    spec = models.BooleanField(default=True,
                               verbose_name="Use first spec")

class BMOptionsModel(models.Model):
    opt_bm3 = models.BooleanField(default=True,
                         verbose_name="Hold Bestial Wrath until KC is ready",)
    opt_bm4 = models.BooleanField(default=False,
                         verbose_name="Do not cast Dire Beast during Bestial Wrath",)
    opt_bm5 = models.BooleanField(default=True,
                         verbose_name="Do not cast Focus Fire during Bestial Wrath",)
    opt_bm6 = models.BooleanField(default=True,
                         verbose_name="Cast Focus Fire just before Bestial Wrath",)
                        
  

carefulaim_choices=[(0,'Aimed Shot only'),
                    (1,'Aimed Shot and talents (no Chimaera)'),
                    (2,'No restrictions'),
                   ]
class MMOptionsModel(models.Model):
    opt_mm1 = models.IntegerField(default=2,
                               verbose_name="Careful Aim behavior",
                               choices=carefulaim_choices,max_length=30)
    opt_mm2 = models.IntegerField(default=0,
                         verbose_name="Aimed Shot - min focus (plus cost) to use",
                         max_length=3)
    opt_mm3 = models.BooleanField(default=True,
                         verbose_name="Only cast instant shots after Focusing Shot")

class SVOptionsModel(models.Model):
    opt_sv2 = models.BooleanField(default=True,
                         verbose_name="Null action - place holder")

class AOEOptionsModel(models.Model):
    opt_aoe1 = models.IntegerField(default=8,
                         verbose_name="Targets",
                         max_length=2)
    opt_aoe2 = models.BooleanField(default=True,
                         verbose_name="Cast main nukes")
    opt_aoe3 = models.IntegerField(default=0,
                         verbose_name="Min focus to cast main nukes",
                         max_length=3)


def slot_maker(*args):
  try:
    itms = GearItem.objects.filter(slot__in=args).order_by('name')
    options = [('','(None equipped)')]
    options.extend([(itm,itm) for itm in itms])
    return options
  except: # if table doesn't exist yet
    return []
  
head_slots = slot_maker(1)
neck_slots = slot_maker(2)
shoulder_slots = slot_maker(3)
back_slots = slot_maker(16)
chest_slots = slot_maker(5)
wrists_slots = slot_maker(9)
hands_slots = slot_maker(10)
waist_slots = slot_maker(6)
legs_slots = slot_maker(7)
feet_slots = slot_maker(8)
ring_slots = slot_maker(11)
trinket_slots = slot_maker(12)
weapon_slots = slot_maker(15,26)

difficulty_options = (('normal','Normal/None'),
                      ('heroic','Heroic'),
                      ('mythic','Mythic'),)


try:
  gem_choices = [('','(None)')]+[(g.id,g.name) for g in Gem.objects.all().order_by('id')]
except:
  gem_choices = [('','(None)')]

class GearEquipModel(models.Model):
    weapon = models.CharField(choices=weapon_slots,
                            default='Crystalline Branch of the Brackenspore',
                            max_length=30)
    weapon_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    weapon_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    weapon_warforged = models.BooleanField(default=False,)

    head = models.CharField(choices=head_slots,
                            default='Gronn-Skin Crown',
                            max_length=30)
    head_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    head_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    head_warforged = models.BooleanField(default=False,)

    neck = models.CharField(choices=neck_slots,
                            default='Reaver\'s Nose Ring',
                            max_length=30)
    neck_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    neck_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    neck_warforged = models.BooleanField(default=False,)

    shoulders = models.CharField(choices=shoulder_slots,
                            default='Living Mountain Shoulderguards',
                            max_length=30)
    shoulders_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    shoulders_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    shoulders_warforged = models.BooleanField(default=False,)

    back = models.CharField(choices=back_slots,
                            default='Cloak of Creeping Necrosis',
                            max_length=30)
    back_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    back_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    back_warforged = models.BooleanField(default=False,)

    chest = models.CharField(choices=chest_slots,
                            default='Moss-Woven Mailshirt',
                            max_length=30)
    chest_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    chest_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    chest_warforged = models.BooleanField(default=False,)

    wrists = models.CharField(choices=wrists_slots,
                            default='Bracers of the Crying Chorus',
                            max_length=30)
    wrists_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    wrists_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    wrists_warforged = models.BooleanField(default=False,)

    hands = models.CharField(choices=hands_slots,
                            default='Grips of Vicious Mauling',
                            max_length=30)
    hands_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    hands_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    hands_warforged = models.BooleanField(default=False,)

    waist = models.CharField(choices=waist_slots,
                            default='Belt of Imminent Lies',
                            max_length=30)
    waist_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    waist_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    waist_warforged = models.BooleanField(default=False,)

    legs = models.CharField(choices=legs_slots,
                            default='Leggings of Broken Magic',
                            max_length=30)
    legs_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    legs_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    legs_warforged = models.BooleanField(default=False,)

    feet = models.CharField(choices=feet_slots,
                            default='Face Kickers',
                            max_length=30)
    feet_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    feet_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    feet_warforged = models.BooleanField(default=False,)

    ring1 = models.CharField(choices=ring_slots,
                            default='Flenser\'s Hookring',
                            max_length=30)
    ring1_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    ring1_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    ring1_warforged = models.BooleanField(default=False,)

    ring2 = models.CharField(choices=ring_slots,
                            default='Spell-Sink Signet',
                            max_length=30)
    ring2_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    ring2_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    ring2_warforged = models.BooleanField(default=False,)

    trinket1 = models.CharField(choices=trinket_slots,
                            default='Captive Micro-Aberration',
                            max_length=30)
    trinket1_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    trinket1_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    trinket1_warforged = models.BooleanField(default=False,)

    trinket2 = models.CharField(choices=trinket_slots,
                            default='Scales of Doom',
                            max_length=30)
    trinket2_difficulty = models.CharField(choices=difficulty_options,
                            default='',
                            max_length=30)
    trinket2_socket = models.CharField(choices=gem_choices,
                            default='',
                            max_length=30)
    trinket2_warforged = models.BooleanField(default=False,)
