from django.shortcuts import render, redirect, get_object_or_404
from aa_app.models import *
from django.contrib import messages
from django.db.models import Q


# ──────────────────────────────────────────
# Admin / Portal Views
# ──────────────────────────────────────────

def portal(request):
    if request.method == 'POST':
        pid      = request.POST['id']
        password = request.POST['password']
        obj = Portal.objects.filter(pid=pid, password=password)
        if obj:
            request.session['session_key']  = pid
            request.session['session_role'] = 'admin'
            messages.success(request, 'Logged In')
            return redirect('portal_home')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'portal/login.html')
    else:
        return render(request, 'portal/login.html')


def portal_home(request):
    pid = request.session.get('session_key')
    role = request.session.get('session_role')
    if pid and role == 'admin':
        try:
            user = Portal.objects.get(pid=pid)
        except Portal.DoesNotExist:
            return redirect('portal')
        customer = User.objects.all()
        artist   = Artist.objects.all()
        art      = Art.objects.all()
        query    = Query.objects.all()
        orders   = Order.objects.all()
        context  = {
            'customer': customer,
            'artist':   artist,
            'art':      art,
            'query':    query,
            'user':     user,
            'orders':   orders,
        }
        return render(request, 'portal/home.html', context)
    else:
        return redirect('portal')


def uploadpdf(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'admin'):
        return redirect('portal')
    try:
        portal_obj = Portal.objects.get(pid=key)
    except Portal.DoesNotExist:
        return redirect('portal')
    if request.method == 'POST':
        name     = request.POST['name']
        desc     = request.POST['desc']
        category = request.POST['category']
        link     = request.FILES.get('link')
        obj = Pdf(name=name, link=link, desc=desc, category=category)
        obj.save()
        messages.success(request, 'Pdf Uploaded')
        return redirect('uploadmats')
    else:
        return render(request, 'portal/uploadmats.html', {'user': portal_obj})


def uploadvideo(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'admin'):
        return redirect('portal')
    try:
        portal_obj = Portal.objects.get(pid=key)
    except Portal.DoesNotExist:
        return redirect('portal')
    if request.method == 'POST':
        name     = request.POST['name']
        desc     = request.POST['desc']
        category = request.POST['category']
        link     = request.POST['link']
        obj = Video(name=name, link=link, desc=desc, category=category)
        obj.save()
        messages.success(request, 'Video Uploaded')
        return redirect('uploadmats')
    else:
        return render(request, 'portal/uploadmats.html', {'user': portal_obj})


def uploadmats(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if key and role == 'admin':
        try:
            portal_obj = Portal.objects.get(pid=key)
        except Portal.DoesNotExist:
            return redirect('portal')
        return render(request, 'portal/uploadmats.html', {'user': portal_obj})
    else:
        return redirect('portal')


def portal_orders(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'admin'):
        return redirect('portal')
    try:
        user = Portal.objects.get(pid=key)   # FIX: was phone=key (Portal has no phone field)
    except Portal.DoesNotExist:
        return redirect('portal')
    orders = Order.objects.all()
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status   = request.POST.get('status')
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
        except Order.DoesNotExist:
            pass
        return redirect('portal_orders')
    else:
        return render(request, 'portal/orders.html', {'orders': orders, 'user': user})


def tutorials(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    user = None
    if key:
        if role == 'user':
            user = User.objects.filter(phone=key).first()
        elif role == 'artist':
            user = Artist.objects.filter(phone=key).first()
        elif role == 'admin':
            user = Portal.objects.filter(pid=key).first()
    videos = Video.objects.all()
    pdfs   = Pdf.objects.all()
    return render(request, 'html/studymats.html', {'videos': videos, 'pdfs': pdfs, 'user': user})


# ──────────────────────────────────────────
# User Views
# ──────────────────────────────────────────

def user_register(request):
    if request.method == 'POST':
        phone    = request.POST['phone']
        password = request.POST['password']
        name     = request.POST['name']
        email    = request.POST['email']
        pic      = request.FILES.get('pic')

        # FIX: check for duplicate phone before registering
        if User.objects.filter(phone=phone).exists():
            messages.error(request, 'An account with this phone number already exists.')
            return render(request, 'user/register.html')

        obj = User(name=name, password=password, email=email, pic=pic, phone=phone)
        obj.save()
        messages.success(request, 'User Registered Successfully')
        return redirect('user_login')
    else:
        return render(request, 'user/register.html')


def user_login(request):
    if request.method == 'POST':
        phone    = request.POST['phone']
        password = request.POST['password']
        obj = User.objects.filter(phone=phone, password=password)
        if obj:
            request.session['session_key']  = phone
            request.session['session_role'] = 'user'
            messages.success(request, 'Logged In')
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'user/login.html')
    else:
        return render(request, 'user/login.html')


def user_chat(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'user'):
        return redirect('user_login')
    try:
        user = User.objects.get(phone=key)
    except User.DoesNotExist:
        return redirect('user_login')
    all_messages   = Chat.objects.filter(user=user).order_by('artist')
    distinct_users = []
    msg_list       = []
    for message in all_messages:
        if message.artist not in distinct_users:
            distinct_users.append(message.artist)
            msg_list.append(message)
    return render(request, 'user/chat.html', {'msg': msg_list, 'user': user})


def user_orders(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'user'):
        return redirect('user_login')
    try:
        user = User.objects.get(phone=key)
    except User.DoesNotExist:
        return redirect('user_login')
    obj = Order.objects.filter(user=user)
    return render(request, 'user/orders.html', {'obj': obj, 'user': user})


# ──────────────────────────────────────────
# Artist Views
# ──────────────────────────────────────────

def artist_register(request):
    if request.method == 'POST':
        phone    = request.POST['phone']
        category = request.POST['category']
        password = request.POST['password']
        name     = request.POST['name']
        email    = request.POST['email']
        pic      = request.FILES.get('pic')

        # FIX: check for duplicate phone before registering
        if Artist.objects.filter(phone=phone).exists():
            messages.error(request, 'An artist account with this phone number already exists.')
            return render(request, 'artist/register.html')

        obj = Artist(name=name, password=password, email=email, pic=pic,
                     category=category, phone=phone)
        obj.save()
        messages.success(request, 'Artist Registered Successfully')
        return redirect('artist_login')
    else:
        return render(request, 'artist/register.html')


def artist_login(request):
    if request.method == 'POST':
        phone    = request.POST['phone']
        password = request.POST['password']
        obj = Artist.objects.filter(phone=phone, password=password)
        if obj:
            request.session['session_key']  = phone
            request.session['session_role'] = 'artist'
            messages.success(request, 'Logged In')
            return redirect('artist_home')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'artist/login.html')
    else:
        return render(request, 'artist/login.html')


