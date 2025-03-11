from django.shortcuts import render,redirect, HttpResponseRedirect
from django.core.mail import send_mail
from .forms import *
from .models import *
from django.contrib.auth import  authenticate,login,logout
from django.contrib import messages
from django.conf import settings
from django.views import View
from django.urls import reverse
import string
import random



def Login(request):
    form = LoginForm()
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            parol = form.cleaned_data['password']
            user = authenticate(request, username=username, password=parol)
            if user is not None:
                login(request, user)
                messages.success(request, f"{user.username}, login qilindingiz!")
                return redirect('captcha')
        messages.error(request, "Usernameㅤorㅤpasswordㅤisㅤwrong")
    return render(request, 'login.html', {'form': form})

class Home(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return Login(request)
        chats = Chat.objects.all()
        search = request.GET.get('search')
        chat = None
        id = request.GET.get('id')
        if id:
            chat = Chat.objects.get(id=id)
            for i in chat.chat_messages.all():
                if not i.user==request.user:
                    i.is_read=True
                    i.save()

            a=[]
            for i in chats:
                if i.Admin == request.user or  request.user in i.Admins.all() or request.user in i.members.all():
                    a.append(i)
            if a:
                chats=a
            if search:
                chats=Chat.objects.filter(name__icontains=search)
            chats=chats[::-1]
        return render(request, 'home.html',{'chats':chats,'chat':chat})

    def post(self, request):
        if request.user.is_authenticated:
            sms = request.POST.get('sms')
            chat_id = request.POST.get('id')
            if chat_id:
                if sms:
                    Messages.objects.create(
                        sms = sms,
                        user = request.user,
                        chat = Chat.objects.get(id=int(chat_id))
                    )
                return redirect(reverse('home') + f'?id={chat_id}')
            azo = request.POST.get('azo')
            if azo:
                chat = Chat.objects.get(id=azo)
                chat.members.add(request.user)
                chat.save()
            return redirect(reverse('home') + f'?chat_id={azo}')
        return Login(request)

def delete_sms(request,id,message_id):
    sms=Messages.objects.get(id=message_id)
    sms.delete()
    chat=Chat.objects.get(id=id)
    chats=Chat.objects.all()
    return render(request,'home.html',{'chat':chat,'chats':chats})


def register(request):
    startswith_is_required=('+92','+998','+93','+964','+98','+355','+213','+1-684','+376','+244','+1-264','+672','+1-268','+54','+374','+297','+61','+43','+994','+1-242','+973','+880','+1-246','+375','+32','+501','+229','+1','+971','+44','+681','+263','+260','+967','+993')
    r = UserForm()
    if request.POST:
        r = UserForm(request.POST)
        if r.is_valid():
            user = r.save()
            parol = r.cleaned_data['password']
            user.set_password(parol)
            user.save()
            return redirect('cap')
    return render(request, 'user.html', {'r': r})
class Confirm(View):
    def get(self, request):
        return render(request, 'confirm.html')
    def post(self, request):
        code = request.POST.get('code', 0)
        if code:
            a=request.user.user_codes.last()
            if a.code == int(code) and a.expired_time>=timezone.now():
                request.user.active=True
                request.user.save()
                messages.success(request, s='You are confirmed!👍👌')

                return redirect('home')
            else:
                messages.info(request, 'There is error code :)😐')
        else:
            messages.info(request, 'Your email is invalid!😐')
        
class Create_Group(View):
    def get(self, request):
        form = ChatNameForm()
        return render(request, 'name.html', {'form':form})
    def post(self, request):
            form = ChatNameForm(request.POST)
            if form.is_valid():
                group = form.save(commit=False)
                group.tur = 'guruh'
                group.save()
                return redirect('add', group.id)

class Add_Members(View):
    def get(self, request, id):
        form = ChatMembersForm()
        return render(request, 'add.html', {'form': form})
    def post(self, request, id):
        chat = Chat.objects.get(id=id)
        form = ChatMembersForm(request.POST)
        if form.is_valid():
            azolar = request.POST.getlist('members')
            for i in azolar:
                user = User.objects.get(id=i)
                chat.members.add(user)
            chat.save()
        return redirect(reverse('home') + f'?id={id}')

class Remove_Members(View):
    def get(self, request, id):
        form = ChatMembersForm()
        return render(request, 'remove.html', {'form': form})
    def post(self, request, id):
        chat = Chat.objects.get(id=id)
        form = ChatMembersForm(request.POST)
        if form.is_valid():
            azolar = request.POST.getlist('members')
            for i in azolar:
                user = User.objects.get(id=i)
                chat.members.remove(user)
            chat.save()
        return redirect(reverse('home') + f'?id={id}')

class Create_Channel(View):
    def get(self, request):
        form = ChatNameForm()
        return render(request, 'channel.html', {'form':form})
    def post(self, request):
        form = ChatNameForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.tur = 'guruh'
            group.save()
            return redirect('add', group.id)
class Change_Password(View):
    def get(self, request):
        form = PasswordForm()
        return render(request, 'change.html', {'form': form})
    def post(self, request):
        form = PasswordForm(request.POST)
        p_1 = form.data['old_password']
        p_2 = form.data['new_password']
        user = request.user
        if user.check_password(p_1):
            user.set_password(p_2)
            user.save()
        return redirect('home')
class User_Edit(View):
    def get(self, request):
        form = UserEditForm(instance=request.user)
        return render(request, 'user_edit.html', {'form': form})
    def post(self, request):
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')

class Profile_Edit(View):
    def get(self, request):
        form = UserEditForm(instance=request.user)
        return render(request, 'user_edit.html', {'form': form})
    def post(self, request):
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')


def create_profile(request):
    form = ProfileForm()
    if request.POST:
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

def calculator(request):
    ...
    return render(request, 'calc.html')
def dino(request):
    ...
    return render(request, 'dino.html')

def spinner(request):
    ...
    return render(request, 'spin.html')

def multiplayer_snake_game(request):
    ...
    return render(request, 'multiplayer_snake.html')


def detect_device_battery(request):
    ...
    return render(request, 'detect_device_battery.html')


def flip_coin_game(request):
    ...
    return render(request, 'flip_coin_game.html')



def dictionary_app(request):
    ...
    return render(request, 'dictionary.html')


def qr_code(request):
    ...
    return render(request, 'qr_code.html')

def music_app(request):
    return render(request, 'music.html')


def geometric_art_generator(request):
    ...
    return render(request, 'geometric_art_generator.html')

def rich_text_editor(request):
    ...
    return render(request, 'rich_text_editor.html')

def budget_app(request):
    ...
    return render(request, 'budget_app.html')


def password_generator(request):
    ...
    return render(request, 'pass_generator.html')


def to_do_app(request):
    ...
    return render(request, 'to_do_app.html')

def nitro_race(request):
    ...
    return render(request, 'nitro_race.html')

def bike_race(request):
    ...
    return render(request, 'bike_race.html')

def slice_fruit(request):
    ...
    return render(request, 'slice_fruit.html')

def weather(request):
    ...
    return render(request, 'weather.html')
def help(request):
    return render(request, 'help.html')
def quiz(request):
    ...
    return render(request, 'quest.html')

def tower_block(request):
    ...
    return render(request, 'tower_blocks.html')

def archery_game(request):
    ...
    return render(request, 'archery.html')

def tilting_maze_game(request):
    ...
    return render(request, 'maze_game.html')

def color_captcha(request):
    ...
    return render(request, 'verification.html')


def code_editor(request):
    ...
    return render(request, 'code_editor.html')


def our_team(request):
    ...
    return render(request, 'our_team.html')


def pixel_art_generator(request):
    ...
    return render(request, 'pixel_art_generator.html')

def maze(request):
    ...
    return render(request, 'maze.html')

def stick_hero_game(request):
    ...
    return render(request, 'stick_hero.html')

def flappy(request):
    ...
    return render(request, 'flappy.html')

def gozilla_game(request):
    ...
    return render(request, 'gozilla.html')

def country_guide(request):
    ...
    return render(request, 'country_guide.html')

def text_to_speech(request):
    ...
    return render(request, 'text_to_speech.html')

def spiderman_game(request):
    ...
    return render(request, 'spider_man.html')

def stop_watch(request):
    ...
    return render(request, 'stop_watch.html')

def zombie_shooter(request):
    ...
    return render(request, 'zombie.html')

def predict_gender(request):
    ...
    return render(request, 'predict_gender.html')

def tetris(request):
    ...
    return render(request, 'tetris.html')

def typing_test(request):
    ...
    return render(request, 'typing.html')

def piano_game(request):
    ...
    return render(request, 'piano.html')

def coronavirus(request):
    ...
    return render(request, 'coronavirus.html')

def tic_tac_toe(request):
    ...
    return render(request, 'tic.html')

def flappy_bird(request):
    ...
    return render(request, 'stack.html')
def cap(request):
    ...
    return render(request, 'custom.html')
def error(request):
    ...
    return render(request, 'error.html')

def memory(request):
    ...
    return render(request, 'memory.html')

def pinball(request):
    ...
    return render(request, 'ball.html')

def mouse_tap(request):
    ...
    return render(request, 'tap.html')

def snake(request):
    ...
    return render(request, 'snake.html')

def chatbot(request):
    ...
    return render(request, 'chatbot.html')


def shadow_generator(request):
    ...
    return render(request, 'shadow_generator.html')

def translator(request):
    ...
    return render(request, 'translate.html')

def monster_match_game(request):
    ...
    return render(request, 'monster_match.html')

def hot_air_balloon(request):
    ...
    return render(request, 'hot_air_balloon.html')


def basketball_game(request):
    ...
    return render(request, 'basketball.html')

def gravity_botz_game(request):
    ...
    return render(request, 'gravity.html')

def cat_stack_game(request):
    ...
    return render(request, 'cat_stack.html')

def hockey(request):
    ...
    return render(request, 'hockey.html')

def flight_academy_game(request):
    ...
    return render(request, 'flight_academy.html')

def drift_derby_game(request):
    ...
    return render(request, 'drift_derby.html')

def burger_shack_stack_game(request):
    ...
    return render(request, 'burger_shack_stack.html')

def massive_word_search_game(request):
    ...
    return render(request, 'massive_word_search.html')

def extreme_ride_game(request):
    ...
    return render(request, 'extreme_ride.html')

def moster_truck_challenge_game(request):
    ...
    return render(request, 'monster_truck_challenge.html')

def table_tennis_cup_game(request):
    ...
    return render(request, 'table_tennis_cup.html')

def mini_derby_game(request):
    ...
    return render(request, 'mini_derby.html')

def cat_attack(request):
    ...
    return render(request, 'cat_attack.html')

def tools_and_games(request):
    ...
    return render(request, 'tools_and_games.html')

def camping_crush(request):
    ...
    return render(request, 'camping_crush.html')

def car(request):
    ...
    return render(request, 'car.html')
def bubble(request):
    ...
    return render(request, 'bubble.html')
def gun_shooter(request):
    ...
    return render(request, 'shooter.html')
def secure(request):
    ...
    return render(request, 'invisible.html')

def google_captcha(request):
    ...
    return render(request, 'google.html')

def alien_castle(request):
    ...
    return render(request, 'alien_castle.html')

def captcha_next(request):
    ...
    return render(request, 'captcha1.html')

def cross_road(request):
    ...
    return render(request, 'cross.html')

def candy_crush(request):
    ...
    return render(request, 'candy.html')


def space_defense(request):
    ...
    return render(request, 'defense.html')

def wizard_westy_game(request):
    ...
    return render(request, 'wizard_westy.html')

def wikipedia_searcher(request):
    ...
    return render(request, 'wikipedia_searcher.html')

def image_color_picker(request):
    ...
    return render(request, 'image_color_picker.html')


def detect_internet_speed(request):
    ...
    return render(request, 'detect_internet_speed.html')

def url_shortener(request):
    ...
    return render(request, 'url_shortener.html')


def matching(request):
    ...
    return render(request, 'matching.html')


def rock_paper_scissors(request):
    ...
    return render(request, 'scissor.html')

def sliding_tile_puzzle(request):
    ...
    return render(request, 'sliding_tile_puzzle.html')

def sonic(request):
    ...
    return render(request, 'sonic.html')

def space_invaders(request):
    ...
    return render(request, 'space.html')

class Create_Profile(View):
    def get(self, request):
        form = ProfileForm()
        return render(request, 'profile.html', {'form':form})
    def post(self, request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')



def profile_image_create(request):
    form=PhotoForm()
    if request.POST:
        form=PhotoForm(request.POST,request.FILES)
        if form.is_valid():
            p=Profile.objects.get(user=request.user)
            Photo.objects.create(
                Profile=p,
                image=form.cleaned_data['image']
            )
            imgs=Photo.objects.all()
            return render(request,'imgs.html',{'imgs':imgs,'form':form})
    return render(request,'imgs.html',{'imgs':imgs,'form':form})


def profile_image_delete(request,id):
    photo=Photo.objects.get(id=id)
    photo.delete()
    return redirect('profile_img_create')


class Create_Friend_Chat(View):
    def get(self, request):
        users=User.objects.all()
        return render(request,'friend.html',{'users':users})
    def post(self, request):
        form=Create_Friend_ChatForm(request.POST,files=request.FILES)
        user=User.objects.get(id = id)
        if form.is_valid:
            chat = Chat.objects.create(
            status='Friends'
            )
            chat.members.add(request.user)
            chat.members.add(user)
            chat.save()
            return redirect('home')

def about(request):
    ...
    return render(request, 'icons.html')


def Logout(request):
    logout(request)
    return redirect('home')


def create_chat_link(request,id):
    chat = Chat.objects.get(id=id)
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
    a = 'http://127.0.0.1:8000/'+random_string+'www.com'
    Chat_Link.objects.create(
        chat=chat,
        url=a
    )
    return redirect('home')

def delete_sms(request,id,sms_id):
    sms=Messages.objects.get(id=sms_id)
    sms.delete()
    chat=Chat.objects.get(id=id)
    chats=Chat.objects.all()
    return render(request,'home.html',{'chat':chat,'chats':chats})



def edit_function(request, sen):
    news =Chat.objects.get(id=sen)
    form = ChatNameForm(instance=news)
    if request.POST:
        form = ChatNameForm(request.POST, files=request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'edit.html', {'form': form})

def delete(request, me):
    chat_delete = Chat.objects.get(id=me)
    chat_delete.delete()
    return redirect('home')




            # send_mail(
            #     f'Salom, {a.username}',
            #     f'Sizning tasdiqlash kodingiz - {a.user_codes.last().code}',
            #     settings.EMAIL_HOST_USER,
            #     [a.email],
            #     fail_silently=False
            # )
            # messages.info(request, 'Sizga kod yubordik')


# def create_chat_f(request):
#     users=User.objects.all()
#     if request.GET:
#         user=User.objects.get(id = id)
#         if request.POST:
#             form=Create_Friend_ChatForm(request.POST,files=request.FILES)
#             if form.is_valid():
#                 chat = Chat.objects.create(
#                     status='Friends'
#                 )
#                 chat.members.add(request.user)
#                 chat.members.add(user)
#                 chat.save()
#                 return redirect('home')
#         return render(request,'friend.html',{'users':users})
# class Users(View):
#     def get(self, request):
#         r = UserForm()
#         return render(request, 'user.html', {'r': r})
#     def post(self, request):
#         r = UserForm(request.POST)
#         if r.is_valid():
#             a = r.save(commit=False)
#             a.set_password(r.cleaned_data['password'])
#             a.save()
#             login(request, a)
#             send_mail(
#                 f'Salom, {a.username}',
#                 f'Sizning tasdiqlash kodingiz - {a.user_codes.last().code}',
#                 settings.EMAIL_HOST_USER,
#                 [a.email],
#                 fail_silently=False
#             )
#             messages.info(request, 'Sizga kod yubordik')
#             return redirect('home')



# old function

# def user_edit(request):
#     form = UserEditForm(instance=request.user)
#     if request.POST:
#         form = UserEditForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     return render(request, 'user_edit.html', {'form': form})


# old function

# def change_password(request):
#     form = PasswordForm()
#     if request.POST:
#         form = PasswordForm(request.POST)
#         p_1 = form.data['password_1']
#         p_2 = form.data['password_2']
#         user = request.user
#         if user.check_password(p_1):
#             user.set_password(p_2)
#             user.save()
#             return redirect('home')
    # return render(request, 'change.html', {'form': form})

# old function

# def login(request):
#     form = LoginForm()
#     if request.POST:
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             a = request.POST['username']
#             b = request.POST['password']
#             f = authenticate(request, username=a, password=b)
#             print(f)
#             if f is not None:
#                 login(request, f)
#                 return redirect('home')
#     return render(request, "index.html", {'form': form})



# old function

# def create_channel(request):
#     form = ChatNameForm()
#     if request.POST:
#         form = ChatNameForm(request.POST)
#         if form.is_valid():
#             group = form.save(commit=False)
#             group.tur = 'guruh'
#             group.save()
#             return redirect('add', group.id)
#     return render(request, 'channel.html', {'form':form})

# def add_members(request, id):
#     chat = Chat.objects.get(id=id)
#     form = ChatMembersForm()
#     if request.POST:
#         form = ChatMembersForm(request.POST)
#         if form.is_valid():
#             azolar = request.POST.getlist('members')
#             for i in azolar:
#                 user = User.objects.get(id=i)
#                 chat.members.add(user)
#             chat.save()
#             return redirect('home')
#     return render(request, 'add.html', {'form': form})



# old function

# def create_group(request):
#     form = ChatNameForm()
#     if request.POST:
#         form = ChatNameForm(request.POST)
#         if form.is_valid():
#             group = form.save(commit=False)
#             group.tur = 'guruh'
#             group.save()
#             return redirect('add', group.id)
#     return render(request, 'name.html', {'form':form})




# old function

# def home(request):
#     chats = Chat.objects.all()
#     chat = None
#     if request.GET:
#         id = request.GET.get('chat_id')
#         chat = Chat.objects.get(id=id)
#     if request.POST:
#         sms = request.POST.get('sms')
#         chat_id = request.POST.get('chat_id')
#         Messages.objects.create(
#             sms = sms,
#             user = request.user,
#             chat = Chat.objects.get(id=int(chat_id))
#         )
#     return render(request, 'home.html', {'chats': chats, 'chat': chat})





# old function
# def confirm(request):
#     if request.POST:
#         code = request.POST.get('code', 0)
#         if code:
#             a=request.user.user_codes.last()
#             if a.code == int(code) and a.expired_time>=timezone.now():
#                 request.user.active=True
#                 request.user.save()
#                 messages.success(request, 'Siz tasdiqlandingiz  !')

#                 return redirect('home')
#             messages.warning(request, 'Sizda xato kod bor :)')
#     return render(request, 'confirm.html')



#like
            # sms_id = request.POST.get['one']
            # sms_id = Messages.objects.get(id=sms_id)
            # if request.user in sms_id.likes.all():
            #     sms_id.likes.remove(request.user)
            # else:
            #     sms_id.likes.add(request.user)    