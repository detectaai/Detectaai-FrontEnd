from flask import Flask, render_template, url_for, redirect, flash, request,session
import base64
import requests
import json


app = Flask(__name__)
global imgBase64Global

# Session 
app.secret_key = 'mysecretkey' 
urlBase = 'https://reconocimientoteaapi.herokuapp.com/predict'

@app.route('/', methods=['POST', 'GET'])
def index():   
    if request.method == 'POST':   
        form=request.form      
        session['nombre'] = form['first_name']
        session['apellido'] = form['last_name']
        return render_template('prediction.html') 
    else:
        return render_template('index.html') 


@app.route('/file', methods=['POST', 'GET'])
def prediction():   
    if request.method == 'POST': 
        global imgBase64Global
        file = request.files['file'].read()
        imgBase64Global = base64.b64encode(file).decode("utf-8") 
        multipart_form_data = {'file': ("file.jpg", file) }
        res = requests.post(url=urlBase, files=multipart_form_data)         
        res = res.json()
        if res['estado']:
            session['tea'] = round(res['tea'], 2) 
            session['sinTea'] = round(res['sinTea'], 2) 
        return redirect('/questions') 
    else:
        return render_template('prediction.html', img=None, flag=0) 


@app.route('/questions', methods=['POST', 'GET'])
def question():   
    if request.method == 'POST':       
        riesgo = 0
        suma = 0
        list_preguntas=[]
        comment_form=request.form
        for respuesta in comment_form:
            if(comment_form[respuesta] == "1"):
                list_preguntas.append(int(respuesta))
                suma = suma + int(comment_form[respuesta])

        if (suma>=8):
            riesgo=3
        elif suma<=2:
            riesgo=1
        else:
            riesgo=2

        session['riesgo'] = riesgo
        session['suma'] = suma
        session['list_preguntas'] = list_preguntas
        if (suma <= 2 ) or (suma >=8):
            session['resultadoDirecto'] = 1
            return redirect('results')
        else:
            session['resultadoDirecto'] = 2
            return redirect('questions_second_part') 
    else:
        with open('preguntas.json', encoding="utf8") as file:
            data = json.load(file)
        return render_template('questions.html', questions=data) 