def artist_home(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'artist'):       # FIX: guard session
        return redirect('artist_login')
    try:
        user = Artist.objects.get(phone=key)
    except Artist.DoesNotExist:
        return redirect('artist_login')
    Oobj = Order.objects.filter(art__artist=user)
    Aobj = Art.objects.filter(artist=user)
    return render(request, 'artist/home.html', {'user': user, 'Oobj': Oobj, 'Aobj': Aobj})


def artist_messages(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'artist'):
        return redirect('artist_login')
    try:
        artist = Artist.objects.get(phone=key)
    except Artist.DoesNotExist:
        return redirect('artist_login')
    all_messages   = Chat.objects.filter(artist=artist).order_by('user')
    distinct_users = []
    msg_list       = []
    for message in all_messages:
        if message.user not in distinct_users:
            distinct_users.append(message.user)
            msg_list.append(message)
    return render(request, 'artist/chat.html', {'msg': msg_list, 'user': artist})


def send_message(request, id):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'artist'):
        return redirect('artist_login')
    user   = get_object_or_404(User, id=id)
    artist = get_object_or_404(Artist, phone=key)
    msg    = Chat.objects.filter(user=user, artist=artist)
    if request.method == 'POST':
        message = request.POST.get('message', '')
        if message:
            Chat.objects.create(user=user, artist=artist, artist_message=message)
        return render(request, 'artist/send_message.html', {'msg': msg, 'u': user, 'user': artist})
    else:
        return render(request, 'artist/send_message.html', {'msg': msg, 'u': user, 'user': artist})


def artist_orders(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'artist'):
        return redirect('artist_login')
    try:
        user = Artist.objects.get(phone=key)
    except Artist.DoesNotExist:
        return redirect('artist_login')
    obj = Order.objects.filter(art__artist=user)
    return render(request, 'artist/orders.html', {'obj': obj, 'user': user})


def upload(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'artist'):
        return redirect('artist_login')
    try:
        artist = Artist.objects.get(phone=key)
    except Artist.DoesNotExist:
        return redirect('artist_login')
    if request.method == 'POST':
        name     = request.POST['name']
        desc     = request.POST['desc']
        art_type = request.POST['art_type']
        price    = request.POST['price']
        pic      = request.FILES.get('pic')
        forsale  = bool(request.POST.get('forsale'))
        obj = Art(artist=artist, name=name, price=price, art_type=art_type,
                  desc=desc, pic=pic, forsale=forsale)
        obj.save()
        messages.success(request, 'Art Uploaded')
        return redirect('artist_home')
    else:
        return render(request, 'artist/upload.html', {'user': artist})


