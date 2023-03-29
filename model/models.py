from django.db import models
from django.db.models import CASCADE

# Create your substance models here.
class Student(models.Model):
    ID = models.AutoField(primary_key=True, null=False, verbose_name="主键")
    Name = models.CharField(max_length=250, null=False, verbose_name="姓名")
    School = models.CharField(max_length=250, null=False, verbose_name="学校")
    Email = models.CharField(max_length=250, null=False, verbose_name="邮箱")
    Password = models.CharField(max_length=250, null=False, verbose_name="密码")
    Majority = models.CharField(max_length=250, null=False, verbose_name="专业方向")
    Rewards = models.TextField(null=True, verbose_name="竞赛获奖")
    SchoolScores = models.CharField(max_length=250, null=True, verbose_name="学习成绩")
    Skills = models.TextField(null=True, verbose_name="技术栈")
    ScientificExperience = models.TextField(null=False, verbose_name="科研经历")
    EnterpriseCertification = models.BooleanField(default=False, verbose_name="企业认证")
    CV = models.CharField(max_length=250, default="", verbose_name="简历")

    class Meta:
        db_table = "student"
        verbose_name = "学生信息表"


class Tutor(models.Model):
    ID = models.AutoField(primary_key=True, null=False, verbose_name="主键")
    Name = models.CharField(max_length=250, null=False, verbose_name="姓名")
    School = models.CharField(max_length=250, null=False, verbose_name="学校")
    Email = models.CharField(max_length=250, null=False, verbose_name="邮箱")
    Password = models.CharField(max_length=250, null=False, verbose_name="密码")
    Majority = models.CharField(max_length=250, null=False, verbose_name="专业方向")
    Position = models.CharField(max_length=250, null=False, verbose_name="职称")
    EductionExperience = models.TextField(null=False, verbose_name="教育经历")
    Paper = models.CharField(max_length=250, null=False, verbose_name="论文发表")

    class Meta:
        db_table = "tutor"
        verbose_name = "导师信息表"


class Laboratory(models.Model):
    ID = models.AutoField(primary_key=True, null=False, verbose_name="主键")
    Name = models.CharField(max_length=250, null=False, verbose_name="名称")
    School = models.CharField(max_length=250, null=False, verbose_name="学校")
    Majority = models.CharField(max_length=250, null=False, verbose_name="专业方向")
    Introduction = models.TextField(null=False, verbose_name="介绍")

    class Meta:
        db_table = "laboratory"
        verbose_name = "实验室信息表"


class Post(models.Model):
    ID = models.AutoField(primary_key=True, null=False, verbose_name="主键")
    Time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    Title = models.CharField(max_length=250, null=False, verbose_name="标题")
    Text = models.CharField(max_length=250, null=False, verbose_name="内容")
    Images = models.CharField(max_length=250, default="", verbose_name="图片")

    class Meta:
        db_table = "Post"
        verbose_name = "帖子信息表"


class Comment(models.Model):
    ID = models.AutoField(primary_key=True, null=False, verbose_name="主键")
    Time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
    Text = models.CharField(max_length=250, null=False, verbose_name="内容")
    Images = models.CharField(max_length=250, default="", verbose_name="图片")

    class Meta:
        db_table = "Comment"
        verbose_name = "评论信息表"


class Project(models.Model):
    ID = models.AutoField(primary_key=True, null=False, verbose_name="主键")
    Title = models.CharField(max_length=250, null=False, verbose_name="标题")
    Time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    Text = models.CharField(max_length=250, null=False, verbose_name="内容")
    Capacity = models.IntegerField(default=0, verbose_name="人数")
    Tutor = models.CharField(max_length=250, null=False, verbose_name="导师姓名")
    Place = models.CharField(max_length=250, null=False, verbose_name="单位")
    Duration = models.CharField(max_length=250, null=False, verbose_name="持续时间")
    Type = models.CharField(max_length=250, null=False, verbose_name="线上/线下")
    State = models.CharField(max_length=250, null=False, verbose_name="项目状态")

    class Meta:
        db_table = "project"
        verbose_name = "项目信息表"


