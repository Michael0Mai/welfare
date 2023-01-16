from drf_yasg.inspectors import SwaggerAutoSchema

class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    method_map = {
        'list': '列表页',
        'create': '创建',
        'read': '根据ID详情页',
        'update': '根据ID更新',
        'partial_update': '根据ID部分更新',
        'delete': '根据ID删除',
        'brief': '简略列表页',
        'address_web': '简略网址列表页',
        'download': '根据ID下载图片',
        'change_password': '修改密码',
        'add_like': '点赞',
        'had_liked': '已赞'
    }
    def get_tags(self, operation_keys=None):
        tags = super().get_tags(operation_keys)
        # print(operation_keys)
        view_tags = getattr(self.view, 'tags', [])
        if "token" not in tags and operation_keys:
            if not view_tags:
                tags[0] = operation_keys[1]
            else:
                tags = view_tags
        return tags
    
    def get_operation_id(self, operation_keys=None): # 每个 API 的 operation_id 需要唯一
        view_tags = getattr(self.view, 'tags', [])
        if view_tags and operation_keys[-1] in self.method_map:
            operation_id = view_tags[0] + "-" + self.method_map[operation_keys[-1]]
        elif view_tags and operation_keys[-1] not in self.method_map:
            operation_id = operation_id = view_tags[0] + "-" + operation_keys[-1]
        elif not view_tags and operation_keys[-1] in self.method_map:
            operation_id = '-'.join(operation_keys[0:-1]) + "-" + self.method_map[operation_keys[-1]]
        else:
            operation_id = '-'.join(operation_keys)
        return operation_id