@app.route('/questions_second_part', methods=['POST', 'GET'])
def questionPart2():   
    if request.method == 'POST':         
        comment_form=request.form
        respuesta_1_pasa=0
        respuesta_1_no_pasa=0
        list_preguntas_no_pasa=[]
        list_preguntas_pasa=[]
        preguntas = session.get('list_preguntas_nuevas')
        for pregunta in preguntas:
            print(pregunta['id'])
            if pregunta['id'] == 1:
                if comment_form['1.1'] == '1': respuesta_1_pasa=respuesta_1_pasa+1
                if comment_form['1.2'] == '1': respuesta_1_pasa=respuesta_1_pasa+1
                if comment_form['1.3'] == '1': respuesta_1_pasa=respuesta_1_pasa+1
                if comment_form['1.4'] == '1': respuesta_1_pasa=respuesta_1_pasa+1
                if comment_form['1.5'] == '1': respuesta_1_no_pasa=respuesta_1_no_pasa+1
                if comment_form['1.6'] == '1': respuesta_1_no_pasa=respuesta_1_no_pasa+1
                if comment_form['1.7'] == '1': respuesta_1_no_pasa=respuesta_1_no_pasa+1
                if respuesta_1_pasa > respuesta_1_no_pasa: list_preguntas_pasa.append(1)
                else: list_preguntas_no_pasa.append(1)
            if pregunta['id'] == 2:
                if comment_form['2.1'] == '0' and comment_form['2.2'] == '0': list_preguntas_pasa.append(2)
                else: list_preguntas_no_pasa.append(2)
            if pregunta['id'] == 3:                
                if comment_form['3.1'] == '0' and comment_form['3.2'] == '0' and comment_form['3.3'] == '0'and comment_form['3.4'] == '0' and comment_form['3.5'] == '0' and comment_form['3.6'] == '0' and comment_form['3.7'] == '0' and comment_form['3.8'] == '0' and comment_form['3.9'] == '0' and comment_form['3.10'] == '0':                    
                    list_preguntas_no_pasa.append(3)
                else: list_preguntas_pasa.append(3)
            if pregunta['id'] == 4:                
                if comment_form['4.1'] == '0' and comment_form['4.2'] == '0' and comment_form['4.3'] == '0'and comment_form['4.4'] == '0':                    
                    list_preguntas_no_pasa.append(4)
                else: list_preguntas_pasa.append(4)
            if pregunta['id'] == 5:            
                if comment_form['5.1'] == '0' and comment_form['5.2'] == '0':
                    if comment_form['5.3'] == '0' and comment_form['5.4'] == '0' and comment_form['5.5'] == '0' and comment_form['5.6'] == '0':
                        list_preguntas_pasa.append(5)
                    elif comment_form['5.7'] == '0': list_preguntas_pasa.append(5)
                    else: list_preguntas_no_pasa.append(5)
                else: list_preguntas_no_pasa.append(5)
            if pregunta['id'] == 6:            
                if comment_form['6.1'] == '0' and comment_form['6.2'] == '0' and comment_form['6.3'] == '0' and comment_form['6.4'] == '0':
                    list_preguntas_no_pasa.append(6)
                elif comment_form['6.5'] == '0': list_preguntas_no_pasa.append(6)             
                else: list_preguntas_pasa.append(6)
            if pregunta['id'] == 7:            
                if comment_form['7.1'] == '0' and comment_form['7.2'] == '0' and comment_form['7.3'] == '0' and comment_form['7.4'] == '0':
                    list_preguntas_no_pasa.append(7)
                elif comment_form['7.5'] == '0' or comment_form['7.6'] == '0' : list_preguntas_no_pasa.append(7)                            
                else: list_preguntas_pasa.append(7)
            if pregunta['id'] == 8:            
                if comment_form['8.1'] == '1' : list_preguntas_pasa.append(8)
                elif comment_form['8.2'] == '0' or comment_form['8.10'] == '0' : list_preguntas_no_pasa.append(8)                            
                elif comment_form['8.3'] == '0' and comment_form['8.4'] == '0' and comment_form['8.5'] == '0' and comment_form['8.6'] == '0' and comment_form['8.7'] == '0' and comment_form['8.8'] == '0' and comment_form['8.9'] == '0':
                    list_preguntas_no_pasa.append(8)
                else: list_preguntas_pasa.append(8)
            if pregunta['id'] == 9:                                       
                if comment_form['9.1'] == '0' and comment_form['9.2'] == '0' and comment_form['9.3'] == '0' and comment_form['9.4'] == '0' and comment_form['9.5'] == '0' :
                    list_preguntas_no_pasa.append(9)
                elif comment_form['9.6'] == '0': list_preguntas_no_pasa.append(9)
                else: list_preguntas_pasa.append(9)
            if pregunta['id'] == 10:                                       
                if comment_form['10.1'] == '1' and comment_form['10.2'] == '1' and comment_form['10.3'] == '1' and comment_form['10.4'] == '0' and comment_form['10.5'] == '0' and comment_form['10.6'] == '0' and comment_form['10.7'] == '0' :
                    list_preguntas_pasa.append(10)
                elif comment_form['10.1'] == '0' and comment_form['10.2'] == '0' and comment_form['10.3'] == '0' and comment_form['10.4'] == '1' and comment_form['10.5'] == '1' and comment_form['10.6'] == '1' and comment_form['10.7'] == '1':
                    list_preguntas_no_pasa.append(10)
                else: list_preguntas_no_pasa.append(10)
            if pregunta['id'] == 11:                                       
                if comment_form['11.1'] == '1' and comment_form['11.2'] == '1' and comment_form['11.3'] == '1' and comment_form['11.4'] == '0' and comment_form['11.5'] == '0' and comment_form['11.6'] == '0' :
                    list_preguntas_pasa.append(11)
                elif comment_form['11.1'] == '0' and comment_form['11.2'] == '0' and comment_form['11.3'] == '0' and comment_form['11.4'] == '1' and comment_form['11.5'] == '1' and comment_form['11.6'] == '1':
                    list_preguntas_no_pasa.append(11)
                else:  list_preguntas_no_pasa.append(11)
            if pregunta['id'] == 12:                                       
                if comment_form['12.1'] == '0' and comment_form['12.2'] == '0' and comment_form['12.3'] == '0' and comment_form['12.4'] == '0' and comment_form['12.5'] == '0' and comment_form['12.6'] == '0' and comment_form['12.7'] == '0' and comment_form['12.8'] == '0' and comment_form['12.9'] == '0' :
                   list_preguntas_pasa.append(12)
                elif comment_form['12.10'] == '1' and comment_form['12.11'] == '1' and comment_form['12.12'] == '0' and comment_form['12.13'] == '0' and comment_form['12.14'] == '0':
                    list_preguntas_pasa.append(12)
                elif comment_form['12.10'] == '0' and comment_form['12.11'] == '0' and comment_form['12.12'] == '1' and comment_form['12.13'] == '1' and comment_form['12.14'] == '1':
                     list_preguntas_no_pasa.append(12)
                else:  list_preguntas_no_pasa.append(12)
            if pregunta['id'] == 13:                                       
                if comment_form['13.1'] == '0' : list_preguntas_no_pasa.append(13)                
                else: list_preguntas_pasa.append(13)
            if pregunta['id'] == 14:                                       
                if((comment_form['14.1']=='0')and(comment_form['14.2']=='0')and(comment_form['14.3']=='0')and(comment_form['14.4']=='0')and(comment_form['14.5']=='0')and(comment_form['14.6']=='0')):
                    list_preguntas_no_pasa.append(14)                          
                else: 
                    if ((comment_form['14.1']=='1')^(comment_form['14.2']=='1')^(comment_form['14.3']=='1')^(comment_form['14.4']=='1')^(comment_form['14.5']=='1')^(comment_form['14.6']=='1')):
                        if(comment_form['14.7']=='0'):
                            list_preguntas_no_pasa.append(14)
                        else:
                            if(comment_form['14.8']=='0'):
                                list_preguntas_no_pasa.append(14)
                            else:
                                list_preguntas_pasa.append(14)     
                    else: 
                        list_preguntas_pasa.append(14)
            if pregunta['id'] == 15:
                if((comment_form['15.1']=='0')and(comment_form['15.2']=='0')and(comment_form['15.3']=='0')and(comment_form['15.4']=='0')and(comment_form['15.5']=='0')and(comment_form['15.6']=='0'))or((comment_form['15.1']=='1')^(comment_form['15.2']=='1')^(comment_form['15.3']=='1')^(comment_form['15.4']=='1')^(comment_form['15.5']=='1')^(comment_form['15.6']=='1')):
                    list_preguntas_no_pasa.append(15)                    
                else:  list_preguntas_pasa.append(15)  
            if pregunta['id'] == 16:
                if((comment_form['16.1']=='1')and(comment_form['16.2']=='1')and(comment_form['16.3']=='1')and(comment_form['16.4']=='0')and(comment_form['16.5']=='0')):
                    list_preguntas_pasa.append(16)                          
                else: 
                    if((comment_form['16.1']=='0')and(comment_form['16.2']=='0')and(comment_form['16.3']=='0')and(comment_form['16.4']=='1')and(comment_form['16.5']=='1')):
                        list_preguntas_no_pasa.append(16)
                    else: list_preguntas_no_pasa.append(16)     
            if pregunta['id'] == 17:
                if((comment_form['17.1']=='0')and(comment_form['17.2']=='0')and(comment_form['17.3']=='0')and(comment_form['17.4']=='0')):
                    list_preguntas_no_pasa.append(17)                         
                else: list_preguntas_pasa.append(17)   
            if pregunta['id'] == 18:
                if (comment_form['18.1']=='0'):list_preguntas_no_pasa.append(18)                       
                elif((comment_form['18.2']=='0')and(comment_form['18.3']=='0')and(comment_form['18.4']=='0')):
                    list_preguntas_no_pasa.append(18)                          
                else: list_preguntas_pasa.append(18)
            if pregunta['id'] == 19:
                if(comment_form['19.1']=='1'):list_preguntas_pasa.append(19)                        
                elif(comment_form['19.2']=='1'):list_preguntas_pasa.append(19)
                elif(comment_form['19.3']=='1'):list_preguntas_pasa.append(19) 
                else: list_preguntas_no_pasa.append(19) 
            if pregunta['id'] == 20:
                if(comment_form['20.1']=='1'):list_preguntas_pasa.append(20)                      
                elif((comment_form['20.2']=='0')and(comment_form['20.3']=='0') and (comment_form['20.4']=='0')):list_preguntas_no_pasa.append(20) 
            
        if (len(list_preguntas_no_pasa)>=2):session['num_no_pasa']=4
        else: session['num_no_pasa']=5
        return redirect('results')
    else:  
        with open('preguntas.json', encoding="utf8") as file:
            data = json.load(file)
        riesgo = session.get('riesgo')
        suma = session.get('suma')
        list_preguntas = session.get('list_preguntas')  
        list_preguntas_nuevas = []
        for pregunta in data:
            if pregunta['id'] in list_preguntas:
                list_preguntas_nuevas.append(pregunta) 
        session['list_preguntas_nuevas'] = list_preguntas_nuevas
        return render_template('questionSecondPart.html', riesgo=riesgo, suma = suma, list_preguntas=list_preguntas_nuevas) 


@app.route('/results', methods=['GET'])
def result():       
    global imgBase64Global   
    with open('resultados.json', encoding="utf8") as file:
        riesgo = ''
        resultados = json.load(file)
        if session.get('resultadoDirecto') == 2:            
            for resultado in resultados:
                if resultado['riesgo'] == int(session.get('num_no_pasa')):
                    riesgo = resultado
        else:
            for resultado in resultados:
                if resultado['riesgo'] == int(session.get('riesgo')):
                    riesgo = resultado
    tea = session.get('tea')                   
    sinTea = session.get('sinTea')                   
    return render_template('result.html', img=imgBase64Global, riesgo=riesgo, tea=tea, noTea=sinTea, nombre=session.get('nombre'), apellido=session.get('apellido')) 


if __name__ == '__main__':
    app.run(port=3000, debug=True)


