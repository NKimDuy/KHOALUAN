
import pandas as pd
from django.shortcuts import render, get_object_or_404
from django.utils.html import strip_tags

from .models import Product, Comment, Emotion, Felling, Order
from .forms import RegistrationForm, CommentForm, OrderForm
from django.http import HttpResponse, HttpResponseRedirect
#from logistic_classifier import LogisticRegressionClassifier
#from tfidf import TfIdfVec
#from dataset import load_dataset
from sklearn.model_selection import train_test_split
import time
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import os
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here.




#//////////////////////////////////////////////////////////////////////////////////////////////////////
from .pre_process.Emotion import preprocess_feature
from .logistic.BaseClassifier import LogisticRegressionClassifier
from .tfxidf.BaseVectorizer import TfIdfVec

def load_dataset(path, category):
    dataset = []
    for category_name in category:
        cat_path = "%s/%s" % (path, category_name)
        cat_file = os.listdir(cat_path)
        for file in cat_file:
            cat_file_path = "%s/%s" % (cat_path, file)
            cat_f = open(cat_file_path, "r+", encoding = "utf-8")
            #feature = cat_f.read()
            feature = preprocess_feature(cat_f.read())
            item = {
                "feature": feature,
                "target": category_name
            }
            dataset.append(item)
            cat_f.close()
    return dataset
"""
class BaseClassifier:
    def __init__(self, class_name, params={}):
        self.class_name = class_name
        self.params = params
        self.classifier = None

    def training(self, train_vectors, train_targets):
        start = time.time()
        self.classifier = globals()[self.class_name](**self.params)
        self.classifier.fit(train_vectors, train_targets)
        end = time.time()

        return {"duration": end - start}

    def predict(self, test_vectors):
        if self.classifier:
            predict = self.classifier.predict(test_vectors)
            return predict



class BaseVectorizer:
    def __init__(self, ds_train, ds_test, class_name=None, params=None):
        self.class_name = class_name
        self.params = params
        self.ds_train = ds_train
        self.ds_test = ds_test

    def vectorizer(self):
        train_vectors, test_vectors = self._process()

        return {
            "train_vectors": train_vectors,
            "test_vectors": test_vectors
        }

    def _process(self):
        v = globals()[self.class_name](**self.params)
        train_vectors = v.fit_transform(self.ds_train)
        test_vectors = v.transform(self.ds_test)

        return train_vectors, test_vectors

class LogisticRegressionClassifier(BaseClassifier):
    def __init__(self, multi_class="ovr"):
        params = {
            "multi_class": multi_class,
            "solver": "lbfgs"
        }

        super().__init__(class_name=LogisticRegression.__name__,
                         params=params)

class TfIdfVec(BaseVectorizer):
    def __init__(self, params, ds_train, ds_test):
        super().__init__(ds_train=ds_train,
                         ds_test=ds_test,
                         class_name=TfidfVectorizer.__name__,
                         params=params)


class TfVec(BaseVectorizer):
    def __init__(self, params, ds_train, ds_test):
        super().__init__(ds_train=ds_train,
                         ds_test=ds_test,
                         class_name=CountVectorizer.__name__,
                         params=params)

"""
path = "/Users/duynk/Desktop/AI/tuyen_dataset"
category = ['RatHaiLong', 'HaiLong', 'KhongHaiLong']
params = {
    "ngram_range": (1, 2)
}
df_train = pd.DataFrame(load_dataset(path, category))
X_train, X_test, y_train, y_test = train_test_split(df_train['feature'], df_train['target'], random_state=0)


#//////////////////////////////////////////////////////////////////////////////////////////////////////


def index(request):
    product = Product.objects.all()
    cart_count = 0  # đếm số sản phẩm có trong giỏ hàng
    data = []  # mảng lưu các id của sản phẩm đã được lưu trong session
    for key, value in request.session.items():
        if type(value) == int:
            cart_count += 1
            product_session = Product.objects.get(id=value)
            data.append(product_session)

    return render(request, 'home/index.html', {'product': product, 'product_session': data, 'cart_count': cart_count})

"""
def detail(request, id):
    #product = Product.objects.get(id = id)
    product = get_object_or_404(Product, id=id)
    form = CommentForm()
    emotion = Emotion()
    if request.method == 'POST':
        form = CommentForm(request.POST, author=request.user, product=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    return render(request, 'home/detail.html', {'detail_product': product, 'form':form, 'emotion':emotion})
"""

abc = 'a'
comment = ''
def detail(request, id):
    global abc, comment  # các biến để kiểm tra bình luận có phải là mới nhất
    product = get_object_or_404(Product, id=id)  # tìm sp nếu không thấy sẽ hiện lỗi 404
    form = CommentForm()
    felling = product.felling_set.get(id=id)  # các nhãn tương ứng với sp

    cart_count = 0
    for key, value in request.session.items():
        if type(value) == int:
            cart_count += 1

    #request.session['id'+str(id)] = id
    #del request.session['id1']
    if request.method == 'POST':
        form = CommentForm(request.POST, author=request.user, product=product)  # hiện text để nhập binh luận
        if form.is_valid():
            form.save()
            comment = Comment.objects.order_by('-date')[0]  # lấy bình luận mới nhất
            by_tfidf = TfIdfVec(ds_train=X_train, ds_test=[comment.content], params=params).vectorizer()
            clf = LogisticRegressionClassifier(multi_class="multinomial")
            clf.training(train_vectors=by_tfidf['train_vectors'], train_targets=y_train)
            result = clf.predict(test_vectors=by_tfidf['test_vectors'])
            if result == 'RatHaiLong':
                abc = 'RatHaiLong'
                felling.strong_positive += 1
                felling.save()
            if result == 'HaiLong':
                abc = 'HaiLong'
                felling.positive += 1
                felling.save()
            if result == 'KhongHaiLong':
                abc = 'KhongHaiLong'
                felling.negative += 1
                felling.save()
            return HttpResponseRedirect(request.path)
    return render(request, 'home/detail.html', {'detail_product': product, 'form': form, 'felling': felling, 'cart_count': cart_count, 're1': abc, 'c': comment})