class Administer(models.Model):
    ID = models.AutoField(primary_key=True, null=False, verbose_name="主键")
    Password = models.CharField(max_length=250, null=False, verbose_name="密码")
    Email = models.CharField(max_length=250, null=False, verbose_name="邮箱")

    class Meta:
        db_table = "administer"
        verbose_name = "管理员信息表"


# Create your relation models here.
class BelongLab(models.Model):
    TutorID = models.ForeignKey(Tutor, on_delete=CASCADE, verbose_name="导师ID")
    LabID = models.ForeignKey(Laboratory, on_delete=CASCADE, verbose_name="实验室ID")

    class Meta:
        unique_together = ("TutorID", "LabID")
        db_table = "belonglab"
        verbose_name = "导师归属实验室"


class SelectProject(models.Model):
    StudentID = models.ForeignKey(Student, on_delete=CASCADE, verbose_name="学生ID")
    ProjectID = models.ForeignKey(Project, on_delete=CASCADE, verbose_name="项目ID")
    State = models.CharField(max_length=250, null=False, default="")
    PlatScore = models.FloatField(default=0)

    class Meta:
        unique_together = ("StudentID", "ProjectID")
        db_table = "selectproject"
        verbose_name = "学生选择项目"


class CreateProject(models.Model):
    TutorID = models.ForeignKey(Tutor, on_delete=CASCADE, verbose_name="导师ID")
    ProjectID = models.ForeignKey(Project, on_delete=CASCADE, verbose_name="项目ID")
    PlatScore = models.FloatField(default=0)

    class Meta:
        unique_together = ("TutorID", "ProjectID")
        db_table = "createproject"
        verbose_name = "导师创建项目"


class PublishPost(models.Model):
    StudentID = models.ForeignKey(Student, on_delete=CASCADE, verbose_name="学生ID")
    PostID = models.ForeignKey(Post, on_delete=CASCADE, verbose_name="帖子ID")

    class Meta:
        unique_together = ("StudentID", "PostID")
        db_table = "PublishPost"
        verbose_name = "学生发帖"


class CommentPost(models.Model):
    CommentID = models.ForeignKey(Comment, on_delete=CASCADE, verbose_name="评论ID")
    PostID = models.ForeignKey(Post, on_delete=CASCADE, verbose_name="帖子ID")

    class Meta:
        unique_together = ("PostID", "CommentID")
        db_table = "CommentPost"
        verbose_name = "评论帖子"


class MakeComment(models.Model):
    StudentID = models.ForeignKey(Student, on_delete=CASCADE, verbose_name="学生ID")
    CommentID = models.ForeignKey(Comment, on_delete=CASCADE, verbose_name="评论ID")

    class Meta:
        unique_together = ("StudentID", "CommentID")
        db_table = "MakeComment"
        verbose_name = "发表评论"


class CollectProject(models.Model):
    StudentID = models.ForeignKey(Student, on_delete=CASCADE, verbose_name="学生ID")
    ProjectID = models.ForeignKey(Project, on_delete=CASCADE, verbose_name="项目ID")

    class Meta:
        unique_together = ("StudentID", "ProjectID")
        db_table = "CollectProject"
        verbose_name = "收藏项目"


class CollectPost(models.Model):
    StudentID = models.ForeignKey(Student, on_delete=CASCADE, verbose_name="学生ID")
    PostID = models.ForeignKey(Post, on_delete=CASCADE,  verbose_name="帖子ID")

    class Meta:
        unique_together = ("StudentID", "PostID")
        db_table = "CollectPost"
        verbose_name = "收藏帖子"


class SendMessage(models.Model):
    ID = models.AutoField(primary_key=True, null=False, verbose_name="主键")
    StudentID = models.ForeignKey(Student, on_delete=CASCADE, verbose_name="学生ID")
    TutTutorID = models.ForeignKey(Tutor, on_delete=CASCADE, verbose_name="导师ID")
    Direction = models.CharField(max_length=250, null=False, verbose_name="发送方向")
    Time = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")
    Text = models.CharField(max_length=250, null=False, verbose_name="内容")

    class Meta:
        db_table = "SendMessage"
        verbose_name = "发送消息"