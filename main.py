import flet as ft
from datetime import datetime
import sqlite3

class DataBase:
    def ConnectToDatabase():
        try:
            db = sqlite3.connect('todo.db')
            c = db.cursor()
            c.execute("CREATE TABLE IF NOt EXISTS tasks(id_task INT PRIMARY KEY , task VARCHAR(255) NOT NULL,date_task VARCHar(255) NOt NULL)")
            return db
        except Exception as e:
            print(e)

    def ReadDb(db):
        c = db.cursor()
        c.execute("SELECT task,date_task FROM tasks")
        recorcd = c.fetchall()
        return recorcd
    def InsertDb(db,value):
        c = db.cursor()
        c.execute("INSERT INTO tasks(task,date_task) VALUES(?,?)",value)
        db.commit()
        print("--Inserted")

    def DeleteDb(db,value):
        c = db.cursor()
        c.execute("DELETE FROM tasks WHERE task=?",(value,))
        db.commit()
        print("--Deleted")

    def UpdateDb(db,value):
        try :
            c = db.cursor()
            c.execute("UPDATE tasks SET task=? WHERE task=?",value)
            db.commit()
            print("--updated")
        except Exception as e : 
            print(e)




class FormContainer(ft.Container):
    def __init__(self,func):
        super().__init__()
        self.func=func
        self.width=400
        self.height=100
        self.bgcolor="bluegrey500"
        self.opacity=0
        self.border_radius=40
        self.animate=ft.animation.Animation(500,"decelerate")
        self.animate_opacity=200
        self.padding=ft.padding.only(top=50,bottom=50)
        self.margin=ft.margin.only(left=0,right=0)
        self.content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.TextField(
                    width=300,
                    height=80,
                    filled=True,
                    border_color='transparent',
                    hint_text="Description ...",
                    text_style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                ft.IconButton(
                    content=ft.Text("Add Task",color="white",
                    weight=ft.FontWeight.BOLD),
                    width=200,
                    height=50,
                    on_click=self.func,
                    style=ft.ButtonStyle(bgcolor={"":"black"},shape={"":ft.RoundedRectangleBorder(radius=8)}))
                ]
        )


class CreateTask(ft.Container):
    def __init__(self,task:str,date:str,func1,func2):
        super().__init__()
        self.task=task
        self.date=date
        self.func1 = func1
        self.func2 = func2
        self.width=380
        self.height=70
        self.border=ft.border.all(0.85,"white")
        self.border_radius=8
        self.on_hover= lambda e : self.ShowIcons(e)# add it later,
        self.clip_behavior=ft.ClipBehavior.HARD_EDGE
        self.padding=10
        self.content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Column(
                    spacing=1,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(value=self.task,size=14,color="white"),
                        ft.Text(value=self.date,size=11,color="white54")
                    ]
                ),
                ft.Row(
                    spacing=0,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.TaskDeletEdit(ft.Icons.DELETE_ROUNDED,"red500",self.func1),
                        self.TaskDeletEdit(ft.Icons.EDIT_ROUNDED,"white70",self.func2)
                    ]
                )
            ]
        )


    
    def TaskDeletEdit(self,name,color,func):
        return ft.IconButton(
            icon=name,
            width=30,
            icon_size=18,
            icon_color= color,
            opacity=0,
            animate_opacity=200,
            on_click=lambda e : func(self.GetContainerInstance())
        )
    def GetContainerInstance(self):
        return self


    def ShowIcons(self,e):
        
        if e.data == "true":
            (e.control.content.controls[1].controls[0].opacity,
            e.control.content.controls[1].controls[1].opacity)=(1,1)
            e.control.content.update()
        else:
            (e.control.content.controls[1].controls[0].opacity,
            e.control.content.controls[1].controls[1].opacity)=(0,0)
            e.control.content.update()
            
    
    
            
        





def main(page:ft.Page):
    page.title = "To-Do APP"
    page.window.width=400
    page.window.height=800
    page.bgcolor = "#0f0f0f"
    
    #=====================
    def AddTaskToScreen(e):
        dateTime = datetime.now().strftime("%b %d,%Y %I:%M")
        db = DataBase.ConnectToDatabase()
        DataBase.InsertDb(db,(form.content.controls[0].value,dateTime))
        db.close()
        if form.content.controls[0].value:
            _main_column_.controls.append(
                CreateTask(form.content.controls[0].value,dateTime,DeleteFunction,UpdateFunction)
            )
            _main_column_.update()
            create_todo_ask(e)
        else:
            db.close()


    def DeleteFunction(e):
        print("--Delete")
        _main_column_.controls.remove(e)
        db  = DataBase.ConnectToDatabase()
        DataBase.DeleteDb(db,e.content.controls[0].controls[0].value)
        db.close()
        _main_column_.update()
        

    def UpdateFunction(e):
        create_todo_ask(e)
        form.content.controls[0].value = e.content.controls[0].controls[0].value
        form.content.controls[1].content.value = "Update" 
        form.content.controls[1].on_click= lambda _: FinalizeUpdate(e)
        form.update()
        print("--Update")

    def FinalizeUpdate(e):
        dateTime = datetime.now().strftime("%b %d,%Y %I:%M")
        db = DataBase.ConnectToDatabase()
        DataBase.UpdateDb(db,(form.content.controls[0].value,e.content.controls[0].controls[0].value  ),)
        db.close()
        e.content.controls[0].controls[0].value = form.content.controls[0].value
        e.content.controls[0].controls[1].value = dateTime
        
        
        print("--Finalize")
        
        _main_column_.update()
        e.content.update()
        create_todo_ask(e)

    def create_todo_ask(e) :
        if form.height!=100:
            form.height , form.opacity=100 , 0
            
        else:
            form.height , form.opacity =250 , 1
            
        form.content.controls[0].value=''
        form.content.controls[1].content.value = "Add Task" 
        form.content.controls[1].on_click= lambda e: AddTaskToScreen(e)
        form.update()
        form.content.controls[0].focus(),
        



    _main_column_ = ft.Column(
        
        scroll = "hidden",
        expand = True,
        alignment=ft.MainAxisAlignment.START,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("    TO DO ITEMS",color="#ffffff",size=18),
                    ft.IconButton(ft.Icons.ADD_CIRCLE_ROUNDED,icon_size=18,icon_color="white",on_click=lambda e: create_todo_ask(e))

                ]
            ),
            ft.Divider(height=8,color="white24")
            
        ]
    )
    _main_container_ = ft.Container(
        
            width=380,
            height=750,
            bgcolor="#0f0f0f",
            border_radius=40,
            border=ft.border.all(0.5, "white"),
            padding=ft.padding.only(top=35, left=1, right=1),
            clip_behavior=ft.ClipBehavior.HARD_EDGE, #clip contents.to container
            content=ft.Column (
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
                controls=[
                    _main_column_,
                    FormContainer(lambda e:AddTaskToScreen(e))]


                        )
        
            )
    
    page.add(_main_container_ )
    page.update()
    form = page.controls[0].content.controls[1]
    #print(form)


    db = DataBase.ConnectToDatabase()
    for task in DataBase.ReadDb(db):
        _main_column_.controls.append(
            CreateTask(task[0],task[1],DeleteFunction,UpdateFunction)
        )
        _main_column_.update()

if __name__ == "__main__":
    ft.app(target=main)