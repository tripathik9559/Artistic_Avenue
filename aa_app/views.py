from django.shortcuts import render, redirect, get_object_or_404
from aa_app.models import *
from django.contrib import messages
from django.db.models import Q


# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────

def _get_user_from_session(request):
    """Returns (user_object, role_string) or (None, None)."""
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


# ──────────────────────────────────────────────────────────────────────────────
# Admin / Portal Views
# ──────────────────────────────────────────────────────────────────────────────

def portal(request):
    if request.method == 'POST':
        pid      = request.POST.get('id', '').strip()
        password = request.POST.get('password', '').strip()
        obj = Portal.objects.filter(pid=pid, password=password).first()
        if obj:
            request.session['session_key']  = pid
            request.session['session_role'] = 'admin'
            messages.success(request, 'Welcome back, ' + obj.name + '!')
            return redirect('portal_home')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'portal/login.html')
    return render(request, 'portal/login.html')


def portal_home(request):
    pid  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (pid and role == 'admin'):
        return redirect('portal')
    try:
        user = Portal.objects.get(pid=pid)
    except Portal.DoesNotExist:
        return redirect('portal')
    context = {
        'user':          user,
        'customer':      User.objects.all(),
        'artist':        Artist.objects.all(),
        'art':           Art.objects.all(),
        'query':         Query.objects.all(),
        'orders':        Order.objects.all(),
        'total_users':   User.objects.count(),
        'total_artists': Artist.objects.count(),
        'total_arts':    Art.objects.count(),
        'total_orders':  Order.objects.count(),
        'pending_orders': Order.objects.filter(status='Pending').count(),
    }
    return render(request, 'portal/home.html', context)


def uploadpdf(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'admin'):
        return redirect('portal')
    portal_obj = Portal.objects.filter(pid=key).first()
    if not portal_obj:
        return redirect('portal')
    if request.method == 'POST':
        Pdf.objects.create(
            name=request.POST['name'],
            desc=request.POST['desc'],
            category=request.POST['category'],
            link=request.FILES.get('link'),
        )
        messages.success(request, 'PDF Uploaded Successfully')
        return redirect('uploadmats')
    return render(request, 'portal/uploadmats.html', {'user': portal_obj})


def uploadvideo(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'admin'):
        return redirect('portal')
    portal_obj = Portal.objects.filter(pid=key).first()
    if not portal_obj:
        return redirect('portal')
    if request.method == 'POST':
        Video.objects.create(
            name=request.POST['name'],
            desc=request.POST['desc'],
            category=request.POST['category'],
            link=request.POST['link'],
        )
        messages.success(request, 'Video Uploaded Successfully')
        return redirect('uploadmats')
    return render(request, 'portal/uploadmats.html', {'user': portal_obj})


def uploadmats(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'admin'):
        return redirect('portal')
    portal_obj = Portal.objects.filter(pid=key).first()
    if not portal_obj:
        return redirect('portal')
    return render(request, 'portal/uploadmats.html', {'user': portal_obj})


def portal_orders(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'admin'):
        return redirect('portal')
    user = Portal.objects.filter(pid=key).first()
    if not user:
        return redirect('portal')
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status   = request.POST.get('status')
        try:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            messages.success(request, f'Order #{order_id} updated to {status}.')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
        return redirect('portal_orders')
    orders = Order.objects.all()
    return render(request, 'portal/orders.html', {'orders': orders, 'user': user})


def tutorials(request):
    user, _ = _get_user_from_session(request)
    videos  = Video.objects.all()
    pdfs    = Pdf.objects.all()
    return render(request, 'html/studymats.html', {'videos': videos, 'pdfs': pdfs, 'user': user})


# ──────────────────────────────────────────────────────────────────────────────
# User Views
# ──────────────────────────────────────────────────────────────────────────────

def user_register(request):
    if request.method == 'POST':
        phone    = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        name     = request.POST.get('name', '').strip()
        email    = request.POST.get('email', '').strip()
        pic      = request.FILES.get('pic')

        if not all([phone, password, name, email]):
            messages.error(request, 'All fields are required.')
            return render(request, 'user/register.html')

        if User.objects.filter(phone=phone).exists():
            messages.error(request, 'An account with this phone number already exists.')
            return render(request, 'user/register.html')

        User.objects.create(name=name, password=password, email=email, pic=pic, phone=phone)
        messages.success(request, 'Account created! Please log in.')
        return redirect('user_login')
    return render(request, 'user/register.html')


def user_login(request):
    if request.method == 'POST':
        phone    = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        obj = User.objects.filter(phone=phone, password=password).first()
        if obj:
            request.session['session_key']  = phone
            request.session['session_role'] = 'user'
            messages.success(request, f'Welcome back, {obj.name}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid phone number or password.')
            return render(request, 'user/login.html')
    return render(request, 'user/login.html')


def user_chat(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'user'):
        return redirect('user_login')
    user = User.objects.filter(phone=key).first()
    if not user:
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
    user = User.objects.filter(phone=key).first()
    if not user:
        return redirect('user_login')
    obj = Order.objects.filter(user=user)
    return render(request, 'user/orders.html', {'obj': obj, 'user': user})