def add_event(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    artist_obj = None
    admin_obj  = None
    if role == 'artist':
        artist_obj = Artist.objects.filter(phone=key).first()
    elif role == 'admin':
        admin_obj = Portal.objects.filter(pid=key).first()
    else:
        return redirect('home')

    if request.method == 'POST':
        name  = request.POST['name']
        date  = request.POST['date']
        venue = request.POST['venue']
        pic   = request.FILES.get('pic')
        obj   = Event(name=name, date=date, venue=venue, pic=pic)
        if artist_obj:
            obj.artist = artist_obj
        else:
            obj.admin = admin_obj
        obj.save()
        messages.success(request, 'Event Added')
        return redirect('events')
    else:
        ctx_user = artist_obj if artist_obj else admin_obj
        return render(request, 'artist/add_event.html', {'user': ctx_user})


# ──────────────────────────────────────────
# General / Shared Views
# ──────────────────────────────────────────

def _get_user_from_session(request):
    """Helper: returns (user_object, role_string) or (None, None)."""
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not key:
        return None, None
    if role == 'user':
        return User.objects.filter(phone=key).first(), 'user'
    if role == 'artist':
        return Artist.objects.filter(phone=key).first(), 'artist'
    if role == 'admin':
        return Portal.objects.filter(pid=key).first(), 'admin'
    return None, None


def home(request):
    user, _  = _get_user_from_session(request)
    artist   = Artist.objects.all()
    art      = Art.objects.all()
    return render(request, 'html/home.html', {'user': user, 'artist': artist, 'art': art})


def artists(request):
    user, _ = _get_user_from_session(request)
    obj = Artist.objects.all()
    return render(request, 'html/artists.html', {'obj': obj, 'user': user})


def shop(request):
    user, _ = _get_user_from_session(request)
    obj = Art.objects.filter(forsale=True, sold=False)
    return render(request, 'html/shop.html', {'obj': obj, 'user': user})


def events(request):
    user, _ = _get_user_from_session(request)
    obj = Event.objects.all()
    return render(request, 'html/events.html', {'obj': obj, 'user': user})


def gallery(request):
    user, _ = _get_user_from_session(request)
    obj = Art.objects.all()
    return render(request, 'html/gallery.html', {'obj': obj, 'user': user})


def show_art(request, phone):
    user, _     = _get_user_from_session(request)
    artist_obj  = get_object_or_404(Artist, phone=phone)
    obj         = Art.objects.filter(artist=artist_obj)
    return render(request, 'html/gallery.html', {'obj': obj, 'user': user})


def billing(request, id):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'user'):
        return redirect('user_login')
    art  = get_object_or_404(Art, id=id)
    user = get_object_or_404(User, phone=key)
    if request.method == 'POST':
        pic = request.FILES.get('pic')
        order = Order(user=user, art=art, payment=pic)
        order.save()
        art.sold = True
        art.save()
        messages.success(request, 'Order Placed')
        return redirect('user_orders')
    else:
        return render(request, 'user/billing.html', {'art': art})


def chat(request, id=None):
    key, role = request.session.get('session_key'), request.session.get('session_role')
    if not key:
        return redirect('user_login')

    # Determine current user object
    if role == 'user':
        user = User.objects.filter(phone=key).first()
    elif role == 'artist':
        user = Artist.objects.filter(phone=key).first()
    elif role == 'admin':
        user = Portal.objects.filter(pid=key).first()
    else:
        user = None

    if id is None:
        return redirect('home')

    receiver = get_object_or_404(Artist, id=id)

    if request.method == 'POST':
        message = request.POST.get('message', '')
        if message and isinstance(user, (User, Artist)):
            chat_msg = Chat()
            if isinstance(user, User):
                chat_msg.user   = user
                chat_msg.artist = receiver
                chat_msg.user_message = message
            else:
                chat_msg.user   = User.objects.filter(phone=key).first()  # fallback
                chat_msg.artist = receiver
                chat_msg.artist_message = message
            chat_msg.save()
        return redirect('chat', id=id)
    else:
        if isinstance(user, User):
            chat_messages = Chat.objects.filter(user=user, artist=receiver)
        else:
            chat_messages = Chat.objects.filter(artist=receiver)
        return render(request, 'html/chat.html',
                      {'user': user, 'receiver': receiver, 'chat_messages': chat_messages})


def query(request):
    user, _ = _get_user_from_session(request)
    if request.method == 'POST':
        name     = request.POST['name']
        email    = request.POST['email']
        question = request.POST['query']
        obj = Query(name=name, email=email, question=question)
        obj.save()
        messages.success(request, 'Query Submitted')
        return redirect('home')
    else:
        return render(request, 'html/query.html', {'user': user})


def logout(request):
    request.session.flush()
    return redirect('home')
