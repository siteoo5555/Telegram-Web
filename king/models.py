from django.db import models
from django.contrib.auth.models import AbstractUser
# signals which is important to send code 💯
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import timedelta
import random

class User(AbstractUser):
    GENDER=(
        ('male','Male'),
        ('female','Female'),
        )
    AGE=(
        ('2013', '2013'),
        ('2012', '2012'),
        ('2011', '2011'),
        ('2010', '2010'),
        ('2009', '2009'),
        ('2008', '2008'),
        ('2007', '2007'),
        ('2006', '2006'),
        ('2005', '2005'),
        ('2004', '2004'),
        ('2003', '2003'),
        ('2002', '2002'),
        ('2001', '2001'),
        ('2000', '2000'),
        ('1999', '1999'),
        ('1998', '1998'),
        ('1997', '1997'),
        ('1996', '1996'),
        ('1995', '1995'),
        ('1994', '1994'),
        ('1993', '1993'),
        ('1992', '1992'),
        ('1991', '1991'),
        ('1990', '1990'),
        ('1989', '1989'),
        ('1988', '1988'),
        ('1987', '1987'),
        ('1986', '1986'),
        ('1985', '1985'),
    )
    COUNTRY = (
        ('Uzbekistan','🆄🆉🅱︎🅴🅺🅸🆂︎🆃🅰︎🅽'),
        ('afghanistan', 'Afghanistan'),
        ('albania', 'Albania'),
        ('algeria', 'Algeria'),
        ('american samoa', 'American Samoa'),
        ('andorra', 'Andorra'),
        ('angola', 'Angola'),
        ('anguilla', 'Anguilla'),
        ('anonymous numbers', 'Anonymous Numbers'),
        ('antigua & barbuda', 'Antigua & Barbuda'),
        ('argentina', 'Argentina'),
        ('armenia', 'Armenia'),
        ('aruba', 'Aruba'),
        ('australia', 'Australia'),
        ('austria', 'Autria'),
        ('azerbaijan', 'Azerbaijan'),
        ('bahamas', 'Bahamas'),
        ('bahrain', 'Bahrain'),
        ('bangladesh', 'Bangladesh'),
        ('barbados', 'Barbados'),
        ('belarus', 'Belarus'),
        ('belgium', 'Belgium'),
        ('belize', 'Belize'),
        ('benin', 'Benin'),
        ('bermuda', 'Bermuda'),
        ('bhutan', 'Bhutan'),
        ('bolivia', 'Bolivia'),
        ('bonaire, sint eustatius & saba', 'Bonaire, Bint Eustatius & Saba'),
        ('bosnia & herzegovina', 'Bosnia & Herzegovina'),
        ('botswana', 'Botswana'),
        ('brazil', 'Brazil'),
        ('british virgin islands', 'British Virgin Islands'),
        ('brunei darussalam','Brunei Darussalam'),
        ('bulgaria','Bulgaria'),
        ('burkina faso','Burkina Faso'),
        ('burundi','Burundi'),
        ('cambodia','Cambodia'),
        ('cameroon','Cameroon'),
        ('canada','Canada'),
        ('cape verde','Cape Verde'),
        ('cayman islands','Cayman Islands'),
        ('central african rep.','Central African Rep.'),
        ('chad','Chad'),
        ('chile','Chile'),
        ('china','China'),
        ('colombia','Colombia'),
        ('comoros','Comoros'),
        ('congo (dem. rep.)','Congo (Dem. Rep.)'),
        ('congo (rep.)','Congo (Rep.)'),
        ('cook islands','Cook Islands'),
        ('costa rica','Costa Rica'),
        ('côte d"ivoire','Côte d"ivoire'),
        ('croatia','Croatia'),
        ('Cuba','Cuba'),
        ('Curaçao','Curaçao'),
        ('Cyprus','Cyprus'),
        ('Czech Republic','Czech Republic'),
        ('Denmark','Denmark'),
        ('Diego Garcia','Diego Garcia'),
        ('Djibouti','Djibouti'),
        ('Dominica','Dominica'),
        ('Dominican Rep.','Dominican Rep.'),
        ('Ecuador','Ecuador'),
        ('Egypt','Egypt'),
        ('El Salvador','El Salvador'),
        ('Equatorial Guinea','Equatorial Guinea'),
        ('Eritrea','Eritrea'),
        ('Estonia','Estonia'),
        ('Eswatini','Eswatini'),
        ('Ethiopia','Ethiopia'),
        ('Falkland Islands','Falkland Islands'),
        ('Faroe Islands','Faroe Islands'),
        ('Fiji','Fiji'),
        ('Finland','Finland'),
        ('France','France'),
        ('French Guiana','French Guiana'),
        ('French Polynesia','French Polynesia'),
        ('Gabon','Gabon'),
        ('Gambia','Gambia'),
        ('Georgia','Georgia'),
        ('Germany','Germany'),
        ('Ghana','Ghana'),
        ('Gibraltar','Gibraltar'),
        ('Greece','Greece'),
        ('Greenland','Greenland'),
        ('Grenada','Grenada'),
        ('Guadeloupe','Guadeloupe'),
        ('Guam','Guam'),
        ('Guatemala','Guatemala'),
        ('Guinea','Guinea'),
        ('Guinea-Bissau','Guinea-Bissau'),
        ('Guyana','Guyana'),
        ('Haiti','Haiti'),
        ('Honduras','Honduras'),
        ('Hong Kong','Hong Kong'),
        ('Hungary','Hungary'),
        ('Iceland','Iceland'),
        ('India','India'),
        ('Indonesia','Indonesia'),
        ('Iran','Iran'),
        ('Iraq','Iraq'),
        ('Ireland','Ireland'),
        ('Italy','Italy'),
        ('Jamaica','Jamaica'),
        ('Japan','Japan'),
        ('Jordan','Jordan'),
        ('Kazakhstan','Kazakhstan'),
        ('Kenya','Kenya'),
        ('Kiribati','Kiribati'),
        ('Kosovo','Kosovo'),
        ('Kuwait','Kuwait'),
        ('Kyrgyzstan','Kyrgyzstan'),
        ('Laos','Laos'),
        ('Latvia','Latvia'),
        ('Lebanon','Lebanon'),
        ('Lesotho','Lesotho'),
        ('Liberia','Liberia'),
        ('Libya','Libya'),
        ('Liechtenstein','Liechtenstein'),
        ('Lithuania','Lithuania'),
        ('Luxembourg','Luxembourg'),
        ('Macau','Macau'),
        ('Madagascar','Madagascar'),
        ('Malawi','Malawi'),
        ('Malaysia','Malaysia'),
        ('Maldives','Maldives'),
        ('Mali','Mali'),
        ('Malta','Malta'),
        ('Marshall Islands','Marshall Islands'),
        ('Martinique','Martinique'),
        ('Mauritania','Mauritania'),
        ('Mauritius','Mauritius'),
        ('Mexico','Mexico'),
        ('Micronesia','Micronesia'),
        ('Moldova','Moldova'),
        ('Monaco','Monaco'),
        ('Mongolia','Mongolia'),
        ('Montenegro','Montenegro'),
        ('Montserrat','Montserrat'),
        ('Morocco','Morocco'),
        ('Mozambique','Mozambique'),
        ('Myanmar','Myanmar'),
        ('Namibia','Namibia'),
        ('Nauru','Nauru'),
        ('Nepal','Nepal'),
        ('Netherlands','Netherlands'),
        ('New Caledonia','New Caledonia'),
        ('New Zealand','New Zealand'),
        ('Nicaragua','Nicaragua'),
        ('Niger','Niger'),
        ('Nigeria','Nigeria'),
        ('Niue','Niue'),
        ('Norfolk Island','Norfolk Island'),
        ('North Korea','North Korea'),
        ('North Macedonia','North Macedonia'),
        ('Northern Mariana Islands','Northern Mariana Islands'),
        ('Norway','Norway'),
        ('Oman','Oman'),
        ('Pakistan','Pakistan'),
        ('Palau','Palau'),
        ('Palestine','Palestine'),
        ('Panama','Panama'),
        ('Papua New Guinea','Papua New Guinea'),
        ('Paraguay','Paraguay'),
        ('Peru','Peru'),
        ('Philippines','Philippines'),
        ('Poland','Poland'),
        ('Portugal','Portugal'),
        ('Puerto Rico','Puerto Rico'),
        ('Qatar','Qatar'),
        ('Réunion','Réunion'),
        ('Romania','Romania'),
        ('Russian Federation','Russian Federation'),
        ('Rwanda','Rwanda'),
        ('Saint Helena','Saint Helena'),
        ('Saint Kitts & Nevis','Saint Kitts & Nevis'),
        ('Saint Lucia','Saint Lucia'),
        ('Saint Pierre & Miquelon','Saint Pierre & Miquelon'),
        ('Saint Vincent & the GrenadinesSamoa','Saint Vincent & the GrenadinesSamoa'),
        ('Samoa','Samoa'),
        ('San Marino','San Marino'),
        ('São Tomé & Príncipe','São Tomé & Príncipe'),
        ('Saudi Arabia','Saudi Arabia'),
        ('Senegal','Senegal'),
        ('Serbia','Serbia'),
        ('Seychelles','Seychelles'),
        ('Switzerland','Switzerland'),
        ('Tajikistan','Tajikistan'),
        ('Tanzania','Tanzania'),
        ('Thailand','Thailand'),
        ('Timor-Leste','Timor-Leste'),
        ('Togo','Togo'),
        ('Trinidad & Tobago','Trinidad & Tobago'),
        ('Turkmenistan','Turkmenistan'),
        ('Turks & Caicos Islands','Turks & Caicos Islands'),
        ('Tuvalu','Tuvalu'),
        ('Uzbekistan','Uzbekistan'),
        ('USA','USA'),
        ('US Virgin Islands','US Virgin Islands'),
        ('Uruguay','Uruguay'),
        ('United Kingdom','United Kingdom'),
        ('United Arab Emirates','United Arab Emirates'),
        ('Vanuatu','Vanuatu'),
        ('Venezuela','Venezuela'),
        ('Vietnam','Vietnam'),
        ('Wallis & Futuna','Wallis & Futuna'),
        ('Yemen','Yemen'),
        ('Zambia','Zambia'),
        ('Zimbabwe','Zimbabwe'),

    )
    gender=models.CharField(max_length=10,choices=GENDER,default='male')
    country = models.CharField(max_length=35, choices=COUNTRY,default='🆄🆉🅱︎🅴🅺🅸🆂︎🆃🅰︎🅽')
    address = models.CharField(max_length=70)
    age = models.CharField(max_length=6, choices=AGE,default='2010')
    active=models.BooleanField(default=False)
    email = models.EmailField(max_length=50)
    phone_number=models.PositiveBigIntegerField(default='+998')