# ──────────────────────────────────────────────────────────────────────────────
# Artist Views
# ──────────────────────────────────────────────────────────────────────────────

def artist_register(request):
    if request.method == 'POST':
        phone    = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        name     = request.POST.get('name', '').strip()
        email    = request.POST.get('email', '').strip()
        category = request.POST.get('category', '').strip()
        bio      = request.POST.get('bio', '').strip()
        pic      = request.FILES.get('pic')

        if not all([phone, password, name, email, category]):
            messages.error(request, 'All fields are required.')
            return render(request, 'artist/register.html')

        if Artist.objects.filter(phone=phone).exists():
            messages.error(request, 'An artist account with this phone already exists.')
            return render(request, 'artist/register.html')

        Artist.objects.create(
            name=name, password=password, email=email, pic=pic,
            category=category, phone=phone, bio=bio,
        )
        messages.success(request, 'Artist account created! Please log in.')
        return redirect('artist_login')
    return render(request, 'artist/register.html')


def artist_login(request):
    if request.method == 'POST':
        phone    = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        obj = Artist.objects.filter(phone=phone, password=password).first()
        if obj:
            request.session['session_key']  = phone
            request.session['session_role'] = 'artist'
            messages.success(request, f'Welcome back, {obj.name}!')
            return redirect('artist_home')
        else:
            messages.error(request, 'Invalid phone number or password.')
            return render(request, 'artist/login.html')
    return render(request, 'artist/login.html')


def artist_home(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'artist'):
        return redirect('artist_login')
    user = Artist.objects.filter(phone=key).first()
    if not user:
        return redirect('artist_login')
    Oobj  = Order.objects.filter(art__artist=user)
    Aobj  = Art.objects.filter(artist=user)
    sold  = Art.objects.filter(artist=user, sold=True).count()
    pending_count = Order.objects.filter(art__artist=user, status='Pending').count()
    return render(request, 'artist/home.html', {
        'user': user, 'Oobj': Oobj, 'Aobj': Aobj,
        'sold': sold, 'pending_count': pending_count,
    })


def artist_messages(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'artist'):
        return redirect('artist_login')
    artist = Artist.objects.filter(phone=key).first()
    if not artist:
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
        message = request.POST.get('message', '').strip()
        if message:
            Chat.objects.create(user=user, artist=artist, artist_message=message)
    return render(request, 'artist/send_message.html', {'msg': msg, 'u': user, 'user': artist})


def artist_orders(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'artist'):
        return redirect('artist_login')
    user = Artist.objects.filter(phone=key).first()
    if not user:
        return redirect('artist_login')
    obj = Order.objects.filter(art__artist=user)
    return render(request, 'artist/orders.html', {'obj': obj, 'user': user})


def upload(request):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'artist'):
        return redirect('artist_login')
    artist = Artist.objects.filter(phone=key).first()
    if not artist:
        return redirect('artist_login')
    if request.method == 'POST':
        name     = request.POST.get('name', '').strip()
        desc     = request.POST.get('desc', '').strip()
        art_type = request.POST.get('art_type', '').strip()
        price    = request.POST.get('price', '').strip()
        pic      = request.FILES.get('pic')
        forsale  = bool(request.POST.get('forsale'))

        if not all([name, desc, art_type, price, pic]):
            messages.error(request, 'All fields including artwork image are required.')
            return render(request, 'artist/upload.html', {'user': artist})

        Art.objects.create(
            artist=artist, name=name, price=price,
            art_type=art_type, desc=desc, pic=pic, forsale=forsale,
        )
        messages.success(request, 'Artwork uploaded successfully!')
        return redirect('artist_home')
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
        obj = Event(
            name=request.POST.get('name', ''),
            date=request.POST.get('date', ''),
            venue=request.POST.get('venue', ''),
            pic=request.FILES.get('pic'),
        )
        if artist_obj:
            obj.artist = artist_obj
        else:
            obj.admin = admin_obj
        obj.save()
        messages.success(request, 'Event added successfully!')
        return redirect('events')
    ctx_user = artist_obj if artist_obj else admin_obj
    return render(request, 'artist/add_event.html', {'user': ctx_user})


# ──────────────────────────────────────────────────────────────────────────────
# General / Shared Views
# ──────────────────────────────────────────────────────────────────────────────

def home(request):
    user, _       = _get_user_from_session(request)
    featured_art  = Art.objects.filter(forsale=True, sold=False)[:8]
    all_art       = Art.objects.all()[:6]
    artists       = Artist.objects.all()[:6]
    total_artists = Artist.objects.count()
    total_arts    = Art.objects.count()
    total_sold    = Art.objects.filter(sold=True).count()
    context = {
        'user':          user,
        'artist':        artists,
        'art':           all_art,
        'featured_art':  featured_art,
        'total_artists': total_artists,
        'total_arts':    total_arts,
        'total_sold':    total_sold,
    }
    return render(request, 'html/home.html', context)


