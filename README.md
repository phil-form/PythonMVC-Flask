# PythonMVC-Flask

## 1) models + sql queries (si nécéssaire)
    ex 
    class Example:
        def __init__(self, data):
            self.data = data
## 2) formulares
    class ExampleForm(FlaskForm):
        exampleData = StringField('exampleData', validators=[])
        exampleData2 = StringField('exampleData2', validators=[DataRequired()])
## 3) services
    - des fonctions pour contacter la db : 
        - findOne => retourne une entité en fonction de son id
        - findOneBy => retourne une entité en fonction d'un paramètre passé (données d'une des colonnes)
        - findAll => retourne toutes les data
        - update => met à jours les donnés en DB
        - insert => insert des nouvelles donnée en DB
        - delete => delete une entrée en DB
## 4) controllers
    class ExampleController:
        # http://servername/path
        @app.route('/path', methods=['GET', 'POST'])
        def getAllData():
            return service.findAll()
        # http://servername/path/1
        @app.route('/path/<int:dataid>', methods=['GET', 'POST'])
        def getAllData(dataid):
            return service.findOne(dataid)
## 5) la vue