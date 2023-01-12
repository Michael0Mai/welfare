from django import forms

class AddLikeForm(forms.Form):
    id = forms.UUIDField(
        label="图片 ID",
        initial=None,  # 设置默认值
        error_messages={
            "required": "不能为空",
            "invalid": "必须是 UUID 格式"
        }
    )