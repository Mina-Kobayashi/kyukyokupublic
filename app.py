from flask import Flask,  render_template,  session, redirect, request
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


#Flaskの立ち上げ

app = Flask(__name__)
app.secret_key = b'..'

member_data={}




engine = create_engine('postgresql://')


Base = declarative_base(bind=engine)


#既存の究極二択を表示　テーブル:kyukyokuをつくる
class kyukyoku(Base):
    __tablename__ = "kyukyoku"  # テーブル名を指定 新しくcreate
    id = Column(Integer, primary_key=True, autoincrement=True)
    a_choice = Column(String(50))
    b_choice = Column(String(50))



    def __init__(self,  a_choice, b_choice):
        self.a_choice = a_choice
        self.b_choice = b_choice



#データベース (A, B, name, password)   みんなのアイディア
class ideakyukyoku(Base):
    __tablename__ = "ideakyukyoku"  # テーブル名を指定 新しくcreate
    id = Column(Integer, primary_key=True, autoincrement=True)
    a_idea = Column(String(50))
    b_idea = Column(String(50))
    name = Column(String(20))
    pswd = Column(String(20))
    date = Column(DateTime(), default=datetime.now)

    def __init__(self,  a_idea, b_idea, name, pswd, date):
        self.a_idea = a_idea
        self.b_idea = b_idea
        self.name = name
        self.pswd = pswd
        self.date = date



Base.metadata.create_all(engine)


#最初の表示　kyukyoku_abが並んでいるところ
@app.route('/', methods=['GET'])
def index():
    Session = sessionmaker(bind=engine)
    ses = Session()
    choices = ses.query(kyukyoku).all()
    ses.close()

    return render_template('postgres.html', choices=choices)




@app.route('/history', methods=['GET', 'POST'])
def history():
    newideaA = request.form.get('txt1')
    newideaB = request.form.get('txt2')
    name = request.form.get('name')
    pswd = request.form.get('pass')
    date = datetime.now()

    # DBへ説族してユーザーの履歴そうしんの表示
    datas = ideakyukyoku(a_idea=newideaA, b_idea=newideaB, name=name, pswd=pswd, date=date)
    Session = sessionmaker(bind=engine)
    ses = Session()
    ses.add(datas)
    ses.commit()
    ideas = ses.query(ideakyukyoku).filter_by(name=name, pswd=pswd).all()
    ses.close()

    message = name + 'さん' + 'ようこそ'

    return render_template('history.html', name=name, ideas=ideas, message=message)







if __name__ == '__main__':
    app.run(debug=True)