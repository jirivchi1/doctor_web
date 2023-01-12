#importamos librerias
import openai
import streamlit as st
from PIL import Image



#ajustamos GPT-3 api key
openai.api_key = st.secrets['pass']

st.set_page_config(layout="wide")
st.title('Doctor Web')

col1, col2 = st.columns(2, gap = 'large')

with st.sidebar:

  ## información básica
  picture = st.camera_input("Tome la foto")  

  name = st.text_input('Escriba Nombre', ' ')

  prim_inf = st.selectbox('Indique Sexo', ('Hombre', 'Mujer'))  

  seg_inf = st.text_input('Indique Edad', ' ')
  
  st.markdown("***")
  ##preguntas hipocráticas
  prim_preg = st.text_input('¿Qué le ocurre?')
  
  prim1_preg = st.selectbox(
    'Indique intensidad de su dolor en función de la siguiente escala:',
    ('Ausencia de dolor','Leve', 'Moderado', 'Severo','Insoportable'))

  seg_preg = st.selectbox(
      'Indique desde cuándo presenta los síntomas:',
      ('horas', '2 días','3 o 4 días', 'semanas','meses'))


  st.markdown("***")
  ## preguntas adicionales

  opt1_preg = st.selectbox(

    'Tengo sobrepeso u obesidad',
    ('Si', 'No')

  )

  opt2_preg = st.selectbox(
    'Tengo hipertensión',
    ('Si','No','No lo sé')
  )

  opt3_preg = st.selectbox(
    'Soy fumador',
    ('Si','No')
  )

  opt4_preg = st.selectbox(
    'Tengo el colesterol alto',
    ('Si','No','No lo sé')
  )

with col1:
  
  
  st.markdown('### Consulta')

  texto = f'Soy {name}, un/a {prim_inf.lower()} con {seg_inf} años. Tengo {prim_preg}, es un dolor {prim1_preg.lower()} y llevo así durante {seg_preg}.'

  st.write(texto)
  
  
  st.markdown('##### Información Adicional: ')

  info = [opt1_preg, opt2_preg, opt3_preg, opt4_preg]
  resp = ['sobrepeso','hipertensión', 'tabaquismo','colesterol alto']

  info_ad = ' '
  for x in range(0,4):
    
    if info[x]=='Si':
      #st.write(f'Tengo {resp[x]}.')
      info_ad += f'Tengo {resp[x]}. '
    
    else:
      #st.write(f'No tengo {resp[x]}.')
      info_ad += f'No tengo {resp[x]}. '


  st.write(info_ad)

  st.markdown('##### Otra información relevante:')
  observacion = st.text_area('¿Tiene idea de cuál podría ser la causa?')

  #st.markdown("***") 
   
  tipo_resultado = st.radio( label= 'Elija qué tipo de información desea:',
   options= ['Conciso','Detallado'],label_visibility='visible')

  if tipo_resultado == 'Conciso':
    token =  50
  else:
    token = 516


  if st.button("Generar diagnóstico",type='primary'):

    respuesta = openai.Completion.create(
      engine = 'text-davinci-002',  #modelo 
      prompt = texto + info_ad + observacion + ',¿qué tengo y qué puedo comprar en la farmacia?',  # input que pregunta al modelo -gpt-3.
      max_tokens = token,    #token = 50 -> respuesta concisa, token = 516 -> respuesta más detallada.
      temperature = 0.5)     # parámetro que controla la aleatoriedad o la creatividad del texto generado por el modelo. 0 = más predictivo. 1 = más aleatorio.
                            

    res = respuesta['choices'][0]['text']
    st.success(res)
    st.download_button('Descargar Resultados', res)


with col2:
  
  if picture:
    st.image(picture)
  
  st.write(f'Paciente: {name}')