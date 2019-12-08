from  app.models import db,BaseModel

# 应用领域
class Application (BaseModel):
    __tablename__ = "application "
    name = db.Column(db.String(100),nullable=False)
    keywords = db.Column(db.String(255)) # 关键词
    info = db.Column(db.Text)
    cover = db.Column(db.String(255))   # 封面图片
    icon = db.Column(db.String(100))    # 图标
    sort = db.Column(db.Integer, default=0)  # 排序
    

    def __repr__(self):
        return '<Ad %r>' % self.name