class Confirmation(models.Model):
    code=models.IntegerField(null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_codes')
    expired_time=models.DateTimeField(null=True) #15:30
    STATUS=(
        ("amalda", "Amalda"),
        ("checked", "Checked"),
        ("expired", "Expired"),
    )
    status=models.CharField(max_length=20, choices=STATUS, default="amalda")

    def str(self) -> str:
        return f'{self.user.username}-{self.code}'

    def is_expired(self):
        return self.expired_time < timezone.now()

@receiver(post_save, sender=User)
def create_confirmation_code(sender, instance, created, **kwargs):
    if created:
        c = Confirmation.objects.create(
            user=instance
        )
        code = ''
        for i in range(5):
            code +=  str(random.randint(1,9))
        c.code = int(code)
        c.expired_time =  timezone.now() + timedelta(minutes=5)
        c.save()
        return True

class Chat(models.Model):
    TUR = (
        ('channel', 'CHANNEL'),
        ('group', 'GROUP'),
        ('chatting', 'CHATTING'),
    )
    description = models.TextField(default='Input Description')
    name = models.CharField(max_length=50, null=True)
    tur = models.CharField(max_length=25, choices=TUR, default='chatting')
    photo = models.ImageField(upload_to='chat/images/', null=True, blank=True)
    members = models.ManyToManyField(User, related_name='chat_members')
    Admin = models.ForeignKey(User, related_name='Admin', on_delete=models.CASCADE, null=True, blank=True)
    Admins = models.ManyToManyField(User, related_name='Admins')
    def str(self):
        return self.status
    @property
    def unread_sms(self):
        soni = self.messages.filter(is_read=False).count()
        return soni

class Chat_Link(models.Model):
    chat=models.OneToOneField(Chat,on_delete=models.CASCADE,related_name='chat_url')
    url=models.TextField()



class Profile(models.Model):
    username = models.CharField(max_length=10)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    birthday = models.CharField(max_length=90,null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True ,blank=True)
    bio = models.CharField(max_length=250, null=True, blank=True)

@receiver(post_save,sender=User)
def create(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
        )
class Photo(models.Model):
    image=models.ImageField(upload_to='telegram/user/',  null=True, blank=True)
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_images')


class Messages(models.Model):
    TUR = (
        ('text', 'Text'),
        ('rasm', 'Rasm'),
    )
    message_type = models.CharField(max_length=30, choices=TUR, default='text')
    sms = models.TextField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_messages')
    created = models.TimeField(auto_now_add=True)
    photo=models.ImageField(upload_to='images/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    is_read=models.BooleanField(default=False,null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_messages')
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'