from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import PicturePostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import PicturePost
from django.views.generic import DetailView
from django.views.generic import DeleteView


class IndexView(TemplateView):
   # debug_int = 12345 # デバッグ時の挙動確認のため使用する無意味な変数
    template_name = "index.html"
    
@method_decorator(login_required, name='dispatch')
class CreatePictureView(CreateView):
    form_class = PicturePostForm
    template_name = 'post_picture.html'
    success_url = reverse_lazy('picture:post_done')
    
    def form_valid(self,form):
        postdata =form.save(commit=False)
        postdata.user=self.request.user
        postdata.save()
        return super().form_valid(form)

class PostSuccessView(TemplateView):
    """投稿完了ページのビュー

    Attribuets:
        template_name: レンダリングするテンプレート
    """
    # index.htmlをレンダリングする
    template_name = "post_success.html"   
    
class IndexView(ListView):
   # debug_int = 12345 # デバッグ時の挙動確認のため使用する無意味な変数
    template_name = "index.html"
    queryset = PicturePost.objects.order_by('-posted_at')
    paginate_by = 9

class CategoryView(ListView):
    """カテゴリページのビュー

    Attributes:
        template_name: レンダリングするテンプレート
        paginame_by: 1ページに表示するレコードの件数
    """
    # index.htmlをレンダリングする
    template_name = 'index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
        """クエリを実行する

        self.kwargsの取得が必要なため、クラス変数querysetではなく、
        get_queryset()のオーバーライドによりクエリを実行する

        Returns:
            クエリによって取得されたレコード
        """
        # self.kwargsでキーワードの辞書を取得し、
        # categoryキーの値(Categoryテーブルのid)を取得
        category_id = self.kwargs['category']
        # filter(フィールド名=id)で絞り込む
        categories = PicturePost.objects.filter(
            category=category_id
        ).order_by('-posted_at')
        return categories
    
class UserView(ListView):
    """ユーザーの投稿一覧ページのビュー

    Attributes:
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコードの件数
    """
    # index.htmlをレンダリングする
    template_name = 'index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
        """クエリを実行する

        self.kwargsの取得が必要なため、クラス変数querysetではなく
        get_queryset()のオーバーライドによりクエリを実行する

        Returns:
            クエリによって取得されたレコード
        """
        # self.kwargsでキーワードの辞書を取得し、
        # userキーの値(ユーザーテーブルのid)を取得
        user_id = self.kwargs['user']
        
        # filter(フィールド名=id)で絞り込む
        user_list = PicturePost.objects.filter(
            user=user_id
        ).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return user_list
    
class DetailView(DetailView):
    """詳細ページのビュー
        投稿記事の詳細を表示するのでDetailViewを継承

    Attributes:
        template_name: レンダリングするテンプレート
        model: モデルのクラス
    """
    # detail.htmlをレンダリングする
    template_name = 'detail.html'
    model = PicturePost        

class MypageView(ListView):
    """マイページのビュー

    Attributes:
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコードの件数
    """
    # mypage.htmlをレンダリングする
    template_name = 'mypage.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
        """クエリを実行する

        self.kwargsの取得が必要なため、クラス変数querysetではなく
        get_queryset()のオーバーライドによりクエリを実行する

        Returns:
            クエリによって取得されたてコード
        """
        # 現在ログインしているユーザー名はHttpRequest.userに格納されている
        # filter(userフィールド=userオブジェクト)で絞り込む
        queryset = PicturePost.objects.filter(
            user=self.request.user
        ).order_by('-posted_at')
        # クエリによって取得されたレコードを返す
        return queryset
    
class PictureDeleteView(DeleteView):
    """レコードの削除を行うビュー

    Attributes:
        model: モデル
        template_name: レンダリングするテンプレート
        paginate_by: 1ページに表示するレコードの件数
        success_url: 削除完了後のリダイレクト先のURL
    """
    # 操作の対象はPicturePostモデル
    model = PicturePost
    # picture_delete.htmlをレンダリングする
    template_name = 'picture_delete.html'
    # 処理完了後にマイページにリダイレクト
    success_url = reverse_lazy('picture:mypage')

    def delete(self, request, *args, **kwargs):
        """レコードの削除を行う

        Args:
            request (WSGIRequest(HttpRequest)):
            args(dist)
            kwargs(dist):
                キーワード付きの辞書
                {'pk': 21}のようにレコードのidが渡される
        Returns:
            HttpResponsRedirect(success_url):
                戻り値を返してsuccess_urlにリダイレクト
        """
        # スーパークラスのdelete()を実行
        return super().delete(request, *args, **kwargs)