def artists(request):
    user, _ = _get_user_from_session(request)
    query   = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    obj = Artist.objects.all()
    if query:
        obj = obj.filter(Q(name__icontains=query) | Q(category__icontains=query))
    if category:
        obj = obj.filter(category__icontains=category)

    # get distinct categories for filter UI
    categories = Artist.objects.values_list('category', flat=True).distinct()
    return render(request, 'html/artists.html', {
        'obj': obj, 'user': user,
        'query': query, 'categories': categories,
        'selected_category': category,
    })


def shop(request):
    user, _ = _get_user_from_session(request)
    query    = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    obj = Art.objects.filter(forsale=True, sold=False)
    if query:
        obj = obj.filter(
            Q(name__icontains=query) |
            Q(artist__name__icontains=query) |
            Q(art_type__icontains=query)
        )
    if category:
        obj = obj.filter(art_type__icontains=category)

    # numeric price filter (price stored as string, try best effort)
    if min_price:
        try:
            min_val = int(min_price)
            filtered = []
            for a in obj:
                try:
                    p = int(str(a.price).replace(',', '').replace(' ', ''))
                    if p >= min_val:
                        filtered.append(a.id)
                except Exception:
                    filtered.append(a.id)
            obj = obj.filter(id__in=filtered)
        except ValueError:
            pass
    if max_price:
        try:
            max_val = int(max_price)
            filtered = []
            for a in obj:
                try:
                    p = int(str(a.price).replace(',', '').replace(' ', ''))
                    if p <= max_val:
                        filtered.append(a.id)
                except Exception:
                    filtered.append(a.id)
            obj = obj.filter(id__in=filtered)
        except ValueError:
            pass

    categories = Art.objects.values_list('art_type', flat=True).distinct()
    return render(request, 'html/shop.html', {
        'obj': obj, 'user': user,
        'query': query, 'categories': categories,
        'selected_category': category,
        'min_price': min_price, 'max_price': max_price,
    })


def events(request):
    user, _ = _get_user_from_session(request)
    obj = Event.objects.all()
    return render(request, 'html/events.html', {'obj': obj, 'user': user})


def gallery(request):
    user, _ = _get_user_from_session(request)
    query    = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    obj = Art.objects.all()
    if query:
        obj = obj.filter(
            Q(name__icontains=query) |
            Q(artist__name__icontains=query) |
            Q(art_type__icontains=query)
        )
    if category:
        obj = obj.filter(art_type__icontains=category)

    categories = Art.objects.values_list('art_type', flat=True).distinct()
    return render(request, 'html/gallery.html', {
        'obj': obj, 'user': user,
        'query': query, 'categories': categories,
        'selected_category': category,
    })


def show_art(request, phone):
    user, _    = _get_user_from_session(request)
    artist_obj = get_object_or_404(Artist, phone=phone)
    obj        = Art.objects.filter(artist=artist_obj)
    art_count  = obj.count()
    sold_count = obj.filter(sold=True).count()
    categories = obj.values_list('art_type', flat=True).distinct()
    return render(request, 'html/artist_profile.html', {
        'obj':        obj,
        'user':       user,
        'artist_obj': artist_obj,
        'art_count':  art_count,
        'sold_count': sold_count,
        'categories': categories,
    })


def billing(request, id):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not (key and role == 'user'):
        messages.error(request, 'Please log in to purchase artwork.')
        return redirect('user_login')
    art  = get_object_or_404(Art, id=id)
    user = get_object_or_404(User, phone=key)

    if art.sold:
        messages.error(request, 'Sorry, this artwork has already been sold.')
        return redirect('shop')

    if request.method == 'POST':
        pic = request.FILES.get('pic')
        if not pic:
            messages.error(request, 'Please upload a payment screenshot.')
            return render(request, 'user/billing.html', {'art': art})
        Order.objects.create(user=user, art=art, payment=pic)
        art.sold = True
        art.save()
        messages.success(request, 'Order placed successfully! We will confirm shortly.')
        return redirect('user_orders')
    return render(request, 'user/billing.html', {'art': art})


def chat(request, id=None):
    key  = request.session.get('session_key')
    role = request.session.get('session_role')
    if not key:
        return redirect('user_login')

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
        message = request.POST.get('message', '').strip()
        if message and isinstance(user, User):
            Chat.objects.create(user=user, artist=receiver, user_message=message)
        return redirect('chat', id=id)

    if isinstance(user, User):
        chat_messages = Chat.objects.filter(user=user, artist=receiver)
    else:
        chat_messages = Chat.objects.filter(artist=receiver)

    return render(request, 'html/chat.html',
                  {'user': user, 'receiver': receiver, 'chat_messages': chat_messages})


def query(request):
    user, _ = _get_user_from_session(request)
    if request.method == 'POST':
        name     = request.POST.get('name', '').strip()
        email    = request.POST.get('email', '').strip()
        question = request.POST.get('query', '').strip()
        if not all([name, email, question]):
            messages.error(request, 'All fields are required.')
            return render(request, 'html/query.html', {'user': user})
        Query.objects.create(name=name, email=email, question=question)
        messages.success(request, 'Message sent! We will get back to you soon.')
        return redirect('home')
    return render(request, 'html/query.html', {'user': user})


def logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('home')