def register(request):
    register = RegistrationForm()
    if request.method == 'POST':
        register = RegistrationForm(request.POST)
        if register.is_valid():
            register.save()
            return HttpResponseRedirect('/')
    return render(request, 'home/register.html', {'register': register})


def cart(request):
    data = []
    cart_count = 0
    for key, value in request.session.items():
        if type(value) == int:
            cart_count += 1  # đếm số sản phẩm đang tồn tại trong giỏ hàng
            product = Product.objects.get(id=value)
            data.append(product)
    form = OrderForm()

    if request.method == 'POST':
        pro = request.POST['hid_product']  # lấy các sản phẩm trong giỏ hàng để tiến hành mua hàng
        pro = pro.split(",")  # chuyển sang mảng
        quantity = request.POST['hid_quantity']  # lấy số lượng tương ứng của từng sp
        quantity = quantity.split(",")
        total_price = request.POST['hid_price']  # lấy giá tương ứng của từng sp
        total_price = total_price.split(",")

        for i, j, k in zip(pro, quantity, total_price):  # lập song song trên 3 mảng
            product_order = Product.objects.get(id=i)
            form = OrderForm(request.POST, author=request.user, product=product_order, quantity=j, price=k)
            if form.is_valid():
                form.save()
            del request.session['id'+i]  # sau khi đã đặt hàng, sẽ tiến hành xóa tẩt cả sản phẩm ở giỏ hàng

        html_message = render_to_string('home/mail.html', {'data': data})  # gửi mail theo định dạng html
        plain_message = strip_tags(html_message)
        send_mail('đơn hàng mới', plain_message, 'duyshop.ou@gmail.com', ['1651010030duy@ou.edu.vn'],
                  fail_silently=False, html_message=html_message)
        return HttpResponseRedirect('/ordered_detail/')  # khi đặt hàng thành công sẽ chuyển sang trang các sản phẩm đã mua
    return render(request, 'home/cart.html', {'product': data, 'form': form, 'cart_count': cart_count})


def ordered(request):
    user = User.objects.get(id=request.session['_auth_user_id'])  # lấy user hiện tại đăng nhập
    data = []  # mảng lưu địa chỉ, điện thoại, mail của người đặt hàng
    order = Order.objects.all()
    for item in order:  # duyệt tất cả các đơn đặt hàng, tìm người đặt hàng tương ứng với người đăng nhập
        if item.author == user:
            data.append(item)
    if data:
        phone = data[0].phone
        mail = data[0].mail
        address = data[0].address
    else:
        phone = mail = address = ''
    return render(request, 'home/ordered_detail.html', {'ordered': data, 'phone': phone, 'mail': mail, 'address': address})

"""
def success_order(request):
    pro = request.GET['pro']
    pro = pro.split(",")
    quantity = request.GET['quantity']
    quantity = quantity.split(",")
    total_price = request.GET['totalPrice']
    total_price = total_price.split(",")

    phone = request.GET['phone']
    mail = request.GET['mail']
    address = request.GET['address']
    #if request.method == 'POST':
    for i, j, k in zip(pro, quantity, total_price):
        product_order = Product.objects.get(id=i)
        #form = OrderForm(request.POST, author=request.user, product=product_order, quantity=6, price=10, phone=phone, mail=mail, address=address)
        #if form.is_valid():
        #form.save()
        order = Order(product_order, request.user, j, k, phone, mail, address)
        order.save()
"""
def count_click(request):
    click = request.GET['id']
    product = Product.objects.get(id=click)
    product.click += 1
    product.save()


def count_like(request):
    click = request.GET['id']
    emotion = request.GET['e']
    product = Product.objects.get(id=click)
    if emotion == '1':
        product.like += 1
    if emotion == '2':
        product.like -= 1
    product.save()


def count_dislike(request):
    click = request.GET['id']
    emotion = request.GET['e']
    product = Product.objects.get(id=click)
    if emotion == '1':
        product.dis_like += 1
    if emotion == '2':
        product.dis_like -= 1
    product.save()


def statistical(request):
    id = request.GET['id']
    product = Product.objects.get(id=id)
    felling = Felling.objects.get(id=id)
    data = {
        'click': product.click,
        'like': product.like,
        'dislike': product.dis_like,
        'rhl': felling.strong_positive,
        'hl': felling.positive,
        'khl': felling.negative
    }
    return JsonResponse(data)


def buy_product(request):
    id = request.GET['id']
    request.session['id' + str(id)] = int(id)

    cart_count = 0
    for key, value in request.session.items():
        if type(value) == int:
            cart_count += 1

    data = {
        'cart_count': cart_count
    }
    return JsonResponse(data)


def delete_product(request):

    cart_count = 0
    for key, value in request.session.items():
        if type(value) == int:
            cart_count += 1
    cart_count = cart_count - 1
    del request.session['id' + request.GET['id']]
    data = {
        'cart_count': cart_count
    }
    return JsonResponse(data)