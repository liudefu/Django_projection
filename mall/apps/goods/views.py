# Create your views here.
from django.shortcuts import render
from django.views import View

from rest_framework.response import Response


class CategoryView(View):
    """获取首页分类数据"""
    def get(self, request):
        # 1. 验证
        # 2. 获取
        # 3. 返回
        categories = OrderedDict()
        # 获取一级分类
        channels = GoodsChannel.objects.order_by('group_id', 'sequence')

        # 对一级分类进行遍历
        for channel in channels:
            # 获取group_id
            group_id = channel.group_id
            # 判断group_id 是否在存储容器,如果不在就初始化
            if group_id not in categories:
                categories[group_id] = {
                    'channels': [],
                    'sub_cats': []
                }

            one = channel.category
            # 为channels填充数据
            categories[group_id]['channels'].append({
                'id': one.id,
                'name': one.name,
                'url': channel.url
            })
            # 为sub_cats填充数据
            for two in one.goodscategory_set.all():
                # 初始化 容器
                two.sub_cats = []
                # 遍历获取
                for three in two.goodscategory_set.all():
                    two.sub_cats.append(three)

                # 组织数据
                categories[group_id]['sub_cats'].append(two)

                # 广告和首页数据
                contents = {}
                content_categories = ContentCategory.objects.all()
                # content_categories = [{'name':xx , 'key': 'index_new'}, {}, {}]

                # {
                #    'index_new': [] ,
                #    'index_lbt': []
                # }
                for cat in content_categories:
                    contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

                context = {
                    'categories': categories,
                    'contents': contents
                }
                return render(request, 'home.html', context)


