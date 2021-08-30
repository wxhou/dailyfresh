# Generated by Django 2.2.24 on 2021-08-30 06:51

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(blank=True, help_text='姓名', max_length=30, null=True, verbose_name='name')),
                ('birthday', models.DateField(blank=True, help_text='出生年月', null=True, verbose_name='birthday')),
                ('gender', models.CharField(choices=[('male', '男'), ('female', '女')], default='female', help_text='性别', max_length=6, verbose_name='gender')),
                ('mobile', models.CharField(blank=True, help_text='电话', max_length=11, null=True, verbose_name='phone')),
                ('email', models.EmailField(blank=True, help_text='邮箱', max_length=100, null=True, verbose_name='email')),
                ('avatar', models.ImageField(help_text='用户头像', upload_to='avatar/', verbose_name='avatar')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户管理',
                'verbose_name_plural': '用户管理',
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='create time')),
                ('updated_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='update time')),
                ('status', models.SmallIntegerField(default=0, help_text='状态', verbose_name='status')),
                ('is_deleted', models.BooleanField(default=False, help_text='是否删除', verbose_name='is deleted')),
                ('code', models.CharField(help_text='验证码', max_length=10, verbose_name='code')),
                ('mobile', models.CharField(help_text='手机号码', max_length=11, verbose_name='mobile')),
            ],
            options={
                'verbose_name': '短信验证码',
                'verbose_name_plural': '短信验证码',
                'db_table': 'user_verify_code',
            },
        ),
        migrations.CreateModel(
            name='UserLeavingMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='create time')),
                ('updated_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='update time')),
                ('status', models.SmallIntegerField(default=0, help_text='状态', verbose_name='status')),
                ('is_deleted', models.BooleanField(default=False, help_text='是否删除', verbose_name='is deleted')),
                ('message_type', models.PositiveSmallIntegerField(choices=[(1, '留言'), (2, '投诉'), (3, '询问'), (4, '售后'), (5, '求购')], default=1, help_text='留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)', verbose_name='message type')),
                ('subject', models.CharField(default='', help_text='主题', max_length=100, verbose_name='subject')),
                ('content', models.TextField(default='', help_text='留言内容', verbose_name='message content')),
                ('file', models.ImageField(help_text='上传的图片', upload_to='message/', verbose_name='upload message image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户留言',
                'verbose_name_plural': '用户留言',
                'db_table': 'user_message',
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='create time')),
                ('updated_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='update time')),
                ('status', models.SmallIntegerField(default=0, help_text='状态', verbose_name='status')),
                ('is_deleted', models.BooleanField(default=False, help_text='是否删除', verbose_name='is deleted')),
                ('province', models.CharField(default='', help_text='省份', max_length=100, verbose_name='province')),
                ('city', models.CharField(default='', help_text='城市', max_length=100, verbose_name='city')),
                ('district', models.CharField(default='', help_text='区域', max_length=100, verbose_name='district')),
                ('address', models.CharField(default='', help_text='详细地址', max_length=100, verbose_name='address')),
                ('signer_name', models.CharField(default='', help_text='签收人', max_length=100, verbose_name='signer_name')),
                ('signer_mobile', models.CharField(default='', help_text='电话', max_length=11, verbose_name='signer_mobile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '收货地址',
                'verbose_name_plural': '收货地址',
                'db_table': 'user address',
            },
        ),
        migrations.CreateModel(
            name='UserFav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='create time')),
                ('updated_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='update time')),
                ('status', models.SmallIntegerField(default=0, help_text='状态', verbose_name='status')),
                ('is_deleted', models.BooleanField(default=False, help_text='是否删除', verbose_name='is deleted')),
                ('goods', models.ForeignKey(help_text='商品ID', on_delete=django.db.models.deletion.CASCADE, to='goods.Goods')),
                ('user', models.ForeignKey(help_text='用户ID', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户收藏',
                'verbose_name_plural': '用户收藏',
                'db_table': 'user_fav',
                'unique_together': {('user', 'goods')},
            },
        ),
    ]
